Date: 2026-01-29
Course:
Tags: 

# Content

## Good mental model
Async: “the server will do it later”, “Asynchronous” is the behavior.
LRO: “and here’s exactly how you track it, control it, and learn the final outcome”, which is the API contract/pattern that makes async usable and reliable.

To understand and implement Long-Running Operations (LROs) effectively, it is essential to distinguish between **how you write the code** (syntax) and **how the API behaves** (semantics). This guide organizes the core concepts into a step-by-step implementation journey for developers.

---
### Step 1: Understand the Difference Between `async` and LRO
The most common point of confusion is thinking that Python's `async def` creates an LRO. It does not.

- **`async def` (Programming Model):** This is a Python implementation detail. It means your handler uses non-blocking I/O while the request is being processed to scale better.
- **LRO (API Semantics):** This is a client contract. It means the **business operation** (like creating a large database or processing a video) continues after the HTTP request has finished.
- **The Key Distinction:** An LRO can be written using either `def` or `async def`. The defining characteristic of an LRO is that it returns a **202 Accepted** status, indicating the work is started but not done.

### Step 2: Choose Your Implementation Style
There are two primary ways to design how a client tracks an operation:

- **Style A: Separate "Operation" Resource:** The API returns a link to a generic "Operation" object (e.g., `/operations/{id}`). This is a "pure" LRO style used for various background tasks.
- **Style B: Intermediate Resource State:** The resource itself is created immediately but marked with a status like **`status=CREATING`**. The client polls the resource's own URL until the status flips to `READY`.

### Step 3: Design the Durable Contract (The Database)
An LRO is only as good as its persistence. If the server restarts, the operation must not be lost. You need a database schema to track the lifecycle.

**Example Database Table (`resources`):**

```
CREATE TABLE resources (
    id UUID PRIMARY KEY,
    status TEXT NOT NULL, -- CREATING, READY, FAILED, DELETING
    spec JSONB NOT NULL,   -- Original request data
    result JSONB,         -- Final output data
    error_code TEXT,      -- For debugging failures
    idempotency_key TEXT UNIQUE, -- Prevents duplicate jobs on retry
    created_at TIMESTAMPTZ DEFAULT now()
);
```

### Step 4: Implement the API Endpoints
The API flow requires a specific handshake between the client and server.
**1. The Request (POST):** The server validates the input, inserts a "CREATING" row in the DB, and **enqueues a job** to a background worker.
- **Response:** `202 Accepted` with a `pollUrl`.

**2. The Polling (GET):** The client calls the status URL repeatedly (e.g., every 1–3 seconds) until the status is no longer "CREATING".
- **Tip:** Include a `Retry-After` header to tell the client how long to wait between polls.
**3. The Result:** Once the worker finishes, it updates the DB row to `READY` or `FAILED`. The client’s next poll will see this final state and the `result` data.

### Step 5: Background Processing (The "Heavy Work")
**Never run long work directly inside the API process** using something like `asyncio.create_task`. This is fragile because if the process restarts, the task dies. Use a **durable queue** like SQS, Celery, or Kafka.

**Code Example (FastAPI Style):**

```
@app.post("/resources", status_code=202)
def create_resource(req: CreateReq, idempotency_key: str = Header(None)):
    # 1. Check Idempotency (Safe retries)
    if idempotency_key in IDEMP_DB:
        return {"id": IDEMP_DB[idempotency_key], "status": "CREATING"}

    # 2. Create record in DB
    rid = uuid4()
    DB[rid] = {"id": rid, "status": "CREATING", "spec": req.dict()}

    # 3. Hand off to worker
    enqueue_job(rid)

    return {"id": str(rid), "status": "CREATING", "pollUrl": f"/resources/{rid}"}
```

### Step 6: When to use LRO vs. Synchronous
- **Use Synchronous (`200 OK`):** If the task is stable and takes **under 1–2 seconds**.
- **Use LRO (`202 Accepted`):** If the task might exceed **10–30 seconds** (the common timeout for load balancers and gateways).

### Summary Checklist for Developers
- **Idempotency:** Ensure that if a client retries the same request, you don't start a second background job.
- **Visibility:** The client must be able to see `PENDING`, `RUNNING`, `DONE`, or `FAILED` states.
- **Control:** Ideally, provide a way to cancel the work using `DELETE /operations/{id}`.
- **Atomicity:** Write the DB row **before** enqueuing the job to ensure you don't lose track of the work.

# Note


# Reference

