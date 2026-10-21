---
sr-due: <% tp.date.now("YYYY-MM-DD", 3) %>
sr-interval: 1
sr-ease: 2.5
---

# Event Streaming — Retained Logs, Partitions, Offsets, and Replay

## Definition and use cases

**Event streaming continuously records and processes sequences of events.** In a retained-log system such as Kafka, events remain available according to retention policy, and consumers track where they have read. Multiple applications can independently consume the same history.

Think of a journal rather than a task that disappears after one worker takes it. A notification service reads recent job completions, while an analytics service replays yesterday's completions to build a report. Reading normally advances the consumer's position; it does not individually remove the record from the log.

Use event streaming for event-driven integration, audit/replay pipelines, telemetry, CDC, and continuously updated projections. A simple work queue is often easier when each task should be handed to one worker and historical replay is unimportant. SSE also streams events, but is a client-delivery mechanism; it is not itself a durable event log or stream-processing platform.

## Real-world use cases

| Real-world scenario | Events retained and processed | Why an event stream fits |
|---|---|---|
| Product clickstream analytics | Page views, searches, clicks, and purchases feed continuously updated metrics. | Independent consumers can calculate funnels or other views and replay retained events when logic changes. |
| Transaction anomaly monitoring | Transaction events feed rolling counts and pattern detection. | Consumers can process events over time windows and maintain their own progress through the log. |
| Connected vehicle telemetry | Vehicle measurements feed live monitoring and later historical analysis. | Retained events support both ongoing processing and replay within the configured retention period. |
| Database change propagation | Change-data-capture events update a search index and analytical store. | Downstream systems can independently track progress and catch up after outages, with an appropriate initial snapshot strategy. |
| Retail inventory projections | Stock changes from warehouses feed an availability read model. | Partitioned processing can build current views from retained changes; ordering and authoritative reservation rules remain explicit. |
| Recommendation pipelines | User activity feeds feature updates and later experimentation. | Different consumers can read the same history at their own pace. |
| Rebuilding a dashboard after a bug | A corrected consumer reprocesses retained job or order events. | Offsets and retention make historical reprocessing possible without asking the original producer to recreate every event. |
| Operational event history | Deployment, job, and service events feed troubleshooting views. | A retained log can support multiple operational consumers, subject to storage and retention requirements. |

**Walk through a clickstream:** one consumer group calculates active-session counts while another writes events to an analytical store. Their progress is independent. If the counting logic has a bug, a replacement consumer can replay the retained interval into a fresh output view. It must handle duplicates and avoid replaying irreversible side effects such as sending historical customer emails again.

The log is available only according to its retention and compaction policies. Keeping events in a broker does not automatically make the application an event-sourced system, nor does it automatically satisfy a permanent audit requirement. A browser dashboard may consume SSE generated from a processed view of this backend stream.

**Interview practice:** explain why replay matters to a product, how events should be partitioned, and what happens when a consumer falls behind the retention window.

## Core vocabulary

| Concept | Meaning |
|---|---|
| Topic | Named collection of events |
| Partition | Ordered subset/log within a topic |
| Offset | Position in one partition; not a global timestamp |
| Key | Value used by the partitioning policy, often a job/customer ID |
| Consumer group | Cooperating consumers sharing partition assignments in the traditional Kafka group model |
| Committed offset | Saved progress from which a group resumes; commonly the next position to consume |
| Retention | How long/how much history remains, subject to configuration |
| Lag | Difference between available data and consumer progress |
| Compaction | Retention policy preserving latest values per key over time, not an immediate delete of all older records |

For traditional partition-assigned groups, different groups independently read the topic, while members of one group divide partitions. A partition is assigned to one consumer in that group at a time. Kafka now also has other consumption models; this guide focuses on the established partition/group model rather than claiming every Kafka mode behaves identically.

## Ordering and partitioning

Ordering is per partition, not across the whole topic. Using job ID as a key can keep a job's events together under a stable partitioning setup. Adding partitions or changing the partitioner can change key placement, so plan ordering-sensitive migrations. Multiple producers and asynchronous processing still require application reasoning about versions and completion order.

More partitions can enable parallelism, but also add metadata, recovery, rebalancing, and operational cost. More consumers than assigned partitions does not increase parallelism for that traditional group/topic allocation.

## Runnable Python: independent offsets and replay

Save as `stream_log_demo.py`. This in-memory model demonstrates semantics, not a durable or concurrent broker. There is one partition. Each group stores the next record index.

```python
class EventLog:
    def __init__(self):
        self.records = []
        self.offsets = {}

    def append(self, event):
        self.records.append(event)
        return len(self.records) - 1

    def poll(self, group):
        offset = self.offsets.get(group, 0)
        if offset >= len(self.records):
            return None
        return offset, self.records[offset]

    def commit(self, group, next_offset):
        if not 0 <= next_offset <= len(self.records):
            raise ValueError("Invalid offset")
        self.offsets[group] = next_offset

if __name__ == "__main__":
    log = EventLog()
    log.append({"event_id": "evt-1", "status": "running"})
    log.append({"event_id": "evt-2", "status": "completed"})
    print("notifications:", log.poll("notifications"))
    log.commit("notifications", 1)
    print("notifications next:", log.poll("notifications"))
    print("analytics independently:", log.poll("analytics"))
    print("analytics redelivery without commit:", log.poll("analytics"))
```

Expected: notifications moves to record 1; analytics still sees record 0 and repeats it until it commits. In a real system, retention may remove data before a slow consumer catches up; define the reset/resync policy explicitly.

## Kafka Python producer and consumer

Requires `confluent-kafka`, a development Kafka broker at `127.0.0.1:9092`, and an existing topic `learning.jobs` with a suitable partition/replication configuration. These snippets are broker-dependent integration examples, not tests against a running cluster here. Use your broker's TLS/SASL settings outside a local lab.

Save as `kafka_producer.py`:

```python
import json
from confluent_kafka import Producer

if __name__ == "__main__":
    failures = []
    producer = Producer({
        "bootstrap.servers": "127.0.0.1:9092",
        "enable.idempotence": True,
        "delivery.timeout.ms": 10000,
    })

    def delivered(error, message):
        if error is not None:
            failures.append(str(error))

    producer.produce(
        "learning.jobs", key="job-123",
        value=json.dumps({"event_id": "evt-1", "status": "completed"}),
        on_delivery=delivered,
    )
    remaining = producer.flush(12)
    if remaining or failures:
        raise RuntimeError({"remaining": remaining, "failures": failures})
    print("Delivery confirmed")
```

Save as `kafka_consumer.py`:

```python
import json
from confluent_kafka import Consumer, KafkaException

if __name__ == "__main__":
    consumer = Consumer({
        "bootstrap.servers": "127.0.0.1:9092",
        "group.id": "learning.notifications",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
        "enable.auto.offset.store": False,
    })
    consumer.subscribe(["learning.jobs"])
    try:
        while True:
            message = consumer.poll(1)
            if message is None:
                continue
            if message.error():
                raise KafkaException(message.error())
            event = json.loads(message.value())
            print("Process", event)  # Replace with an idempotent durable effect.
            consumer.commit(message=message, asynchronous=False)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
```

The demonstration prints then commits. A crash between them can print twice; committing first could skip processing after a crash. Real effects need idempotency or transactional coordination. `auto.offset.reset=earliest` applies when there is no valid committed offset; it does not reset an existing group to the start on every run.

Producer idempotence protects specified producer retry behavior, not arbitrary duplicates across application restarts or duplicate business commands. Kafka transactions can coordinate offsets and outputs within Kafka under suitable consumer settings; they do not automatically transact with an external payment API or database.

## Processing time, event time, and operations

**Event time** is when the source event occurred; **processing time** is when your system handles it. Network delay and retries create late arrivals. Aggregations may use windows, watermarks, and allowed-lateness policies; a watermark is a progress estimate/policy, not proof that no late event can arrive.

**Rebalance:** partition assignments change as consumers join/leave or conditions change. Long processing can prevent timely polling and trigger reassignment. Bound processing, handle revoked partitions, and commit only contiguous completed progress per partition. Do not commit past unfinished earlier records when parallelizing handlers.

Use schemas and compatibility checks, event IDs, partition-aware ordering, monitoring of lag/oldest unprocessed age, retention capacity planning, poison-event handling, and replay controls. Replaying events into an external system can repeat side effects unless designed otherwise.

## Quick recall and interview practice

**Remember:** a partition is an ordered log; a group has progress; replay depends on retained history. Exactly-once claims must name their boundaries.

**Interview answer:** “I would use a retained event stream when independent consumers need history and replay. I would choose keys/partitions for ordering and parallelism, commit progress after safe processing, and design idempotency for external effects.”

1. Why do two consumer groups both receive history while two members of one group divide it?
2. What does a committed offset represent?
3. Why is ordering across the entire topic not automatic?
4. What does producer idempotence fail to guarantee for a business workflow?
5. How can parallel processing accidentally commit past unfinished work?

References: [Kafka design](https://kafka.apache.org/41/design/design/), [Confluent Python client](https://docs.confluent.io/kafka-clients/python/current/overview.html). Related: [Pub/sub](14-pubsub.md), [Workflows](17-reliable-distributed-workflows.md).
