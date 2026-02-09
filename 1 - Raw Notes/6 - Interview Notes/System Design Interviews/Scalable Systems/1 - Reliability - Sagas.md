Date: 2026-01-30
Course: https://www.youtube.com/watch?v=d2z78guUR4g(Youtube), https://www.tryexponent.com/courses/system-design-interviews/reliability-strategies(Exponent)
Tags: [[API]]  [[interview]] [[../../../7 - JCUS.LINK/System Design]] [[High Level ]] [[Low Level]]

# Content

## Defination
Saga reliability in system design ensures data consistency across distributed microservices by breaking long-running, multi-service transactions into smaller, independent lcal transactions. 
if one step fails, the sage executes compensating transactions to revert preceding steps, maintaining eventual consistency without relying on complex, two phrase commits
### Key aspects of Saga reliability include:
- Compensating Transactions: explicit, pre-designed actions that undo changes made by a successful step if a later step fails, ensuring the system returns to a known, valid state
- Choreography or Orchestration(编舞或配器): sagas are implemented via choreography (services exchange events) or orchestration (a central coordinator manages steps).
- Eventual Consistency: Instead of immediate ACID compliance, the system is designed to reach a consistent state over time.
- Failure Handing: The pattern enables automatic rollback, allowing the system to handle, for example, a stock reservation failure after a payment has already been processed.

Common implementations for ensuring reliability includes the Outbox pattern (ensuring atomic, reliable message publishing) and maintaining Idempotency in services(allowing steps to retried without side effects)

![](assets/1%20-%20Reliability%20-%20Sagas/file-20260130012529784.png)
![](assets/1%20-%20Reliability%20-%20Sagas/file-20260130012429138.png)
## Why distributed transactions are hard in microservices

If Flight, Hotel, Car, Notification each have separate DBs, there’s **no single ACID transaction** that spans them (not safely, not at scale, not with good availability). So you need a coordination strategy.

There are two main strategies people talk about:
1. **Two-Phase Commit (2PC)** — strong consistency, heavy coordination
2. **Saga pattern** — eventual consistency + compensations, designed for microservices

---
# Two-Phase Commit (2PC)

### What it is
A classic distributed transaction protocol with a **coordinator** and participants.
2-phase commit used **atomic rollback via coordinator** vs saga orchestration **uses explicit compensating actions**.

### How it works
**Phase 1: Prepare**
* Coordinator asks each service: “Can you commit?”
* Each service locks resources, writes “prepared” state, replies YES/NO.

**Phase 2: Commit / Abort**
* If everyone said YES → coordinator tells everyone COMMIT
* If anyone said NO → coordinator tells everyone ABORT (rollback)
### Pros
* **Strong consistency**: you get close to “atomic commit across services”
* Clear “committed or not” outcome
### Cons (why it’s unpopular for microservices)
* **Blocking**: if coordinator dies after “prepare”, participants can be stuck holding locks
* **Locks/resources held** longer → reduced throughput, higher latency
* **Tight coupling** across services and databases
* **Availability suffers** (CAP tradeoff): if any participant/coordinator is down, the whole transaction is impacted
* Operationally complex across heterogeneous systems

In microservices, this tends to be a bad fit because teams prioritize **availability + independent deployability**.

---
# Saga Pattern
### What it is
A saga is a **sequence of local transactions** (each service commits to its own DB), plus **compensating transactions** to undo work if something later fails.

Instead of “all services commit together”, you do:
* Step 1 commits locally
* Step 2 commits locally
* Step 3 commits locally
* If step 3 fails, you run compensations to undo step 2 and step 1
### Pros
* No distributed locks across services
* Services stay decoupled and independently deployable
* Better availability and scalability
* Works naturally with async messaging and queues
### Cons
* **Eventual consistency**: system can be temporarily “in-between”
* You must design **compensations** (undo) which are not always perfect
* More engineering: idempotency, retries, timeouts, state tracking, ordering

---
# Why you “need” Saga instead of 2PC
Use Saga because, in microservices, you usually want:
* **high availability**
* **no long-lived distributed locks**
* **services can fail independently**
* **async workflows**

2PC gives atomicity but at the cost of availability and performance; Saga gives availability/performance but you accept eventual consistency and compensate on failure.

---

# When you should use Sagas
Use sagas when:
* A business process spans **multiple services/databases**
* You can tolerate **eventual consistency**
* You can define a meaningful **compensation** for each step (cancel reservation, refund, release hold, etc.)
* You need resilience across partial failures

Avoid sagas when:
* You truly require **strict atomicity** across everything (rare, but sometimes in finance/ledger core)
* Compensations are impossible or legally/physically irreversible (e.g., “ship package” once shipped, you can’t un-ship; you can only create a return process)

---

# Your use case: Flight + Hotel + Car + Notification
## The real trick: don’t “book” immediately—use holds + confirm
A practical saga usually looks like:

* Reserve/Hold flight (temporary)
* Reserve/Hold hotel (temporary)
* Reserve/Hold car (temporary)
* Confirm all reservations
* Send notification

That’s better than booking each irreversibly up front.
### Example saga steps + compensations

| Step | Action (forward)                | Compensation (undo)                                                   |
| ---- | ------------------------------- | --------------------------------------------------------------------- |
| 1    | Flight: create reservation/hold | Flight: cancel reservation                                            |
| 2    | Hotel: create reservation/hold  | Hotel: cancel reservation                                             |
| 3    | Car: create reservation/hold    | Car: cancel reservation                                               |
| 4    | Confirm flight/hotel/car        | If confirm partially fails, compensate confirmed ones (refund/cancel) |
| 5    | Notify user                     | Usually no compensation needed (or send “correction” message)         |

Important: **Notification should be last**, and should be **idempotent** (sending twice shouldn’t confuse the user).

---
# How the saga “controls” steps: two styles

## 1) Orchestration (recommended for your scenario)

A central **Saga Orchestrator** tells each service what to do and tracks state.

Flow:
1. Orchestrator → Flight: Reserve
2. Orchestrator → Hotel: Reserve
3. Orchestrator → Car: Reserve
4. If all succeed → Orchestrator → Confirm all
5. Orchestrator → Notification: Send

If Hotel fails at step 2:
* Orchestrator → Flight: Cancel reservation (compensation)
* End saga as FAILED

**Why orchestration is nice:** one place to see the workflow, retries, timeouts, compensation logic.

## 2) Choreography(编舞) (event-driven chain)
Services emit events and react to events:
* FlightReserved → Hotel service tries to reserve
* HotelReserved → Car service tries to reserve
* CarReserved → Notification sends

If something fails, services emit “Failed” events and others compensate.
**Downside(缺点):** logic gets scattered(分散); debugging becomes “event spaghetti” unless you’re very disciplined(自律).

---

# What you must implement for a real Saga (or you’ll get double-bookings)

### 1) Idempotency
Each command should be safe to retry:
* “ReserveHotel(sagaId)” called twice → same reservation, not two reservations.

### 2) Durable state tracking (Saga log)
Orchestrator should persist:
* sagaId
* current step
* status (RUNNING/COMPENSATING/FAILED/SUCCEEDED)
* service correlation IDs (flightReservationId, etc.)

### 3) Timeouts
If Car reservation doesn’t respond in 10 seconds:
* mark step failed
* run compensations

### 4) Outbox / reliable messaging (if async)
To avoid “DB commit succeeded but event publish failed”, use the **transactional outbox** pattern.

### 5) Compensations are not the same as rollback
Compensation is a **new business action**:
* “Cancel reservation” / “Refund” / “Release hold”
  It can fail too → you need retry and reconciliation.

---
# A concrete failure example

**Hotel step fails**
1. Flight reserved successfully (flight DB committed)
2. Hotel reserve fails (service down or no rooms)
3. Orchestrator triggers FlightCancel
4. Saga ends FAILED
5. User gets “Could not complete booking” (or no notification at all until final decision)

During steps 1–3 the system is *temporarily inconsistent* (flight reserved but trip not complete). Saga is designed to manage that inconsistency.

---
## Below is a minimal-but-real saga implementation pattern
Below is a **minimal-but-real** saga implementation pattern for your travel booking example using:
- **FastAPI** (orchestrator API)
- **Postgres** for **saga table** + **outbox table**
- **SQS** (commands/events) _(I’ll note the Kafka swap at the end)_
- **Transactional Outbox** (DB write + “publish later” so you don’t lose messages)

#### What is Transcational Outbox Pattern: guarantees that database changes and outgoing events/messages are saved atomically in the same local transaction.
##### in plain english: update data record and event to send -- together or not at all
This pattern prevents the classic “DB committed but message publish failed” problem.

---
## Architecture (minimal saga with orchestration)
**Queues**
- `trip-commands.fifo` (or per-service command queues)
- `trip-events.fifo` (events back to orchestrator)

**Orchestrator**
- `POST /trip-bookings` → creates saga row + inserts outbox “ReserveFlight” → returns `202` with sagaId
- Outbox publisher sends commands to SQS
- Event consumer receives events and advances saga or compensates

**Services (Flight/Hotel/Car)**
- Each consumes commands, does **local transaction**, writes **local outbox** event, publisher sends to SQS
- Idempotent by `saga_id + step`

---
# 1) Postgres schema (saga table + outbox)
### sages and outbox tables in the same database, so: update data and record the event to send -- together or not at all
```sql
-- saga orchestration state
create table if not exists sagas (
  saga_id uuid primary key,
  status text not null, -- RUNNING | COMPENSATING | SUCCEEDED | FAILED
  step text not null,   -- RESERVE_FLIGHT | RESERVE_HOTEL | RESERVE_CAR | CONFIRM | NOTIFY | DONE
  flight_res_id text,
  hotel_res_id text,
  car_res_id text,
  error_code text,
  error_message text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- transactional outbox (for both orchestrator and services)
create table if not exists outbox (
  id bigserial primary key,
  aggregate_type text not null,     -- "saga" / "flight" / "hotel" / "car"
  aggregate_id uuid not null,
  event_type text not null,         -- ReserveFlightCommand, FlightReservedEvent, etc.
  payload jsonb not null,
  status text not null default 'NEW', -- NEW | SENT | ERROR
  created_at timestamptz not null default now(),
  sent_at timestamptz
);

create index if not exists idx_outbox_new on outbox(status, created_at);
```

**Key idea:** whenever you change saga state, you **also insert outbox rows in the same DB transaction**. Publishing happens later.

---
# 2) Message contracts (commands/events)

Keep them small and explicit:
```json
// Command example
{
  "type": "ReserveFlightCommand",
  "saga_id": "uuid",
  "step": "RESERVE_FLIGHT",
  "user_id": "u1",
  "trip": { "from": "ORD", "to": "SFO", "date": "2026-02-10" }
}

// Event example
{
  "type": "FlightReservedEvent",
  "saga_id": "uuid",
  "step": "RESERVE_FLIGHT",
  "reservation_id": "F123"
}

// Failure event example
{
  "type": "HotelReserveFailedEvent",
  "saga_id": "uuid",
  "step": "RESERVE_HOTEL",
  "error_code": "NO_ROOMS",
  "error_message": "No availability"
}
```

---
# 3) Orchestrator API (FastAPI) — creates saga + outbox command
```python
# orchestrator_api.py
import os, json, uuid
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg

DSN = os.getenv("PG_DSN", "postgresql://postgres:postgres@localhost:5432/postgres")

app = FastAPI()

class TripRequest(BaseModel):
    user_id: str
    trip: dict  # keep minimal for demo

@app.post("/trip-bookings", status_code=202)
def create_trip(req: TripRequest):
    saga_id = uuid.uuid4()
    cmd = {
        "type": "ReserveFlightCommand",
        "saga_id": str(saga_id),
        "step": "RESERVE_FLIGHT",
        "user_id": req.user_id,
        "trip": req.trip,
    }

    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("begin;")
            cur.execute("""
              insert into sagas(saga_id, status, step) # <----save data
              values (%s, 'RUNNING', 'RESERVE_FLIGHT')
            """, (saga_id,))
            cur.execute("""
              insert into outbox(aggregate_type, aggregate_id, event_type, payload) # <----record event. save data + record event/message are transaction outbox pattern. so the another script will read the data in outbox and send message istead of using data table directly.
              values ('saga', %s, 'ReserveFlightCommand', %s::jsonb)
            """, (saga_id, json.dumps(cmd)))
            cur.execute("commit;")

    return {"saga_id": str(saga_id), "status": "RUNNING", "poll": f"/trip-bookings/{saga_id}"}

@app.get("/trip-bookings/{saga_id}")
def get_trip(saga_id: str):
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("select * from sagas where saga_id = %s::uuid", (saga_id,))
            row = cur.fetchone()
            if not row:
                return {"error": "not found"}
            cols = [d.name for d in cur.description]
            return dict(zip(cols, row))
```

```sql
-- the above python function will insert data into two tables together or rollback for nothing changes.
BEGIN;

INSERT INTO bookings (...);

INSERT INTO outbox (
  event_type,
  payload,
  status
) VALUES (
  'FlightBooked',
  '{ "booking_id": 123 }',
  'pending'
);

COMMIT;
```

Run:
```bash
pip install fastapi uvicorn psycopg[binary]
uvicorn orchestrator_api:app --reload --port 8000
```

---

# 4) Outbox publisher — sends NEW outbox rows to SQS
This is a separate process (daemon). Same pattern for orchestrator + each service.
```python
# outbox_publisher.py
import os, json, time
import psycopg
import boto3

DSN = os.getenv("PG_DSN", "postgresql://postgres:postgres@localhost:5432/postgres")
QUEUE_URL = os.getenv("SQS_QUEUE_URL")  # e.g. trip-commands.fifo
sqs = boto3.client("sqs")

def publish_loop():
    while True:
        with psycopg.connect(DSN) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                  select id, event_type, payload
                  from outbox
                  where status='NEW'
                  order by id
                  limit 20
                  for update skip locked
                """)
                rows = cur.fetchall()

                for outbox_id, event_type, payload in rows:
                    body = json.dumps(payload)

                    # FIFO recommended: dedupe by saga+step
                    dedupe = payload.get("saga_id", str(outbox_id)) + ":" + payload.get("step","")
                    sqs.send_message(
                        QueueUrl=QUEUE_URL,
                        MessageBody=body,
                        MessageGroupId=payload.get("saga_id", "default"),
                        MessageDeduplicationId=dedupe,
                    )

                    cur.execute("""
                      update outbox set status='SENT', sent_at=now() where id=%s
                    """, (outbox_id,))
                conn.commit()

        time.sleep(0.5)

if __name__ == "__main__":
    publish_loop()
```

---
# 5) Orchestrator event consumer — advance saga or compensate

This process reads from `trip-events.fifo` and drives state transitions.
```python
# orchestrator_events_consumer.py
import os, json, time, uuid
import psycopg
import boto3

DSN = os.getenv("PG_DSN", "postgresql://postgres:postgres@localhost:5432/postgres")
EVENTS_QUEUE_URL = os.getenv("SQS_EVENTS_QUEUE_URL")
sqs = boto3.client("sqs")

def next_command_for(event: dict, saga_row: dict):
    t = event["type"]
    saga_id = saga_row["saga_id"]

    # Success path
    if t == "FlightReservedEvent":
        return ("RESERVE_HOTEL", {
            "type": "ReserveHotelCommand",
            "saga_id": str(saga_id),
            "step": "RESERVE_HOTEL",
            "trip": event.get("trip") or saga_row.get("trip"),
        })

    if t == "HotelReservedEvent":
        return ("RESERVE_CAR", {
            "type": "ReserveCarCommand",
            "saga_id": str(saga_id),
            "step": "RESERVE_CAR",
        })

    if t == "CarReservedEvent":
        return ("NOTIFY", {
            "type": "SendNotificationCommand",
            "saga_id": str(saga_id),
            "step": "NOTIFY",
        })

    if t == "NotificationSentEvent":
        return ("DONE", None)

    # Failure → compensate
    if t in ("FlightReserveFailedEvent", "HotelReserveFailedEvent", "CarReserveFailedEvent"):
        return ("COMPENSATE", {"type": "StartCompensationCommand", "saga_id": str(saga_id), "step": "COMPENSATE"})

    return (None, None)

def consume_loop():
    while True:
        resp = sqs.receive_message(
            QueueUrl=EVENTS_QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10,
        )
        for msg in resp.get("Messages", []):
            event = json.loads(msg["Body"])

            saga_id = uuid.UUID(event["saga_id"])
            with psycopg.connect(DSN) as conn:
                with conn.cursor() as cur:
                    cur.execute("begin;")
                    cur.execute("select * from sagas where saga_id=%s for update", (saga_id,))
                    row = cur.fetchone()
                    if not row:
                        cur.execute("rollback;")
                        sqs.delete_message(QueueUrl=EVENTS_QUEUE_URL, ReceiptHandle=msg["ReceiptHandle"])
                        continue

                    cols = [d.name for d in cur.description]
                    saga = dict(zip(cols, row))

                    # Update saga with reservation IDs on success events
                    if event["type"] == "FlightReservedEvent":
                        cur.execute("update sagas set flight_res_id=%s, updated_at=now() where saga_id=%s",
                                    (event["reservation_id"], saga_id))
                    if event["type"] == "HotelReservedEvent":
                        cur.execute("update sagas set hotel_res_id=%s, updated_at=now() where saga_id=%s",
                                    (event["reservation_id"], saga_id))
                    if event["type"] == "CarReservedEvent":
                        cur.execute("update sagas set car_res_id=%s, updated_at=now() where saga_id=%s",
                                    (event["reservation_id"], saga_id))

                    new_step, cmd = next_command_for(event, saga)

                    if new_step == "DONE":
                        cur.execute("update sagas set status='SUCCEEDED', step='DONE', updated_at=now() where saga_id=%s",
                                    (saga_id,))
                    elif new_step == "COMPENSATE":
                        cur.execute("update sagas set status='COMPENSATING', step='COMPENSATE', updated_at=now() where saga_id=%s",
                                    (saga_id,))
                        # enqueue compensation commands (cancel in reverse order if reserved)
                        if saga.get("car_res_id"):
                            c = {"type":"CancelCarCommand","saga_id":str(saga_id),"step":"CANCEL_CAR","reservation_id":saga["car_res_id"]}
                            cur.execute("insert into outbox(aggregate_type, aggregate_id, event_type, payload) values('saga',%s,'CancelCarCommand',%s::jsonb)",
                                        (saga_id, json.dumps(c)))
                        if saga.get("hotel_res_id"):
                            c = {"type":"CancelHotelCommand","saga_id":str(saga_id),"step":"CANCEL_HOTEL","reservation_id":saga["hotel_res_id"]}
                            cur.execute("insert into outbox(aggregate_type, aggregate_id, event_type, payload) values('saga',%s,'CancelHotelCommand',%s::jsonb)",
                                        (saga_id, json.dumps(c)))
                        if saga.get("flight_res_id"):
                            c = {"type":"CancelFlightCommand","saga_id":str(saga_id),"step":"CANCEL_FLIGHT","reservation_id":saga["flight_res_id"]}
                            cur.execute("insert into outbox(aggregate_type, aggregate_id, event_type, payload) values('saga',%s,'CancelFlightCommand',%s::jsonb)",
                                        (saga_id, json.dumps(c)))
                        # optional final notify failure
                        fail_note = {"type":"SendFailureNotificationCommand","saga_id":str(saga_id),"step":"NOTIFY_FAIL"}
                        cur.execute("insert into outbox(aggregate_type, aggregate_id, event_type, payload) values('saga',%s,'SendFailureNotificationCommand',%s::jsonb)",
                                    (saga_id, json.dumps(fail_note)))

                    elif cmd:
                        cur.execute("update sagas set step=%s, updated_at=now() where saga_id=%s", (new_step, saga_id))
                        cur.execute("""
                          insert into outbox(aggregate_type, aggregate_id, event_type, payload)
                          values ('saga', %s, %s, %s::jsonb)
                        """, (saga_id, cmd["type"], json.dumps(cmd)))

                    cur.execute("commit;")

            sqs.delete_message(QueueUrl=EVENTS_QUEUE_URL, ReceiptHandle=msg["ReceiptHandle"])

        time.sleep(0.1)

if __name__ == "__main__":
    consume_loop()
```

This is intentionally “minimal”; production versions add:
- retry policies
- dead-letter queues
- dedupe on events
- timeouts (“stuck saga” detector)
    
---

# 6) A microservice worker example (Flight service)
This shows the **local transaction + local outbox** idea.
```python
# flight_service_worker.py
import os, json, time, uuid
import psycopg
import boto3

DSN = os.getenv("PG_DSN_FLIGHT", "postgresql://postgres:postgres@localhost:5432/postgres")
COMMANDS_QUEUE_URL = os.getenv("SQS_FLIGHT_COMMANDS_URL")
EVENTS_OUTBOX_DB = DSN
sqs = boto3.client("sqs")

def ensure_tables():
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("""
              create table if not exists flight_reservations (
                saga_id uuid not null,
                step text not null,
                reservation_id text not null,
                status text not null, -- RESERVED | CANCELLED
                primary key (saga_id, step)
              );
            """)
            conn.commit()

def reserve_flight(saga_id: uuid.UUID, step: str) -> str:
    # fake reservation id
    return "F-" + str(uuid.uuid4())[:8]

def consume_loop():
    ensure_tables()

    while True:
        resp = sqs.receive_message(QueueUrl=COMMANDS_QUEUE_URL, MaxNumberOfMessages=10, WaitTimeSeconds=10)
        for msg in resp.get("Messages", []):
            cmd = json.loads(msg["Body"])
            if cmd["type"] != "ReserveFlightCommand" and cmd["type"] != "CancelFlightCommand":
                sqs.delete_message(QueueUrl=COMMANDS_QUEUE_URL, ReceiptHandle=msg["ReceiptHandle"])
                continue

            saga_id = uuid.UUID(cmd["saga_id"])
            step = cmd.get("step", "")

            with psycopg.connect(DSN) as conn:
                with conn.cursor() as cur:
                    cur.execute("begin;")

                    # idempotency: (saga_id, step) unique
                    if cmd["type"] == "ReserveFlightCommand":
                        cur.execute("select reservation_id, status from flight_reservations where saga_id=%s and step=%s",
                                    (saga_id, step))
                        existing = cur.fetchone()
                        if existing:
                            res_id, status = existing
                        else:
                            # simulate availability
                            res_id = reserve_flight(saga_id, step)
                            cur.execute("""
                              insert into flight_reservations(saga_id, step, reservation_id, status)
                              values(%s,%s,%s,'RESERVED')
                            """, (saga_id, step, res_id))

                        event = {"type":"FlightReservedEvent","saga_id":str(saga_id),"step":step,"reservation_id":res_id}
                        cur.execute("insert into outbox(aggregate_type, aggregate_id, event_type, payload) values('flight',%s,'FlightReservedEvent',%s::jsonb)",
                                    (saga_id, json.dumps(event)))

                    elif cmd["type"] == "CancelFlightCommand":
                        res_id = cmd["reservation_id"]
                        # idempotent cancel
                        cur.execute("update flight_reservations set status='CANCELLED' where saga_id=%s", (saga_id,))
                        event = {"type":"FlightCancelledEvent","saga_id":str(saga_id),"step":step,"reservation_id":res_id}
                        cur.execute("insert into outbox(aggregate_type, aggregate_id, event_type, payload) values('flight',%s,'FlightCancelledEvent',%s::jsonb)",
                                    (saga_id, json.dumps(event)))

                    cur.execute("commit;")

            sqs.delete_message(QueueUrl=COMMANDS_QUEUE_URL, ReceiptHandle=msg["ReceiptHandle"])

        time.sleep(0.1)

if __name__ == "__main__":
    consume_loop()
```

You’d repeat the same skeleton for **Hotel** and **Car** (different tables + business rules + compensation commands).
Then run the same `outbox_publisher.py` for each service (pointing it at that service’s DB + events queue).

---
# 7) Why this pattern works (what it guarantees)

### ✅ No double-booking / double-cancel
Because each service uses **idempotency keys**: `(saga_id, step)` unique.

### ✅ No lost messages
Because you don’t publish directly in the request/worker transaction.  
You **write outbox row in the same DB transaction**, then publish later.

### ✅ Clear audit trail
Saga row tells you exactly where it is (and reservation IDs captured).

### ✅ Rollback is “compensation”
You’re not rolling back a distributed transaction. You run compensating actions:
- cancel car, cancel hotel, cancel flight (reverse order)
    
---

# Kafka swap (if you prefer Kafka instead of SQS)
Replace:
- `send_message()` with a Kafka producer `producer.send(topic, value=...)`
- `receive_message()` with a Kafka consumer loop

The rest stays identical:
- same **saga table**
- same **outbox**
- same “publisher reads outbox and publishes events”
- same idempotency in services

Kafka advantage: replay + consumer groups + ordering by key; SQS advantage: managed simplicity + DLQ.

# Note


# Reference

