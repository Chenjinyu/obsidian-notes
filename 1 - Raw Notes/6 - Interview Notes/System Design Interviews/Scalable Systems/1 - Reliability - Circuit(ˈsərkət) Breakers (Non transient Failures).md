Course:
Tags:  [[interview]] [[System Design]] [[High Level ]] [[Low Level]]

# Content

## Examples
- Service crashed/dead
- Database is down
- Invalid credentials/authentication
- Bug causing service to always return 500
- Dependency service deployed with breaking changes
- Hardware failure
- Configuration error

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
- **Acts as "health check"**
- All successes → CLOSED
- Any failure → back to OPEN
- Other requests (beyond test limit) still fail fast
## 4. Complete Implementation
Basic Circuit Breaker
```python
from enum import Enum
from datetime import datetime, timedelta
from threading import Lock
import time

class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class CircuitBreakerOpenError(Exception):
    """Raised when circuit is open"""
    pass

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold=5,      # Open after 5 failures
        timeout_seconds=60,       # Stay open for 60s
        success_threshold=3,      # Need 3 successes to close
        expected_exception=Exception
    ):
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.success_threshold = success_threshold
        self.expected_exception = expected_exception
        
        # State
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.lock = Lock()
    
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        with self.lock:
            if self.state == CircuitState.OPEN:
                # Check if timeout expired
                if self._should_attempt_reset():
                    self._transition_to_half_open()
                else:
                    raise CircuitBreakerOpenError(
                        f"Circuit breaker is OPEN. "
                        f"Retry after {self._time_until_retry()}s"
                    )
            
            if self.state == CircuitState.HALF_OPEN:
                # In half-open, only allow limited requests
                if self.success_count >= self.success_threshold:
                    self._transition_to_closed()
        
        # Actually make the call
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        
        except self.expected_exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Handle successful call"""
        with self.lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.success_threshold:
                    self._transition_to_closed()
            else:
                # In CLOSED state, reset failure count on success
                self.failure_count = 0
    
    def _on_failure(self):
        """Handle failed call"""
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            
            if self.state == CircuitState.HALF_OPEN:
                # Any failure in half-open → back to open
                self._transition_to_open()
            
            elif self.failure_count >= self.failure_threshold:
                self._transition_to_open()
    
    def _transition_to_open(self):
        """Transition to OPEN state"""
        self.state = CircuitState.OPEN
        self.last_failure_time = datetime.now()
        print(f"⚠️  Circuit breaker OPENED at {self.last_failure_time}")
    
    def _transition_to_half_open(self):
        """Transition to HALF_OPEN state"""
        self.state = CircuitState.HALF_OPEN
        self.success_count = 0
        self.failure_count = 0
        print(f"🔄 Circuit breaker HALF_OPEN")
    
    def _transition_to_closed(self):
        """Transition to CLOSED state"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        print(f"✅ Circuit breaker CLOSED")
    
    def _should_attempt_reset(self):
        """Check if enough time passed to try half-open"""
        if self.last_failure_time is None:
            return False
        
        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return elapsed >= self.timeout_seconds
    
    def _time_until_retry(self):
        """Time remaining until half-open attempt"""
        if self.last_failure_time is None:
            return 0
        
        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return max(0, self.timeout_seconds - elapsed)
    
    @property
    def current_state(self):
        """Get current state info"""
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "time_until_retry": self._time_until_retry()
        }

# Usage Example
def unreliable_service():
    """Simulates an unreliable external service"""
    import random
    if random.random() < 0.7:  # 70% failure rate
        raise Exception("Service unavailable")
    return "Success"

# Create circuit breaker
cb = CircuitBreaker(
    failure_threshold=3,
    timeout_seconds=10,
    success_threshold=2
)

# Test it, call it once per protected operation, here just an example to call once. 
for i in range(20):
    try:
        result = cb.call(unreliable_service)
        print(f"Request {i+1}: {result} | State: {cb.current_state}")
    except CircuitBreakerOpenError as e:
        print(f"Request {i+1}: BLOCKED - {e}")
    except Exception as e:
        print(f"Request {i+1}: FAILED - {e} | State: {cb.current_state}")
    
    time.sleep(1)
```

**Output example:**
```
Request 1: FAILED - Service unavailable | State: CLOSED, failures: 1
Request 2: Success | State: CLOSED, failures: 0
Request 3: FAILED - Service unavailable | State: CLOSED, failures: 1
Request 4: FAILED - Service unavailable | State: CLOSED, failures: 2
Request 5: FAILED - Service unavailable | State: CLOSED, failures: 3
⚠️  Circuit breaker OPENED
Request 6: BLOCKED - Circuit breaker is OPEN. Retry after 9s
Request 7: BLOCKED - Circuit breaker is OPEN. Retry after 8s
...
Request 15: BLOCKED - Circuit breaker is OPEN. Retry after 0s
🔄 Circuit breaker HALF_OPEN
Request 16: Success | State: HALF_OPEN, successes: 1
Request 17: Success | State: HALF_OPEN, successes: 2
✅ Circuit breaker CLOSED
Request 18: Success | State: CLOSED, failures: 0
```
## 5. Advanced Circuit Breaker with Sliding Window
**Problem with simple counter:** One burst of errors can trip circuit, even if overall health is good.
>Use a **sliding window** in a circuit breaker when you want the breaker to react to the **recent health** of a dependency (last N requests or last T seconds), not lifetime counters. It’s the most common production approach because it’s stable under traffic spikes and avoids “one old incident keeps poisoning the breaker.”

eg:
```
If QPS changes a lot (API traffic, user-driven load), a simple “N consecutive failures” or “failure_count since start” behaves badly.
- Sliding window answers: “In the last 20 calls (or last 10s), how bad is it?”
- That’s what you want when load can spike.
```

**Solution:** Use sliding window to track failures over time.
```python
from collections import deque
from datetime import datetime, timedelta

class SlidingWindowCircuitBreaker:
    def __init__(
        self,
        window_size_seconds=60,
        failure_threshold_percentage=50,  # Open if >50% failures
        minimum_requests=10,               # Need at least 10 requests
        timeout_seconds=30
    ):
        self.window_size = timedelta(seconds=window_size_seconds)
        self.failure_threshold_pct = failure_threshold_percentage
        self.minimum_requests = minimum_requests
        self.timeout_seconds = timeout_seconds
        
        # Sliding window of (timestamp, success: bool)
        self.requests = deque()
        self.state = CircuitState.CLOSED
        self.last_open_time = None
        self.lock = Lock()
    
    def call(self, func, *args, **kwargs):
        with self.lock:
            self._clean_old_requests()
            
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self._transition_to_half_open()
                else:
                    raise CircuitBreakerOpenError("Circuit is OPEN")
        
        # Execute
        start_time = datetime.now()
        try:
            result = func(*args, **kwargs)
            self._record_result(start_time, success=True)
            return result
        except Exception as e:
            self._record_result(start_time, success=False)
            raise
    
    def _record_result(self, timestamp, success):
        """Record request result in sliding window"""
        with self.lock:
            self.requests.append((timestamp, success))
            self._clean_old_requests()
            
            # Check if should open circuit
            if self.state == CircuitState.CLOSED:
                if self._should_open():
                    self._transition_to_open()
            
            elif self.state == CircuitState.HALF_OPEN:
                if success:
                    self._transition_to_closed()
                else:
                    self._transition_to_open()
    
    def _clean_old_requests(self):
        """Remove requests outside the time window"""
        cutoff = datetime.now() - self.window_size
        
        while self.requests and self.requests[0][0] < cutoff:
            self.requests.popleft()
    
    def _should_open(self):
        """Determine if circuit should open based on failure rate"""
        total = len(self.requests)
        
        if total < self.minimum_requests:
            return False
        
        failures = sum(1 for _, success in self.requests if not success)
        failure_rate = (failures / total) * 100
        
        return failure_rate > self.failure_threshold_pct
    
    def _should_attempt_reset(self):
        if self.last_open_time is None:
            return False
        
        elapsed = (datetime.now() - self.last_open_time).total_seconds()
        return elapsed >= self.timeout_seconds
    
    def _transition_to_open(self):
        self.state = CircuitState.OPEN
        self.last_open_time = datetime.now()
        print(f"⚠️  Circuit OPENED - Failure rate too high")
    
    def _transition_to_half_open(self):
        self.state = CircuitState.HALF_OPEN
        print(f"🔄 Circuit HALF_OPEN - Testing recovery")
    
    def _transition_to_closed(self):
        self.state = CircuitState.CLOSED
        self.requests.clear()
        print(f"✅ Circuit CLOSED - Service recovered")
    
    @property
    def metrics(self):
        """Get current metrics"""
        total = len(self.requests)
        if total == 0:
            return {
                "state": self.state.value,
                "total_requests": 0,
                "failure_rate": 0
            }
        
        failures = sum(1 for _, success in self.requests if not success)
        
        return {
            "state": self.state.value,
            "total_requests": total,
            "failures": failures,
            "failure_rate": f"{(failures/total)*100:.1f}%"
        }
```

**Why sliding window is better:**
```
Simple counter (last 5 requests):
[S, S, S, F, F] → 2/5 failures = 40%

[F, F, F, F, F] → 5/5 failures = 100% → OPENS
↑ Could be old failures from 2 hours ago!

Sliding window (last 60 seconds):
Current time: 14:35:00
Window: 14:34:00 - 14:35:00

14:34:05: F
14:34:10: F
14:34:15: F
14:34:58: S
14:34:59: S
→ 3 failures in 60s = 60% → OPENS

14:35:15: Old failures drop out of window
14:35:15: S
14:35:16: S
→ 0 failures in last 60s = 0% → CLOSED
```
## 6. Fallback Strategies
When circuit is open, you need a **fallback** strategy:
### Strategy 1: Return Cached/Stale Data
```python
class CachedCircuitBreaker:
    def __init__(self):
        self.cb = CircuitBreaker(failure_threshold=3)
        self.cache = {}
    
    def get_user_profile(self, user_id):
        try:
            # Try to fetch fresh data
            profile = self.cb.call(user_service.get_profile, user_id)
            
            # Cache successful response
            self.cache[user_id] = {
                'data': profile,
                'timestamp': datetime.now()
            }
            return profile
        
        except CircuitBreakerOpenError:
            # Circuit open - return cached data
            cached = self.cache.get(user_id)
            
            if cached:
                print(f"⚠️  Using cached data from {cached['timestamp']}")
                return cached['data']
            else:
                # No cache available
                return {"error": "Service unavailable", "user_id": user_id}
```

### Strategy 2: Return Default/Degraded Response
```python
def get_product_recommendations(user_id):
    try:
        return cb.call(ml_service.get_recommendations, user_id)
    except CircuitBreakerOpenError:
        # Fallback to popular products (not personalized)
        print("⚠️  ML service down, showing popular products")
        return db.get_popular_products(limit=10)
```

### Strategy 3: Queue for Later Processing
```python
def process_payment(order_id, amount):
    try:
        return cb.call(payment_gateway.charge, order_id, amount)
    
    except CircuitBreakerOpenError:
        # Queue payment for later
        print(f"⚠️  Payment service down, queuing order {order_id}")
        message_queue.enqueue({
            'order_id': order_id,
            'amount': amount,
            'retry_after': datetime.now() + timedelta(minutes=5)
        })
        return {"status": "pending", "message": "Payment queued for processing"}
```

### Strategy 4: Fail Gracefully with User Message
```python
def send_email(user_email, subject, body):
    try:
        return cb.call(email_service.send, user_email, subject, body)
    
    except CircuitBreakerOpenError:
        # Can't send email, but don't crash the request
        logger.error(f"Email service unavailable for {user_email}")
        
        # Save to DB for retry
        db.save_pending_email(user_email, subject, body)
        
        return {
            "sent": False,
            "message": "Email will be sent once service recovers"
        }
```
## 7. Circuit Breaker in Distributed Systems
### Challenge: Multiple Instances
```
Instance 1: CB (failures: 2/5)
Instance 2: CB (failures: 1/5)
Instance 3: CB (failures: 3/5)

Problem: Each instance has its own circuit breaker!
         No shared state
         Inconsistent behavior
```

Solution 1: Shared State (Redis)
```python
import redis
from datetime import datetime, timedelta

class DistributedCircuitBreaker:
    def __init__(self, redis_client, service_name):
        self.redis = redis_client
        self.service_name = service_name
        self.failure_threshold = 5
        self.timeout_seconds = 60
    
    def _get_key(self, suffix):
        return f"circuit_breaker:{self.service_name}:{suffix}"
    
    def call(self, func, *args, **kwargs):
        # Check state in Redis
        state = self.redis.get(self._get_key("state"))
        
        if state == b"OPEN":
            # Check if timeout expired
            open_time = self.redis.get(self._get_key("open_time"))
            if open_time:
                elapsed = time.time() - float(open_time)
                if elapsed < self.timeout_seconds:
                    raise CircuitBreakerOpenError(
                        f"Circuit open. Retry in {self.timeout_seconds - elapsed:.0f}s"
                    )
                else:
                    # Transition to half-open
                    self.redis.set(self._get_key("state"), "HALF_OPEN")
        
        # Execute call
        try:
            result = func(*args, **kwargs)
            self._record_success()
            return result
        except Exception as e:
            self._record_failure()
            raise
    
    def _record_failure(self):
        """Record failure in Redis"""
        key = self._get_key("failures")
        
        # Increment failure count
        failures = self.redis.incr(key)
        self.redis.expire(key, 60)  # Sliding window of 60s
        
        # Check threshold
        if failures >= self.failure_threshold:
            self.redis.set(self._get_key("state"), "OPEN")
            self.redis.set(self._get_key("open_time"), time.time())
            print(f"⚠️  Circuit OPENED (failures: {failures})")
    
    def _record_success(self):
        """Record success in Redis"""
        state = self.redis.get(self._get_key("state"))
        
        if state == b"HALF_OPEN":
            # Success in half-open → close circuit
            self.redis.set(self._get_key("state"), "CLOSED")
            self.redis.delete(self._get_key("failures"))
            print(f"✅ Circuit CLOSED")
        else:
            # Regular success - reset failure count
            self.redis.delete(self._get_key("failures"))

# Usage across multiple instances
redis_client = redis.Redis(host='redis.example.com')
cb = DistributedCircuitBreaker(redis_client, "payment-service")

# All instances share the same circuit state in Redis
```

### Solution 2: Sidecar Pattern (Envoy:  is a high performance C++ distributed _proxy_ designed for single services and applications, as well as a communication bus and “universal data plane”)
```
┌─────────────────┐
│  App Instance   │
│  ┌──────────┐   │
│  │Your App  │   │
│  └────┬─────┘   │
│       │         │
│  ┌────▼──────┐  │
│  │  Envoy    │  │ ← Sidecar with circuit breaker
│  │  Proxy    │  │
│  └────┬──────┘  │
└───────┼─────────┘
        │
        ▼
   External Service

Envoy configuration:
outlier_detection:
  consecutive_5xx: 5
  interval: 10s
  base_ejection_time: 30s
  max_ejection_percent: 50
```
#### NOTE: sidecar means here:
- Same Pod
- Different container
- They share:
	- the same network namespace (same pod ip)
	- localhost access to each other
- your app sends outbound traffic to Envoy (often transparently via iptables in a service mesh), and Envoy forwards to the external service.
#### Why same Pod matters
- Envoy can intercept the app’s traffic with low latency.
- It can apply circuit breaking, retries, timeouts, outlier detection, mTLS, etc., consistently for that workload.
#### Not always a sidecar

Envoy can also be deployed in other roles:
- **Ingress / Gateway** (separate deployment)
- **Edge proxy** in front of many services
- **Dedicated egress gateway** for outbound traffic

## 8. Real-World Examples
AWS API Gateway Circuit Breaker
```python
# API Gateway configuration
x-amazon-apigateway-integration:
  type: http_proxy
  httpMethod: POST
  uri: https://backend-service.com/api
  connectionId: my-vpc-link
  connectionType: VPC_LINK
  
  # Circuit breaker settings
  circuitBreaker:
    tripThreshold: 50        # Percentage of failures
    resetAfter: 30           # Seconds
    volumeThreshold: 10      # Minimum requests
```

---

## 9. System Design Interview Framework

### Question: "Design a resilient microservices architecture"
**Interviewer**: "How would you handle one service going down?"
**Your Answer** (Step-by-step):
#### Step 1: Identify the Problem

**You**: "When a dependency service fails, we face several risks:
1. **Resource exhaustion**: Threads blocked waiting for timeouts
2. **Cascading failures**: Slow service makes caller slow, which makes its caller slow...
3. **User impact**: Long wait times, poor experience

To address non-transient failures, I'd implement circuit breakers at service boundaries."

#### Step 2: Draw the Architecture
```
┌────────────────────────────────────┐
│        API Gateway                 │
└─────────────┬──────────────────────┘
              │
              ▼
┌──────────────────────────────┐
│   Order Service              │
│   ┌────────────────┐         │
│   │ Circuit        │         │
│   │ Breaker        │         │
│   └───┬────────────┘         │
└───────┼──────────────────────┘
        │
    ┌───┴──────┬─────────────────┐
    ▼          ▼                 ▼
┌────────┐ ┌──────────┐   ┌───────────┐
│Payment │ │Inventory │   │Shipping   │
│Service │ │Service   │   │Service    │
└────────┘ └──────────┘   └───────────┘
   CB         CB              CB

Each downstream call protected by circuit breaker
```

#### Step 3: Explain Circuit Breaker Behavior
**You**: "Let's trace what happens when Payment Service goes down:

**Normal operation (Circuit CLOSED):**
```
User places order
→ Order Service calls Payment Service
→ Payment processes successfully
→ Order completed
```
**Payment Service crashes:**
```
Request 1 → Payment timeout (30s) ❌
Request 2 → Payment timeout (30s) ❌
Request 3 → Payment timeout (30s) ❌
Request 4 → Payment timeout (30s) ❌
Request 5 → Payment timeout (30s) ❌

Circuit breaker threshold reached (5 failures)
→ Circuit OPENS
```

**Circuit OPEN:**
```
Request 6 → Circuit breaker blocks immediately (1ms) ❌
           → Returns fallback: "Payment queued for later"
           → Order Service stays responsive!

Request 7-100 → All fail fast with fallback
                No wasted resources
                Users get immediate response
```

**After 60 seconds (Circuit HALF_OPEN):**
```
Request 101 → Test call to Payment Service
            → If successful → Circuit CLOSES
            → If fails → Circuit stays OPEN for another 60s
```

#### Step 4: Discuss Configuration
**Interviewer**: "What values would you use for the thresholds?"
**You**: "It depends on the service's characteristics, but here's my thinking:
**For critical services (Payment, Auth):**
```python
CircuitBreaker(
    failure_threshold=10,          # More tolerance
    timeout_seconds=120,           # Longer recovery time
    success_threshold=5,           # Need multiple successes
    window_size_seconds=60
)
```
For less critical services (Recommendations, Analytics):
```python
CircuitBreaker(
    failure_threshold=3,           # Trip faster
    timeout_seconds=30,            # Quick retry
    success_threshold=2,           # Less stringent
    window_size_seconds=30
)
```
**Rationale:**

- Critical services: Give more time to recover, be more conservative
- High traffic: Need more samples before tripping (avoid false positives)
- Low traffic: Can trip faster (fewer samples is OK)"
#### Step 5: Add Fallback Strategies
**Interviewer**: "What happens when circuit is open?"
**You**: "Depends on the service. Let me give examples:
**Payment Service (critical):**
```python
try:
    payment_cb.call(payment_service.charge, amount)
except CircuitBreakerOpenError:
    # Queue for async processing
    message_queue.publish({
        'order_id': order.id,
        'amount': amount,
        'retry_at': now() + timedelta(minutes=5)
    })
    return {
        'status': 'pending',
        'message': 'Payment will be processed shortly'
    }
```

Recommendation Service (non-critical):
```python
try:
    recommendations = reco_cb.call(ml_service.personalized, user_id)
except CircuitBreakerOpenError:
    # Fallback to popular items
    recommendations = db.get_popular_items(limit=10)
    
return recommendations  # User never knows service was down
```
Inventory Service (partial degradation):
```python
try:
    live_stock = inventory_cb.call(inventory_service.check, product_id)
except CircuitBreakerOpenError:
    # Use cached data with warning
    cached_stock = cache.get(f'stock:{product_id}')
    return {
        'quantity': cached_stock,
        'warning': 'Stock levels may not be current'
    }
```

#### Step 6: Handle Distributed Systems
**Interviewer**: "You have 100 Order Service instances. How does circuit breaker work?"

**You**: "Great question. We have two options:
**Option 1: Local circuit breakers (simpler)**
- Each instance has its own circuit breaker
- Pros: No network dependency, faster
- Cons: Inconsistent behavior across instances

**Option 2: Shared circuit breaker (better for critical services)**
```
All Order Service instances
         ↓
    Share state in Redis
         ↓
Circuit breaker state:
- Current state (OPEN/CLOSED/HALF_OPEN)
- Failure count
- Last failure time

Redis key structure:
circuit:payment_service:state → "OPEN"
circuit:payment_service:failures → 15
circuit:payment_service:opened_at → 1699564800
```

I'd use **Option 1 for most cases** because:
- Simpler, no external dependency
- If 20% of instances trip, that's a strong signal
- Once enough instances trip, overall traffic to failing service drops

**Option 2 for critical services** where we need:
- Consistent behavior across all instances
- Precise control over when to stop calling service"

---

## 10. Common Interview Mistakes
### ❌ Mistake 1: Confusing Retry with Circuit Breaker

**Wrong:**
"When a request fails, the circuit breaker retries it."

**Right:**
"Circuit breaker prevents calls to a failing service. Retry logic handles transient failures. They serve different purposes:
- Retry: For temporary issues (network blip)
- Circuit breaker: For persistent failures (service down)"

### ❌ Mistake 2: Not Discussing Fallback

**Wrong:**
"When circuit opens, requests fail."

**Right:**
"When circuit opens, we need a fallback strategy. For example:
- Return cached data
- Return default response
- Queue for later processing
The fallback depends on whether the operation is critical and whether we have alternative data sources."

### ❌ Mistake 3: Ignoring Distributed Systems

**Wrong:**
"I'll add a circuit breaker class to my service."

**Right:**
"In a distributed system with multiple instances, I need to consider:
- Should circuit state be shared (Redis) or local?
- How do we coordinate across instances?
- For most cases, local circuit breakers are simpler and sufficient."

### ❌ Mistake 4: No Metrics/Monitoring

**Wrong:**
Just implementing circuit breaker without discussing observability.

**Right:**
"We need to monitor:
- Circuit state transitions (OPEN/CLOSED)
- Failure rates per service
- Time spent in OPEN state
- Fallback execution rates

This helps us:
- Detect service degradation
- Tune threshold values
- Identify cascade failure patterns"

---

## 11. Advanced Topics

### Health Checks vs Circuit Breaker

**They're complementary:**
```
Health Check (active):
- Periodic probe to service
- "Hey service, are you alive?"
- Proactive detection

Circuit Breaker (passive):
- Monitors actual traffic
- "Service failed 5 real requests"
- Reactive protection
```

Best practice: Use both!
```python
class HealthAwareCircuitBreaker:
    def __init__(self, health_check_interval=30):
        self.cb = CircuitBreaker()
        self.last_health_check = None
        self.health_check_interval = health_check_interval
    
    def call(self, func, *args, **kwargs):
        # Run health check if due
        if self._should_health_check():
            if not self._check_health():
                # Proactively open circuit
                self.cb._transition_to_open()
        
        return self.cb.call(func, *args, **kwargs)
    
    def _check_health(self):
        try:
            # Simple health endpoint
            response = requests.get(
                "https://service/health",
                timeout=1
            )
            return response.status_code == 200
        except:
            return False
```

## 12. Interview Cheat Sheet

### Key Points to Cover

✅ **Problem**: Prevent cascading failures from non-transient errors

✅ **States**: CLOSED (normal), OPEN (blocking), HALF_OPEN (testing)

✅ **Thresholds**:
- Failure threshold: When to open (e.g., 5 failures)
- Timeout: How long to stay open (e.g., 60 seconds)
- Success threshold: When to close (e.g., 3 successes)

✅ **Fallback**: What to do when circuit is open
- Cached data
- Default response
- Queue for later
- Graceful degradation

✅ **Distributed**: Local vs shared state

✅ **Monitoring**: Track state transitions, failure rates

### Quick Decision Framework
```
Is the failure transient?
├─ YES: Use RETRY logic (with exponential backoff)
└─ NO: Use CIRCUIT BREAKER

Is the operation critical?
├─ YES: Conservative thresholds, robust fallback
└─ NO: Aggressive thresholds, simple fallback

Multiple service instances?
├─ YES: Consider shared state (Redis) for critical services
└─ NO: Local circuit breaker is fine

```


# Note


# Reference

