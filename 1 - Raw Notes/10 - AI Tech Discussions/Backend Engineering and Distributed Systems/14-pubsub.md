---
sr-due: <% tp.date.now("YYYY-MM-DD", 3) %>
sr-interval: 1
sr-ease: 2.5
---

# Publish/Subscribe — One Event, Independent Subscribers

## Definition and mental model

**Publish/subscribe, or pub/sub, is a pattern in which producers publish to a topic or channel, and interested subscribers receive matching messages.** Producers do not directly call each subscriber. A completion event might independently update a notification service, an analytics service, and a browser gateway.

Think of subscribing to a newsletter: multiple subscribers each want their own copy. This differs from workers competing to take one task from a queue. A pub/sub system can implement fan-out by placing a separate copy into each subscriber's durable queue, then let workers within that subscriber compete for its copy.

Pub/sub describes routing and decoupling, not a universal durability guarantee. Redis Pub/Sub is live ephemeral delivery; SNS feeding durable SQS queues and retained streaming systems have different recovery behavior. Ask what happens while a subscriber is offline.

## Use cases and design choices

Use pub/sub for independent reactions to events, notifications, cache invalidation signals, and live updates. It reduces direct coupling: the producer does not need to know every consumer's URL or implementation.

It does not eliminate semantic coupling. Subscribers still depend on event schemas, meanings, identifiers, and delivery guarantees. An event such as `JobCompleted` describes a fact; a command such as `SendCompletionEmail` requests an action by an intended owner. Clear names prevent different services from assuming conflicting responsibilities.

| Pattern | Who receives one publication? | Typical intent |
|---|---|---|
| Work queue | One competing worker per delivery, with possible redelivery | Distribute tasks |
| Pub/sub fan-out | Each independent subscriber/subscription | Distribute knowledge of an event |
| Pub/sub with subscriber queues | Each subscription, then one worker within it | Independent durable processing |
| Retained event stream | Independent groups read at their own offsets | Replayable history and projections |

## Runnable Python mental-model demo

Save as `pubsub_demo.py`. No external packages or broker are needed. Two subscribers have separate bounded queues. Publishing to one shared queue instead would make them compete rather than broadcast.

```python
import asyncio

class Topic:
    def __init__(self):
        self.subscribers = []

    def subscribe(self):
        queue = asyncio.Queue(maxsize=10)
        self.subscribers.append(queue)
        return queue

    def publish(self, event):
        for queue in self.subscribers:
            queue.put_nowait(event)

async def receive(name, queue):
    event = await queue.get()
    print(name, "received", event["event_id"])

async def main():
    topic = Topic()
    notifications = topic.subscribe()
    analytics = topic.subscribe()
    topic.publish({"event_id": "evt-123", "type": "JobCompleted"})
    await asyncio.gather(
        receive("notifications", notifications),
        receive("analytics", analytics),
    )

if __name__ == "__main__":
    asyncio.run(main())
```

Expected: both subscribers receive evt-123. This is not a durable broker: process exit loses data, absent subscribers miss events, and a full queue raises an exception. If some queues have already accepted the event before another fills, publication can be partial. A production policy must deliberately block, drop/coalesce, disconnect, or persist rather than pretend this is atomic fan-out.

## Python Redis Pub/Sub example

Install `redis` and use a disposable local Redis. Save as `redis_pubsub_demo.py`; run one or more subscribers first with `python redis_pubsub_demo.py subscribe`, then a publisher with `python redis_pubsub_demo.py publish`.

```python
import json
import sys
import redis

CHANNEL = "learning.job.completed"

def main(role):
    client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True,
                         socket_connect_timeout=2)
    try:
        if role == "publish":
            receivers = client.publish(CHANNEL, json.dumps({"event_id": "evt-123"}))
            print("Matching subscriptions:", receivers)
        elif role == "subscribe":
            with client.pubsub() as subscription:
                subscription.subscribe(CHANNEL)
                for message in subscription.listen():
                    if message["type"] == "subscribe":
                        print("Ready", flush=True)
                    elif message["type"] == "message":
                        print(json.loads(message["data"]), flush=True)
        else:
            raise ValueError("Use subscribe or publish")
    finally:
        client.close()

if __name__ == "__main__":
    main(sys.argv[1])
```

Wait for `Ready` before publishing. The returned count is not proof that applications completed processing. Reconnecting to Redis Pub/Sub does not replay messages sent during disconnection. This is suitable for live hints when the consumer can refresh authoritative state; it is insufficient by itself for an irreplaceable billing event.

## Supporting techniques and common interview follow-ups

| Requirement | Supporting design |
|---|---|
| Subscribers may be offline | Durable per-subscriber queues or retained log |
| One subscriber is slow | Independent backlog and quotas; avoid blocking all subscribers |
| Repeated events | Stable event IDs and idempotent processing |
| Evolving event shape | Versioned contracts and compatibility checks |
| Wrong or missing order | Resource versions, partitioning, or authoritative resync |
| Sensitive topics | Topic/subscription ACLs and tenant-aware routing |
| Event never published after commit | Transactional outbox or suitable CDC pipeline |

For an SSE/WebSocket gateway fleet, every interested gateway needs the relevant event, or a router must send it to the gateway holding the connection. A single shared competing-consumer group can route a message to a gateway with no matching browser. Fan-out topology must match connection ownership.

For cache invalidation, a lost signal can leave stale cache entries. Add TTLs, version checks, or reconciliation. Pub/sub is a notification path, not a substitute for the consistency design.

Monitor subscriber lag/backlog where retained, disconnected subscribers, delivery failures, dropped messages, and handler latency. Maintain event ownership and documentation so “loosely coupled” does not become “nobody knows who depends on this event.”

## Quick recall and practice

**Remember:** independent subscribers each receive their own event view; workers within one subscription may compete. Durability is a product/configuration property, not part of the word pub/sub.

**Interview answer:** “I would use pub/sub when several independent systems need to react to an event. I would choose ephemeral or durable subscriptions based on whether offline consumers must catch up, and define schema, ordering, and idempotency contracts.”

1. How does a shared work queue differ from one queue per subscriber?
2. What happens if a Redis subscriber is offline for ten seconds?
3. Can a successful publish prove that every subscriber finished its work?
4. How do you isolate a slow analytics subscriber from notifications?
5. Why might one consumer group be wrong for browser-gateway fan-out?

References: [Redis Pub/Sub](https://redis.io/docs/latest/develop/pubsub/), [RabbitMQ publish/subscribe](https://www.rabbitmq.com/tutorials/tutorial-three-python). Next: [Event streaming](15-event-streaming.md).
