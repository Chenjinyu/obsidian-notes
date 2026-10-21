---
sr-due: <% tp.date.now("YYYY-MM-DD", 3) %>
sr-interval: 1
sr-ease: 2.5
---

# Message Queues — Durable Work and Competing Consumers

## Definition and use cases

**A message queue holds messages until consumers can process them.** A producer submits work; workers receive it independently of the producer's request. In a work-queue pattern, consumers compete for messages so each task is normally handled by one worker at a time. Redelivery can still cause repeated handling.

For an AI batch job, the API can save the job, enqueue a command, and return a job ID. Workers execute jobs as capacity becomes available. This separates request latency from execution time and lets a backlog absorb a temporary burst. A queue does not create unlimited capacity: a growing backlog is delayed work that still needs storage and processing.

Use queues for background jobs, email generation, image processing, batch imports, and load leveling. Prefer synchronous HTTP/RPC when the caller needs a short immediate response. Prefer pub/sub when independent applications each need a copy; prefer a retained event log when replaying history is central.

## Terms that matter

| Term | Meaning |
|---|---|
| Producer / consumer | Sends messages / receives and processes them |
| Broker | Service managing routing, queues, and delivery |
| Acknowledgment | Consumer tells the broker it accepted/completed handling according to its contract |
| Publisher confirm | Broker confirms publication handling; not proof the consumer completed the job |
| Visibility timeout / lease | Temporarily hides a delivered message from other consumers in systems using this model |
| Prefetch | Limits outstanding unacknowledged deliveries to a consumer/channel scope |
| Dead-letter queue | Stores messages that cannot complete normal processing, under configured routing/policies |
| Poison message | Deterministically fails due to content, schema, or incompatible code |

RabbitMQ manual acknowledgments and SQS-style visibility timeouts are different mechanisms. In SQS, delete after success and extend visibility for longer work as appropriate. In RabbitMQ, acknowledge delivery on the correct channel; unacknowledged messages can be redelivered after connection loss. Neither alone makes side effects exactly once.

## Workflow and failure branches

```mermaid
flowchart TD
    P["Producer publishes"] --> Q["Broker queue"]
    Q --> W["Worker receives"]
    W --> V{"Valid message?"}
    V -->|"No"| D["Dead-letter or quarantine"]
    V -->|"Yes"| T["Commit idempotent effect"]
    T --> A["Acknowledge delivery"]
    T -. "Crash before acknowledgment" .-> R["Later redelivery"]
    R --> W
```

## Python example with RabbitMQ

This example requires a local RabbitMQ broker and `pika`. It is not a brokerless demo. Use a disposable development broker, with an AMQP URL in `AMQP_URL` if it is not localhost. Production needs suitable TLS, credentials, authorization, and replication settings. The snippets use named demo queues; do not point them at an unrelated production broker.

Save as `queue_setup.py`:

```python
import os
import pika

QUEUE = "learning.jobs"

def connect():
    params = pika.URLParameters(os.getenv(
        "AMQP_URL", "amqp://guest:guest@127.0.0.1:5672/%2F"
    ))
    params.heartbeat = 30
    params.blocked_connection_timeout = 5
    return pika.BlockingConnection(params)

def declare(channel):
    channel.exchange_declare("learning.dead", exchange_type="fanout", durable=True)
    channel.queue_declare("learning.jobs.dead", durable=True)
    channel.queue_bind("learning.jobs.dead", "learning.dead")
    channel.queue_declare(
        QUEUE, durable=True,
        arguments={"x-dead-letter-exchange": "learning.dead"},
    )
```

Save as `queue_producer.py`:

```python
import json
import pika
from queue_setup import connect, declare, QUEUE

if __name__ == "__main__":
    connection = connect()
    try:
        channel = connection.channel()
        declare(channel)
        channel.confirm_delivery()
        body = json.dumps({"event_id": "task-1", "job_id": "job-123"}).encode()
        channel.basic_publish(
            exchange="", routing_key=QUEUE, body=body, mandatory=True,
            properties=pika.BasicProperties(
                delivery_mode=2, content_type="application/json", message_id="task-1"
            ),
        )
        print("Publication confirmed")
    finally:
        connection.close()
```

Save as `queue_worker.py`. This local example's “effect” is a unique database record, so record creation and duplicate protection share one transaction. It does not perform a real external AI call.

```python
import json
import sqlite3
from contextlib import closing
from queue_setup import connect, declare, QUEUE

DB_PATH = "queue_effects.sqlite3"

def apply_once(event):
    with closing(sqlite3.connect(DB_PATH, timeout=2)) as db:
        with db:
            db.execute("CREATE TABLE IF NOT EXISTS effects "
                       "(event_id TEXT PRIMARY KEY, job_id TEXT NOT NULL)")
            previous = db.execute(
                "SELECT job_id FROM effects WHERE event_id = ?", (event["event_id"],)
            ).fetchone()
            if previous and previous[0] != event["job_id"]:
                raise ValueError("Event ID reused with different content")
            db.execute("INSERT OR IGNORE INTO effects VALUES (?, ?)",
                       (event["event_id"], event["job_id"]))

def handle(channel, method, properties, body):
    try:
        event = json.loads(body)
        if not isinstance(event, dict) or any(
            not isinstance(event.get(k), str) or not event[k]
            for k in ("event_id", "job_id")
        ):
            raise ValueError("Invalid task")
        apply_once(event)
    except (ValueError, UnicodeError):
        channel.basic_nack(method.delivery_tag, requeue=False)
        return  # Route toward the configured dead-letter queue.
    channel.basic_ack(method.delivery_tag)

if __name__ == "__main__":
    connection = connect()
    try:
        channel = connection.channel()
        declare(channel)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(QUEUE, on_message_callback=handle, auto_ack=False)
        channel.start_consuming()
    finally:
        connection.close()
```

Start the worker, then run the producer twice. The queue receives two deliveries with the same event ID, while the local effects table keeps one row. A database error is not swallowed: the worker exits, closing its connection with the delivery unacknowledged. Recovery/restart policy is intentionally not implemented.

The local SQLite file is shared only where the file is shared. A fleet of machines needs a shared authoritative database or another idempotency design. Long-running callbacks can block this client's heartbeat handling; use an appropriate asynchronous/offloaded processing design and channel-safe acknowledgments.

## Supporting technology and pitfalls

- Save a job and an outbox record in one database transaction if submission must not be lost between database commit and publication.
- Queue durability, persistent message flags, confirms, and replicated queue configuration solve different problems. A successful publish call before confirmation is not enough evidence of durable acceptance.
- Dead-letter routing is not automatically lossless. Its safety depends on queue type, broker configuration, and destination availability; monitor it and choose an appropriate supported dead-letter strategy when retention is critical.
- The example declares dead-letter settings as queue arguments for a self-contained lab. Operational deployments generally prefer broker policies for settings that need to change without redeploying and redeclaring queues.
- Retry transient processing failures with bounded attempts and delay. Immediate requeue loops can monopolize a queue and hammer a dependency.
- Limit message size, validate schemas, propagate trace context, and separate tenant quotas where needed.
- Monitor oldest-message age, backlog, processing rate, in-flight count, retries, and dead letters. Queue length alone cannot tell whether the system meets a job-completion target.
- More consumers do not guarantee linear scaling; database contention, downstream limits, ordering, and task duration can dominate.

## Quick recall and interview practice

**Remember:** publisher confirm protects one boundary; consumer acknowledgment protects another. Commit the intended effect before acknowledging, and handle redelivery.

**Interview answer:** “I would queue long-running work, use durable publication and manual acknowledgments, and make the worker idempotent. I would bound retries, control prefetch/concurrency, and monitor queue age rather than assuming the broker guarantees exactly-once processing.”

1. What if a worker commits its effect and crashes before acknowledging?
2. What if the producer times out waiting for confirmation?
3. How is a visibility timeout different from successful processing?
4. Why can adding workers make an overloaded database worse?
5. Which failure belongs in a dead-letter queue rather than an immediate retry loop?

References: [RabbitMQ work queues](https://www.rabbitmq.com/tutorials/tutorial-two-python), [confirms and acknowledgments](https://www.rabbitmq.com/docs/confirms), [dead-letter configuration and safety](https://www.rabbitmq.com/docs/dlx), [SQS visibility timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html). Related: [Pub/sub](14-pubsub.md), [Workflows](17-reliable-distributed-workflows.md).
