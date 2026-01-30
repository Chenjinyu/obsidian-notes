Date: 2026-01-30
Course: https://www.youtube.com/watch?v=d2z78guUR4g(Youtube), https://www.tryexponent.com/courses/system-design-interviews/reliability-strategies(Exponent)
Tags: [[API]] [[interview]]

# Content


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

## 2) Choreography (event-driven chain)
Services emit events and react to events:
* FlightReserved → Hotel service tries to reserve
* HotelReserved → Car service tries to reserve
* CarReserved → Notification sends

If something fails, services emit “Failed” events and others compensate.
**Downside:** logic gets scattered; debugging becomes “event spaghetti” unless you’re very disciplined.

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

# Note


# Reference

