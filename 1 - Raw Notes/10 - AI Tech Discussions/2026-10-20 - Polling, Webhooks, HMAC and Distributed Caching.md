---
sr-due: <% tp.date.now("YYYY-MM-DD", 3) %>
sr-interval: 1
sr-ease: 2.5
---
# Polling, Webhooks, HMAC, and Distributed Caching — Interview Notes

Discussion date: 2026-10-20 (America/Chicago).
Purpose: turn JC's questions and points of uncertainty into definitions, examples, interview answers, and active-recall practice.

Expanded on 2026-10-21: [start with the learning map](00-learning-map.md). Separate guides now cover REST APIs, polling, SSE, WebSockets, webhooks, retry strategies, HMAC/encoding, and caching. Each explains the definition, use cases, Python implementation, supporting techniques, and interview follow-ups.

The frontmatter above intentionally preserves the requested Templater expression literally. GitHub does not execute it; until evaluated in Obsidian, sr-due is a template string, not an actual due date.

## 1. My questions and what needed clarification

Questions below are lightly edited for readability, preserving their meaning.

| Question I asked | Concept I needed to clarify | Key correction |
|---|---|---|
| What should I know about polling and webhooks for interviews? | Pull versus event-driven notification; failure handling | A communication choice must include delivery, security, and reliability trade-offs. |
| What are jitter and HMAC? Can I see Python examples? | Retry timing versus message authentication | Jitter spreads requests; HMAC authenticates bytes using a shared secret. |
| Why encode the body as UTF-8 and timestamp as ASCII? Does HMAC only deal with bytes? | Text versus bytes | HMAC operates on bytes. ASCII digits have the same bytes in UTF-8. |
| Why add b"."? | Bytes literals and message framing | The dot separates fields; HMAC itself does not require or interpret it. |
| ASCII supports 128 characters; UTF-8 supports more? | Character encodings | ASCII has 128 codes; UTF-8 encodes Unicode with 1–4 bytes per code point. |
| Why does adaptive polling reduce requests? | Poll interval versus request count | Polling does not inherently reduce traffic; longer intervals do. |
| What is Retry-After? | Server-directed retry delay | A response header containing delay seconds or an HTTP date. |
| Can we use small queries, indexes, and read replicas? | Read-path optimization | Yes, but they solve different problems and replicas can lag. |
| How can status be cached if it changes frequently? | Freshness versus reuse | Short-lived cached values are useful if read often enough; status may change less often than progress. |
| What is a good cache strategy? | Cache-aside, TTL, invalidation | Start from load and freshness requirements, not "always add Redis." |
| How do we identify acceptable staleness? | Business freshness requirement | Ask about the consequence and allowed visibility delay; budget all delay sources. |
| What does revalidating authoritative state look like in code? | Correctness and check-then-act races | Use an atomic conditional transition, not an unprotected read followed by a write. |
| What does coalescing concurrent loads mean? | Cache stampede | One loader fetches a missing key; concurrent callers share or reuse the result. |
| How do multiple services coordinate caching? Is it an interview topic? | Process boundaries and ownership | Local locks do not coordinate servers; shared caches still need miss coordination when justified. |

## 2. Polling, webhooks, SSE, and WebSockets

**Polling (輪詢):** the client repeatedly asks for current state.
**Webhook:** a service sends an HTTP request to a registered backend endpoint when an event happens.
**Long polling:** the server holds a request until there is an update or a timeout; the client reconnects.
**SSE (Server-Sent Events):** a web technology that lets a server push real-time updates or a continuing stream of text to a browser or another client over a single, long-lived HTTP response. The client connects once, and the server keeps sending new events through that response as information becomes available. This is useful for one-way streams such as sports scores, stock-price displays, job-status updates, and AI-generated text appearing piece by piece. The client can send commands through separate HTTP requests. Connections can break or finish, so production designs also need reconnection, heartbeats, and retained events if missed updates must be replayed. See [the complete SSE guide](03-server-sent-events.md) for the workflow, wire format, Python server/client examples, and reliability design.
**WebSocket:** a persistent connection supporting bidirectional messages.

| Mechanism | Good fit | Main trade-off |
|---|---|---|
| Short polling | Simple async job-status checks | Repeated requests and discovery latency |
| Long polling | Updates without frequent empty immediate responses | Open requests and reconnect management |
| Webhook | Backend notification of batch completion | Retries, duplicates, signature verification |
| SSE | Browser progress and streamed output | Reconnection and event recovery |
| WebSocket | Interactive bidirectional communication | Connection lifecycle and scaling |

Example API:
- POST /jobs returns 202 Accepted and a job ID.
- GET /jobs/{id} returns queued, running, completed, failed, or cancelled.
- Stop polling terminal states and enforce an overall deadline.
- An async task, including an MCP-related task, does not inherently require polling; use the capabilities the API actually exposes.
- Polling can serve live displays when a few seconds of delay is acceptable.
- A webhook normally cannot call a browser tab directly. It calls your backend; the browser then gets updates through polling, SSE, or WebSockets.

### Webhook reliability checklist

1. Verify the provider's signature against the raw body.
2. Validate event structure and signed timestamp.
3. Durably accept the event before acknowledging success.
4. Process asynchronously when work is expensive.
5. Deduplicate event IDs and make effects idempotent.
6. Expect retries and potentially out-of-order events.
7. Retry processing failures; retain exhausted failures for investigation/replay.
8. Reconcile with authoritative state when missed notifications matter.

**Idempotency:** repeated execution has the same intended business effect as one execution. An event ID check and its business effect need atomic coordination; a separate unsafe "check then insert" is insufficient.
**Dead-letter queue:** a destination for events that exhausted normal processing retries.
Webhook delivery guarantees depend on the provider; HTTP callbacks alone do not guarantee delivery.

**Interview answer:** "Polling is simple and client-driven, but trades request volume for detection latency. Webhooks reduce empty checks but require authentication, durable acceptance, retries, and idempotent processing."

## 3. Adaptive polling, backoff, jitter, and Retry-After

**Adaptive polling:** adjust normal check frequency based on expected duration, unchanged status, load, or server guidance.
**Backoff:** increase the delay between retry attempts after transient failures.
**Jitter:** add randomness to timing to avoid synchronized requests.
**Thundering herd:** many clients simultaneously create a burst of work.

For a five-minute job:
- Every second: approximately 300 checks.
- Every ten seconds: approximately 30 checks.
- Longer intervals reduce traffic but delay discovery.
- For a fixed interval and uniformly timed changes, average discovery delay is approximately half the interval.

10,000 active clients polling every five seconds produce about 2,000 requests/second.

### Python: exponential backoff with full jitter

```python
import random
import time

def call_with_retry(operation, max_attempts=5):
    for attempt in range(max_attempts):
        try:
            return operation()
        except (TimeoutError, ConnectionError):
            if attempt == max_attempts - 1:
                raise
            bound = min(30.0, 1.0 * 2 ** attempt)
            time.sleep(random.uniform(0, bound))
```

The HTTP client may have its own exception types. Retry transient failures, not every error. Retried mutations need idempotency. Use asyncio.sleep in async code.

### Retry-After

Examples:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 30
```

Wait at least 30 seconds. A 503 may also include this header. A value can instead be an HTTP date.

```python
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

def retry_after_seconds(value):
    if value is None:
        return None
    value = value.strip()
    if value.isdigit():
        return float(value)
    try:
        target = parsedate_to_datetime(value)
        if target.tzinfo is None:
            target = target.replace(tzinfo=timezone.utc)
        return max(0.0, (target - datetime.now(timezone.utc)).total_seconds())
    except (ValueError, TypeError, OverflowError):
        return None
```

Combine a parsed delay with jittered backoff using max(backoff_delay, retry_after_delay). Optional additional positive jitter can spread clients further. Do not randomize below the server's minimum. Stop if the wait exceeds the request's overall deadline.

### Python: normal adaptive polling

This illustrates successful status checks; the supplied fetch function should handle network failures, rate limits, authorization, and per-request timeouts.

```python
import random
import time

def poll_until_done(fetch_status, timeout_seconds=300):
    deadline = time.monotonic() + timeout_seconds
    interval = 1.0

    while time.monotonic() < deadline:
        # Adapter must respect this remaining timeout.
        remaining = deadline - time.monotonic()
        result = fetch_status(timeout_seconds=min(5, remaining))
        if result["status"] in {"completed", "failed", "cancelled"}:
            return result
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        time.sleep(min(random.uniform(interval * 0.8, interval), remaining))
        interval = min(10.0, interval * 1.5)

    raise TimeoutError("Polling deadline exceeded")
```

## 4. HMAC, UTF-8, ASCII, and bytes

**HMAC:** Hash-based Message Authentication Code. A shared secret and message bytes produce an authentication tag. It authenticates possession of the secret and detects message changes.
**Encoding:** representing text as bytes. It is not encryption.
**ASCII:** 128 character codes, including digits, English letters, punctuation, and controls.
**UTF-8:** encoding for Unicode; 1–4 bytes per code point. A visible character may contain multiple code points.
**Bytes literal:** b"." represents the dot as bytes.

```python
assert "123".encode("ascii") == "123".encode("utf-8")
assert ".".encode("utf-8") == b"."

body = '{"message":"你好"}'.encode("utf-8")
timestamp = "1792512000"
signed_message = timestamp.encode("ascii") + b"." + body
```

The timestamp could also use UTF-8: digits encode identically. The dot is a chosen delimiter, not an HMAC requirement. Without framing, b"12" + b"345" and b"123" + b"45" both produce b"12345".

Signing the timestamp prevents someone from attaching a fresh timestamp to an old signed body. A freshness check limits replay age; event deduplication is still needed inside that window.

### Python: sign and verify

```python
import hashlib
import hmac
import json
import time

# Demo only: use a securely provisioned secret in production.
secret = b"demo-shared-secret"
body = json.dumps(
    {"event_id": "evt-456", "job_id": "job-123"},
    separators=(",", ":"),
).encode("utf-8")
timestamp = str(int(time.time()))

def sign(secret, timestamp, body):
    message = timestamp.encode("ascii") + b"." + body
    return hmac.new(secret, message, hashlib.sha256).hexdigest()

def verify(secret, timestamp, body, received_signature, tolerance=300):
    try:
        if abs(time.time() - int(timestamp)) > tolerance:
            return False
        expected = sign(secret, timestamp, body)
        return hmac.compare_digest(expected, received_signature)
    except (ValueError, TypeError, UnicodeError):
        return False

signature = sign(secret, timestamp, body)
assert verify(secret, timestamp, body, signature)
assert not verify(secret, timestamp, body + b" ", signature)
```

Send the exact signed bytes, for example requests.post(url, data=body, headers=headers, timeout=10). Receive raw HTTP body bytes directly; do not parse and reserialize before verification. JSON whitespace and property ordering can change bytes without changing semantic meaning.

**Interview essentials:** HMAC is not encryption; use HTTPS. Use constant-time comparison, signed freshness information, secret management, and event deduplication. Follow the provider's precise format rather than assuming this illustrative protocol.

## 5. Database reads and cache strategy

| Technique | Main benefit | Limitation |
|---|---|---|
| Adaptive polling | Fewer API requests | More discovery delay |
| Small indexed query | Less work per database read | High volume still costs resources |
| Read replicas | Shift reads from primary | Replication lag |
| Shared cache | Avoid repeated database reads | Staleness, invalidation, cache failures |

JC already identified selecting minimal fields, indexes, and read replicas. These are valid starting points.

**Cache hit:** requested value is present and usable.
**Cache miss:** no usable cached value.
**Cache-aside:** application checks cache, loads from database on miss, then populates cache.
**TTL:** time-to-live; how long a cached entry may remain usable.
**Expiration:** TTL elapses.
**Invalidation:** deliberately remove or mark an entry stale.
**Eviction:** remove an entry, often to free memory.
**Hit ratio:** hits divided by total cache lookups.

Status may change only a few times while progress changes every second. A cache can store a short-lived snapshot.

Illustrative policy:
- Active job: 1–2 second TTL if freshness allows.
- Immutable terminal status: longer TTL.
- Include tenant, job, and where needed attempt IDs in the key.
- Authorize access even when a response comes from cache.
- Do not cache expiring signed result URLs as though they were permanent.
- If one client polls every five seconds and TTL is two seconds, cache-aside may miss every time: caching adds little value.
- Worker-published cache updates can support a different read pattern.

After a database commit, refresh or invalidate the cache. A failure between the database write and cache operation can leave stale data. TTL limits ordinary cache residence but does not eliminate concurrent stale-fill races.

For stronger propagation, consider:
- **Transactional outbox:** commit an event alongside the business update in the same database transaction; a relay publishes it.
- **CDC:** capture committed database changes and propagate them.
- **Version-aware updates:** atomically reject an older version when a newer version is already present.

These mechanisms still require handling duplicates, ordering, and recovery. They do not automatically provide strong cache consistency.

## 6. Acceptable staleness and freshness budgets

**Acceptable staleness:** how far behind authoritative changes a consumer may be without unacceptable consequences.

Ask:
1. Is the consumer a person or an automated service?
2. What happens if it sees old information?
3. How quickly must a change become visible?
4. Do completion, failure, and progress have different requirements?

Illustrative requirement: "99% of completions are visible to active clients within five seconds."

Budget end-to-end delay:
- Publication plus replica lag: 0.5 seconds.
- Cache staleness: 1 second.
- Next polling opportunity: 3 seconds.
- Network and rendering: 0.5 seconds.

A five-second freshness requirement does not justify both a five-second TTL and five-second polling interval. Their delays can combine.

TTL starts when a value is cached, not when the source last changed. Reading from a stale replica or delayed loader may produce older data. Measure commit-to-observation delay using versions and timestamps; percentile targets are not hard worst-case guarantees.

## 7. Cached display versus critical actions

**Authoritative state:** the system of record used to decide whether a business operation is valid.
**Check-then-act race:** state changes between a check and its subsequent action.
**Atomic conditional update:** check the required current state and perform the transition in one database operation.

Example: cancellation is allowed only while queued. The UI can show stale queued status, but the server must not cancel a job that has started.

```sql
UPDATE jobs
SET status = 'cancelled',
    version = version + 1
WHERE tenant_id = :tenant_id
  AND job_id = :job_id
  AND status = 'queued'
RETURNING job_id, status, version;
```

The worker must also claim the job conditionally from queued to running. If the transition returns no row, handle not found, already cancelled, or incompatible current status appropriately.

Illustrative Python using an application-specific database adapter:

```python
def cancel_job(db, tenant_id, job_id, invalidate_best_effort):
    # Authentication and authorization happen before this function.
    with db.transaction() as tx:
        updated = tx.fetch_one(
            """UPDATE jobs
               SET status = 'cancelled', version = version + 1
               WHERE tenant_id = :tenant_id
                 AND job_id = :job_id AND status = 'queued'
               RETURNING job_id, status, version""",
            {"tenant_id": tenant_id, "job_id": job_id},
        )
    if updated is None:
        return {"error": "Job is not cancellable"}, 409

    # Failure here must not imply the committed cancellation was undone.
    invalidate_best_effort(tenant_id, job_id)
    return updated, 200
```

A fresh SELECT alone does not solve the race. Use conditional writes or suitable transactional locking. External effects such as payments additionally need idempotency and reliable execution.

**Interview answer:** "The UI can tolerate slightly stale status, but I enforce state transitions atomically against the authoritative database."

## 8. Cache stampedes and local coalescing

**Cache stampede:** concurrent misses trigger many loads of the same missing/expired value.
**Coalescing / single-flight:** one in-flight load serves concurrent requests for that key.
**Hot key:** one key receives a disproportionate share of traffic.
**Stale-while-revalidate:** return an allowed stale value while one worker refreshes it.

A local per-key lock followed by a second cache check prevents redundant successful loads within one process. A stronger single-flight example shares the current load's result or exception:

```python
from concurrent.futures import Future
import threading

class SingleFlight:
    def __init__(self):
        self.guard = threading.Lock()
        self.inflight = {}

    def run(self, key, load):
        with self.guard:
            future = self.inflight.get(key)
            leader = future is None
            if leader:
                future = Future()
                self.inflight[key] = future

        if not leader:
            return future.result(timeout=3)

        try:
            value = load()  # Must enforce its own I/O timeout.
            future.set_result(value)
            return value
        except BaseException as exc:
            future.set_exception(exc)
            raise
        finally:
            with self.guard:
                if self.inflight.get(key) is future:
                    del self.inflight[key]

# Application-specific adapters:
def get_status(key, cache, database, flights):
    cached = cache.get(key)
    if cached is not None:
        return cached

    def load():
        # Double-check after winning the in-flight slot.
        cached = cache.get(key)
        if cached is not None:
            return cached
        value = database.load_status(key)
        cache.set(key, value, ttl_seconds=2)
        return value

    return flights.run(key, load)
```

This is synchronous, process-local teaching code. Bound concurrent distinct loads and apply backend timeouts in production. A timed-out follower does not cancel the leader. A failed load can be attempted again by later requests; error cooldowns may help.

## 9. Multiple instances and distributed coordination

A shared Redis cache lets all instances reuse data, but all can still miss together.

Distributed miss coordination:
1. Check shared cache.
2. Try a per-key lock.
3. Winner double-checks cache and loads.
4. Others wait briefly with jitter and recheck.
5. Winner caches the result and safely releases the lock.

Redis-style lock acquisition:

```python
token = uuid.uuid4().hex
acquired = redis.set(lock_key, token, nx=True, px=2000)
```

- NX means set only when the key is absent.
- PX sets a lease in milliseconds.
- A lease prevents permanent blocking if the holder crashes.
- A random owner token identifies this acquisition, not just the machine.

Ownership-safe release must be atomic:

```lua
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
else
    return 0
end
```

### Why not simply delete the lock?

A's lease expires, B acquires a new lease, then A finishes. An unconditional delete would remove B's lock.

### Limitations that matter in interviews

- Lease expiry can allow two loaders. Redis failover can also weaken mutual exclusion assumptions.
- Safe release does not stop an expired holder from writing stale cache data.
- Conditional publication while the lease is still owned can reject late publishers; version-aware writes may also be required.
- Versions need atomic comparison and careful invalidation/tombstone design: deleting all version evidence can allow an old loader to repopulate.
- Cache-load locks reduce duplicate work; they are not the authority for critical business correctness.
- Bound waiting. Do not let every waiter fall back to the database simultaneously after timeout.
- On cache outage, use bounded database fallback, concurrency limits, allowed stale responses, or load shedding.

### Do we always need a distributed lock?

No. Cheap indexed reads and modest traffic may tolerate one load per process. Use distributed coordination when repeated expensive misses create meaningful pressure.

TTL jitter spreads expirations of different keys. It does not by itself coalesce simultaneous loads of one hot key.

### Different services versus instances

Instances of Jobs can share its cache. Jobs, Billing, and Notifications need clear ownership:
- Jobs owns job state.
- Others call its API or consume its events.
- Separate cached projections need freshness, versioning, and recovery rules.
- Shared Redis infrastructure does not imply that every service should write every key.

## 10. Interview follow-up map

| If I propose... | Expect the follow-up... | Answer focus |
|---|---|---|
| Polling | How often? How much traffic? | QPS estimate, delay, deadline, adaptive intervals |
| Webhooks | What if delivery fails or repeats? | Durable acceptance, retries, idempotency |
| HMAC | What exactly is signed? | Raw bytes, signed timestamp, shared secret |
| Caching | Why is it useful here? | Reuse, hit ratio, database load, staleness |
| TTL | How was it chosen? | Business requirement and end-to-end budget |
| Invalidation | What about concurrent stale fills? | Races, versions, acceptable consistency |
| Read replicas | Can I trust the latest state? | Lag; authoritative critical-action path |
| Local locks | What about multiple servers? | Shared cache, distributed miss coordination |
| Distributed locks | What if the holder crashes or pauses? | Lease, owner token, late writers, bounded waits |
| Redis fallback | Could the database survive? | Rate/concurrency limits, stale reads, shedding |

## 11. Active-recall interview practice

Answer aloud before reading earlier sections. Use: definition → example → trade-off → mitigation.

1. Explain polling versus webhooks in 60 seconds.
2. A job takes five minutes. How do you choose the polling interval?
3. What is the difference between adaptive polling, backoff, and jitter?
4. A server returns Retry-After: 30. How should your retry code behave?
5. Explain why HMAC needs bytes and why the timestamp can use either ASCII or UTF-8.
6. What does b"." do? Is it required by HMAC?
7. Why do valid signatures not eliminate duplicate webhook events?
8. When does caching job status provide little benefit?
9. How would you choose a TTL for a five-second freshness target?
10. Why is a fresh database SELECT not enough before cancelling a job?
11. Explain cache stampede and implement per-key coalescing.
12. Why does threading.Lock not coordinate multiple containers?
13. Why does a Redis lock need an owner token and a lease?
14. What can still go wrong after implementing safe lock release?
15. What should happen when Redis is unavailable?
16. How should different services share job-status information?

### Short model answer: distributed caching

"I would first measure repeated reads and define acceptable staleness. A shared cache lets service instances reuse status. For expensive concurrent misses, I would coalesce loads and use distributed coordination if process-local coordination is insufficient. Locks need leases and ownership-safe release, but critical business transitions remain atomic in the database."

### Review priorities from this conversation

- First: bytes versus strings; HMAC versus encryption; delimiter versus cryptographic requirement.
- Next: adaptive polling versus error backoff; Retry-After.
- Next: freshness budgets, TTL limits, and whether a cache will actually get hits.
- Then: atomic state transitions, local coalescing, and distributed leases.
- Revisit with changed scenarios; understanding is demonstrated by explaining trade-offs, not memorizing Redis syntax.

## 12. Reference links

Further reading; examples above are educational patterns, not production-ready drop-in implementations.

- [HTTP semantics: Retry-After](https://www.rfc-editor.org/rfc/rfc9110.html#name-retry-after)
- [AWS Builders' Library: caching challenges and strategies](https://aws.amazon.com/builders-library/caching-challenges-and-strategies/)
