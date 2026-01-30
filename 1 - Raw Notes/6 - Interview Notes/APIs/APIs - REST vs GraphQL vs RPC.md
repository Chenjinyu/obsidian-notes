Date: 2026-01-29
Course:
Tags: [[API]] [[interview]]

# Content

Other than REST APIs, there are other popular APIs, such as Remote Procedure Call ([RPC](https://en.wikipedia.org/wiki/Remote_procedure_call)), [GraphQL](https://graphql.org/), and Simple Access Protocol ([SOAP](https://en.wikipedia.org/wiki/SOAP)):
# RPC
A requester selects a remote procedure to execute, serializes the parameters, and then sends the lightweight binary data to the server. The server decodes the message and executes the operation, sending the result back to the requester.
Its simplicity and light payloads have made it a de facto standard for many inter-service data exchanges on the backend.

# GraphQL
GraphQL was developed to allow clients to execute precise queries and retrieve only the data they are interested in, typically from a graph database.
To achieve this process, servers need to predefine a schema that describes all possible queries and their return types. This reduces the server payload and offers the client a great amount of flexibility during query time.
However, performance can suffer when the client has too many nested fields in one request. Additionally, there is a steep learning curve that requires extensive knowledge.

Therefore, GraphQL users need to find a balance between its benefits and implementation costs.

# SOAP
A precursor to REST. SOAP works like an envelope that contains a bulky, text-based message. It is much slower than binary messaging protocols, such as RPC.
However, the standardized text format and security features make enforcing legal contracts and authentication easy throughout the API's processing.
SOAP is a legacy protocol and is still heavily used in high-security data transmission scenarios, such as billing operations, booking, and payment systems.

# Long-running Operations
A **long-running operation (LRO)** is just a pattern for handling API requests that **can’t finish within a normal request/response window** (seconds) because the work is slow, heavy, or queued (delete big data, rebuild index, export report, ML training, etc.). Instead of holding the connection open, the server **acknowledges** the request and gives the client an **operation handle** to poll (or subscribe) for progress/results.

# What “long-running” means in APIs (**LRO almost always means the operation is (or behaves like) asynchronous**.)

Typical characteristics:

* Work may take **seconds → minutes → hours**
* Might be **asynchronous** (queued / background job)
* Needs **progress**, **retry**, **cancellation**, **idempotency**, and **result retrieval**
## Core LRO building blocks (common pattern)

1. Client calls an endpoint to start work
2. Server returns **202 Accepted** (often) with:

   * an **operation ID**
   * a way to check status (URL or token)
3. Client checks operation status later
4. When done, operation returns:

   * success + result, or
   * failure + error details

### REST example (common)

**Request**
`DELETE /resources/123`

**Response**
`202 Accepted`

```json
{
  "operationId": "op_9f3c",
  "status": "PENDING",
  "statusUrl": "/operations/op_9f3c"
}
```

**Poll**
`GET /operations/op_9f3c`

**Status response**

```json
{
  "operationId": "op_9f3c",
  "status": "RUNNING",
  "progress": 42
}
```

**Done**

```json
{
  "operationId": "op_9f3c",
  "status": "DONE",
  "result": { "deletedResourceId": "123" }
}
```

Alternative to polling: server pushes updates via **webhooks**, **SSE**, or **WebSocket**.

---

## Does LRO apply to REST, RPC, SOAP, GraphQL?

Yes. **LRO is transport/style-agnostic**. It’s not “a REST thing.” It’s a design solution for async work.

### 1) REST

Very common:

* `202 Accepted` + `Location` header to status URL
* Or return an “operation resource” in body
* Often paired with **Retry-After** header for poll interval

### 2) RPC (gRPC / protobuf-style)

Also common:

* Return an operation handle (e.g., `Operation { name, done, error, response }`)
* Client polls `GetOperation(name)` or uses streaming callbacks/events

### 3) SOAP

Also possible:

* “SubmitJob” returns a job ID
* “GetJobStatus(jobId)” returns status/progress
* “GetJobResult(jobId)” fetches output

### 4) GraphQL

Also common, despite GraphQL being “single endpoint”:

* Mutation returns a `jobId` / `operationId`
* Query `operation(id)` to check status
* Or use GraphQL **subscriptions** for push updates

Example pattern:

```graphql
mutation {
  deleteBigThing(id:"123") { operationId }
}
```

Then:

```graphql
query {
  operation(id:"op_9f3c") { status progress result error }
}
```

---
## When should an API use LRO vs synchronous response?

Use **LRO** when:

* deletion/creation takes “noticeable time” (often > a few seconds)
* work is queued or depends on other services
* you want reliability across retries/timeouts
* you need progress + cancel + audit trail

Stay **synchronous** (200/204) when:

* operation is quick and deterministic
* the resource is truly removed immediately

---
## Important nuances (especially for DELETE)

* “Delete requested” vs “deleted”: with LRO you’re acknowledging the request, not promising it’s already gone.
* After completion, `GET /resource/123` may return:

  * `404 Not Found` (gone)
  * or `410 Gone` (explicitly gone)
  * or if “soft delete,” it may still exist but hidden.

Also consider **idempotency**:

* Multiple DELETEs should not create multiple background jobs; typically return the same operation or a safe response.


# Note


# Reference

