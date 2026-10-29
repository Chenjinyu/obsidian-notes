---
sr-due: 2026-10-21
sr-interval: 1
sr-ease: 2.5
---

# REST APIs — Resources, Requests, and Reliable Actions

## 1. Definition in plain language

**REST means Representational State Transfer.** It is an architectural style for building interfaces around resources, such as jobs, orders, and users. In common HTTP APIs, a client names a resource with a URL, chooses an HTTP method, and sends or receives a representation such as JSON.

For example, `GET /jobs/job-123` means “give me the current representation of this job.” `POST /jobs` means “submit a new job.”

REST is not another name for JSON or HTTP. Formal REST includes client/server separation, stateless requests, cacheability, a uniform interface, layers, and optional code-on-demand. The uniform interface includes resource identification, manipulation through representations, self-descriptive messages, and hypermedia-driven transitions. Many practical “REST APIs” implement only part of this style. The example here is a resource-oriented HTTP API, not a demonstration of every REST constraint.

**Stateless does not mean the server has no database.** It means requests carry the context needed to interpret them rather than depending on a hidden sequence of earlier interactions with a particular server instance. The resource's persistent state still exists.

## Idempotent Definition
 Per the RFC 910 specification, an HTTP method is considered idempotent if the intended effect on the server of multiple identical requests is the exact same as the effect for a single such request
## Real-world use cases

| Real-world scenario | What happens in the product | Why a REST-style HTTP API fits |
|---|---|---|
| Online shopping | A customer browses products, adds cart items, creates an order, and checks its details. | Products, carts, and orders are identifiable resources with bounded requests and responses. |
| Appointment booking | A patient views available slots, books an appointment, and later cancels it. | Availability and appointments have clear resource representations; the server validates conflicts when accepting a booking. |
| SaaS administration | An administrator lists employees, updates team membership, and disables an account. | Resource URLs and standard HTTP methods provide a straightforward interface for an admin UI and automation. |
| AI job submission | A client submits a document for summarization and receives a job ID before processing finishes. | A request can create a job resource; its result can be retrieved later without holding the submission request open. |
| Delivery tracking | A retailer retrieves a shipment's current location and estimated delivery time from a carrier API. | The caller wants a current snapshot of a known shipment, rather than a continuous conversation. |
| Media management | A creator lists videos, changes titles, and retrieves upload instructions or download links. | Metadata and media resources can be managed through a stable resource-oriented interface. |
| Personal finance dashboard | An authenticated customer retrieves account details and paginated transaction history. | Readable resource boundaries, access checks, and pagination fit a request-driven screen. |

**Walk through an online order:** the app reads `GET /products/42`, submits `POST /orders`, and receives an order ID. Later, `GET /orders/{id}` returns its current state. The server must validate price, inventory, and authorization when creating the order; a previously displayed product response is not a reservation. If the UI also needs live delivery updates, that same product can add SSE or polling beside the resource API.

**Interview practice:** explain why a product catalog needs bounded resource requests, then identify the separate requirement that would justify adding live updates.

## 2. What happens in a request?

The client sends a method, URL, headers, and sometimes a body. The server authenticates the caller, validates the request, checks authorization, performs an operation, and returns a status code, headers, and optionally a body. A normal request completes when that response body ends. The underlying HTTP connection may be reused for later requests; it does not require a new TCP connection for every request.

| Method | Typical use | Interview detail |
|---|---|---|
| GET | Read a resource | Safe and idempotent in intended semantics |
| POST | Create or submit an operation | Not inherently idempotent |
| PUT | Replace/set a resource at a known URL | Intended effect is idempotent |
| PATCH | Apply a partial update | Idempotency depends on the patch operation |
| DELETE | Remove a resource | Intended effect is idempotent; responses can differ |

Useful statuses: 200 success; 201 created; 202 accepted but not complete; 204 success without body; 400 bad request; 401 missing/invalid authentication; 403 forbidden; 404 not found; 409 conflict; 412 failed precondition; 422 validation failure in this FastAPI example; 429 rate limit; 503 temporarily unavailable.

## 3. When should I use it?

Use an HTTP API for CRUD, job submission, retrieving final results, configuration, and occasional client commands. It fits browser, mobile, and backend callers. If a job takes minutes, return a job ID rather than making a normal request wait for the whole execution.

An API does not automatically notify clients of later changes. Add polling, SSE, WebSockets, or webhooks according to the consumer's needs.

## 4. Runnable Python example

Install `fastapi`, `uvicorn`, and `httpx`. Save the following as `rest_server.py`, then run `python -m uvicorn rest_server:app --host 127.0.0.1 --port 8000`.

This local demonstration deliberately uses an in-memory dictionary and no login. Use one process. Jobs remain queued because job execution is not implemented in this example.

```python
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

app = FastAPI()
jobs = {}

class JobInput(BaseModel):
    prompt: str = Field(min_length=1, max_length=2000)

@app.post("/jobs", status_code=202)
async def create_job(data: JobInput, response: Response):
    job_id = str(uuid4())
    jobs[job_id] = {
        "id": job_id, "status": "queued", "version": 1,
        "prompt": data.prompt,
    }
    response.headers["Location"] = f"/jobs/{job_id}"
    response.headers["Cache-Control"] = "no-store"
    return {"id": job_id, "status": "queued"}

@app.get("/jobs/{job_id}")
async def get_job(job_id: str, response: Response):
    job = jobs.get(job_id)
    if job is None:
        raise HTTPException(404, "Job not found")
    response.headers["Cache-Control"] = "no-store"
    return {k: job[k] for k in ("id", "status", "version")}
```

Save this separately as `rest_client.py` and run it while the server is running:

```python
import httpx

with httpx.Client(base_url="http://127.0.0.1:8000", timeout=5) as client:
    submitted = client.post("/jobs", json={"prompt": "Explain caching"})
    submitted.raise_for_status()
    print(submitted.status_code)  # 202
    status = client.get(submitted.headers["Location"])
    status.raise_for_status()
    print(status.json())  # id, queued, version=1
```

The `httpx.Client` reuses connections. Input validation limits malformed or oversized prompts. The status response omits prompt text because it is not needed for status checks.

## 5. What supporting technologies do I need?

| Problem | Supporting mechanism | Important limit |
|---|---|---|
| Who may read this job? | Authentication plus tenant/resource authorization | Knowing a UUID is not authorization |
| POST timed out after creating the job | Idempotency key | Server must actually implement atomic deduplication |
| Slow downstream service | Timeouts and an overall deadline | A timeout does not prove the operation did not happen |
| Too many calls | Rate limiting and bounded concurrency | Caller retries need backoff and jitter |
| Minutes of work | Durable queue and workers | In-process background tasks can disappear on restart |
| Two users update a resource | Version / ETag with If-Match, checked atomically | A preliminary SELECT alone leaves a race |
| A huge resource collection | Pagination and filtering | Stable ordering matters while records change |
| Debugging production | Correlation IDs, metrics, traces | Avoid logging secrets or private request bodies |

### Idempotency is a server contract

For retriable job creation, store `(tenant_id, idempotency_key, request_hash, job_id, response)` with a unique constraint. In one transaction, create the key record and job. Same key and same payload returns the earlier outcome; same key and different payload is rejected. Concurrent requests must not create two jobs. If a queue is external, use an outbox to avoid “database committed, enqueue failed.” Set an explicit retention window; reusing an expired key may create another job.

Sending `Idempotency-Key` by itself does not make a POST safe. The minimal server above does not implement this contract.

## 6. Interview answer and recall

“I would expose a resource-oriented HTTP API for submitting and reading jobs. Long-running work would return 202 with a job URL. I would add authentication, ownership checks, idempotent submission, and durable execution. Clients could use polling or a stream for later updates.”

1. Does stateless mean there is no stored job state?
2. Why can retrying POST create duplicate jobs?
3. What does 202 promise, and what does it not promise?
4. How do REST, polling, and SSE coexist in one application?
5. Why can repeated DELETE calls be idempotent even if one returns 204 and another 404?
	1. after one call or ten calls, the end state is identical - the resource does not exist. therefore, the method is idempotent

## 7. References and next step

- [Fielding's REST definition](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)
- [HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
- [HTTPX clients](https://www.python-httpx.org/advanced/clients/)
- Next: [Polling](02-polling.md), [Retries](06-retries-backoff-jitter.md).
