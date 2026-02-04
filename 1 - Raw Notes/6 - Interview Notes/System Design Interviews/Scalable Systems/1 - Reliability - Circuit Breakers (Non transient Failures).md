Date: 2026-02-03
Course:
Tags: 

# Content

## Examples
✗ Service crashed/dead
✗ Database is down
✗ Invalid credentials/authentication
✗ Bug causing service to always return 500
✗ Dependency service deployed with breaking changes
✗ Hardware failure
✗ Configuration error
✗ Code bug (null pointer, etc.)

### Circuit Breaker example
```python
# Stop calling failed service, provide fallback
@circuit_breaker(
    failure_threshold=5,
    timeout=60
)
def call_payment_service():
    try:
        return payment_api.charge(amount)
    except CircuitOpen:
        # Use fallback: queue for later processing
        return queue_payment_for_retry()
```

**Interview insight**: "Circuit breakers are for non-transient failures. For transient failures, we use retry logic. Using circuit breaker for transient failures would cause unnecessary service degradation. Using retry for non-transient failures wastes resources and increases latency."

## 3. Circuit Breaker States

```
┌────────────────────────────────────────────────────┐
│                                                    │
│    ┌────────┐  Failure threshold  ┌──────┐         │
│    │        │    exceeded         │      │         │
│    │ CLOSED ├────────────────────→│ OPEN │         │
│    │        │                     │      │         │
│    └───▲────┘                     └───┬──┘         │
│        │                              │            │
│        │                              │            │
│        │                              │            │
│        │ Success                  Timeout          │
│        │ threshold                expires          │
│        │ met                          │            │
│        │                              │            │
│        │                              ▼            │
│        │                          ┌─────────┐      │
│        │                          │  HALF   │      │
│        └──────────────────────────┤  OPEN   │      │
│                                   └────┬────┘      │
│                                        │           │
│                                        │           │
│                         Failure        │           │
│                        threshold       │           │
│                        exceeded        │           │
│                           └────────────┘           │
│                              (back to OPEN)        │
└────────────────────────────────────────────────────┘
```

### State 1: CLOSED (Normal Operation)

**Behavior:** Requests pass through normally

python
```python
State: CLOSED
Failure count: 0/5

Request 1 → Success → failure_count = 0
Request 2 → Success → failure_count = 0
Request 3 → Failure → failure_count = 1
Request 4 → Success → failure_count = 0 (reset on success)
Request 5 → Failure → failure_count = 1
```

**Characteristics:**
- All requests are attempted
- Failures are counted
- Success resets failure count (or uses sliding window)
- Stays CLOSED until threshold exceeded

### State 2: OPEN (Blocking Requests)
**Behavior:** All requests fail immediately without calling service

python
```python
State: OPEN (since 14:32:00)
Timeout: 60 seconds
Current time: 14:32:30

Request 1 → IMMEDIATE FAIL (CircuitOpenException)
Request 2 → IMMEDIATE FAIL (CircuitOpenException)
Request 3 → IMMEDIATE FAIL (CircuitOpenException)

# Fast fail in ~1ms instead of waiting 30s for timeout
```

**Characteristics:**
- No requests to downstream service
- Fails fast (microseconds instead of seconds)
- Protects downstream service from overload
- Prevents resource exhaustion (threads, connections)
- After timeout period → transitions to HALF_OPEN
### State 3: HALF_OPEN (Testing Recovery)
**Behavior:** Allow limited requests to test if service recovered

python
```python
State: HALF_OPEN
Test requests allowed: 3

Request 1 → SUCCESS ✓ (1/3 successes needed)
Request 2 → SUCCESS ✓ (2/3 successes needed)
Request 3 → SUCCESS ✓ (3/3 successes needed)

→ Circuit transitions to CLOSED

# OR if failures:

Request 1 → SUCCESS ✓ (1/3 needed)
Request 2 → FAILURE ✗

→ Circuit immediately back to OPEN
```

**Characteristics:**
- Only limited number of requests allowed through
- Acts as "health check"
- All successes → CLOSED
- Any failure → back to OPEN
- Other requests (beyond test limit) still fail fast
# Note


# Reference

