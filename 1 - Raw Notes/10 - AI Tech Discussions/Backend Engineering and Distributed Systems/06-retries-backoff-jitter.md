---
sr-due: <% tp.date.now("YYYY-MM-DD", 3) %>
sr-interval: 1
sr-ease: 2.5
---

# Timeouts, Retries, Backoff, Jitter, and Retry-After

## 1. Definitions with a failure story

Your status request times out. Maybe the server is overloaded; maybe one packet was lost. Retrying immediately may succeed, but if thousands of clients do it together, they can make an outage worse.

- **Timeout:** limit how long a particular operation or I/O phase waits.
- **Deadline:** an end-to-end limit that includes attempts and waiting.
- **Retry:** another attempt at an operation after failure.
- **Backoff:** increase the wait between attempts.
- **Exponential backoff:** grow the bound exponentially, such as 1, 2, 4, 8 seconds.
- **Jitter:** randomize timing to spread synchronized callers.
- **Retry budget:** limit retry work by attempts, elapsed time, or a shared rate allowance.
- **Retry-After:** server response header giving delay seconds or an HTTP date before a follow-up request.

Full jitter chooses uniformly from zero to the current bound. Equal/delayed jitter designs use a minimum plus randomness. Select a policy for the workload; randomness is not a correctness guarantee.

## 2. Where these ideas fit

| Situation | Useful policy |
|---|---|
| GET fails transiently | Bounded retry with backoff and jitter |
| Successful poll says running | Normal adaptive polling interval |
| Server sends 429 / Retry-After | Wait at least its stated delay |
| SSE or WebSocket disconnects | Reconnect policy plus resume state |
| Webhook receiver unavailable | Sender retries according to its delivery contract |
| Many cache keys expire together | TTL jitter, a different use of randomness |

Jitter spreads work; it does not inherently reduce how many requests eventually occur. Backoff reduces retry rate. A deadline prevents endless waiting.

## 3. Decide what is safe to retry

Retry selected transient failures, such as temporary connectivity problems and a service's documented retryable statuses. Do not endlessly retry malformed input, invalid credentials, forbidden requests, or a permanently missing resource.

A timeout does not tell you whether the server applied a mutation. For POST/payment/job submission, use a real idempotency contract or check the operation's outcome. Do not infer retry safety from a client-side header alone.

Retry at a deliberate layer. If five layers each make three attempts, one operation can cause up to 3^5 = 243 deepest-layer attempts. Coordinate SDK, proxy, client, and application retry policies.

## 4. Reusable Python GET helper

Install `httpx`. Save as `retry_helpers.py`. Requires Python 3.11+. It retries only the listed network failures/statuses. The total timeout includes retry delays and complete response reads. It is designed for small JSON status responses, not indefinite event streams.

```python
import asyncio
import random
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import httpx

RETRYABLE = {429, 502, 503, 504}

def parse_retry_after(value):
    if value is None:
        return None
    value = value.strip()
    if value.isascii() and value.isdigit():
        try:
            return float(value)
        except (ValueError, OverflowError):
            return None
    try:
        when = parsedate_to_datetime(value)
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        return max(0.0, (when - datetime.now(timezone.utc)).total_seconds())
    except (ValueError, TypeError, OverflowError):
        return None

async def get_json(client, url, *, budget=15, max_attempts=4):
    if budget <= 0 or max_attempts < 1:
        raise ValueError("Budget and attempts must be positive")

    async with asyncio.timeout(budget):
        for attempt in range(max_attempts):
            server_delay = None
            try:
                response = await client.get(url, timeout=5)
            except (httpx.TimeoutException, httpx.NetworkError):
                if attempt == max_attempts - 1:
                    raise
            else:
                if response.status_code not in RETRYABLE:
                    response.raise_for_status()
                    return response.json()
                if attempt == max_attempts - 1:
                    response.raise_for_status()
                server_delay = parse_retry_after(
                    response.headers.get("Retry-After")
                )

            bound = min(8.0, 0.5 * 2 ** attempt)
            delay = random.uniform(0, bound)
            if server_delay is not None:
                delay = max(delay, server_delay) + random.uniform(0, 0.2)
            # The overall timeout stops us if this wait exceeds the budget.
            # We never shorten Retry-After just to squeeze in another attempt.
            await asyncio.sleep(delay)
```

An HTTPX timeout normally governs phases such as connect/read/write/pool waits; it is not necessarily a total wall-clock deadline for every possible response. The outer asyncio timeout supplies the overall limit. Reuse one AsyncClient instead of creating a new connection pool on each retry. Cancellation must propagate; do not catch and suppress it broadly.

## 5. Try it without a real server

Run this in a separate file beside `retry_helpers.py`:

```python
import asyncio
import httpx
from retry_helpers import get_json

attempts = 0

def fake_server(request):
    global attempts
    attempts += 1
    if attempts < 3:
        return httpx.Response(503, headers={"Retry-After": "0"})
    return httpx.Response(200, json={"status": "completed"})

async def main():
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(fake_server)
    ) as client:
        print(await get_json(client, "https://demo.invalid/jobs/123"))
        print("Attempts:", attempts)

if __name__ == "__main__":
    asyncio.run(main())
```

Expected: completed after three attempts. The mock transport does not make an external network call. Change the handler to return 400: the helper should stop on the first attempt. Return a very large Retry-After: the overall deadline should expire instead of sending an early retry.

## 6. Supporting tools and trade-offs

**Circuit breaker:** stop calling a failing dependency for a period, then allow limited probes. It complements retries; it does not repair the dependency. **Bulkhead/concurrency limit:** cap simultaneous work so a slow dependency does not consume all resources. **Load shedding:** reject excess work deliberately to preserve service for the rest.

For streamed connections, a quiet stream is not automatically broken. Align read timeouts with expected heartbeats. A reconnect restores transport; cursor replay, resubscription, and deduplication restore application continuity.

Track attempts per original request, final success rate, latency including waits, server 429s, deadline expirations, and retry QPS. An apparent increase in success can hide exploding load and latency.

## 7. Interview answer and recall

“I would retry only transient failures and safe or idempotent operations. I would use exponential backoff with jitter, honor Retry-After, and bound both attempts and total duration. I would also check for retries at other layers to avoid multiplying traffic.”

1. Why does backoff without jitter still create synchronized spikes?
2. Does a timeout prove a payment was not processed?
3. Why is Retry-After a minimum wait rather than a randomization bound?
4. How is a read timeout different from an overall deadline?
5. When would a circuit breaker help more than additional retries?

References: [AWS timeouts and retry design](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/), [Retry-After semantics](https://www.rfc-editor.org/rfc/rfc9110.html#name-retry-after), [HTTPX timeouts](https://www.python-httpx.org/advanced/timeouts/).
