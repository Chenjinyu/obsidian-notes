Date: 2026-02-03
Course:
Tags: [[API]]  [[System Design Interview]] [[../../../../3 - Zettelkasten/B - Tags/High Level]] [[Availability]]

# Content

# Rate Limiting: Complete System Design Guide

Let me walk you through rate limiting from fundamental concepts to distributed system complexities—exactly what you need for system design interviews.

Used for 
 - Public API Platform
 - Authentication % Identity Systems
 - CDNs / Edge Gateways / WAF / API Gateways
 - Payment, FinTech, and Fraud-senstive workflows
 - LLM/AI inference products
 - High-traffic Consumer Apps (social, messaging, content)
 - Search Systems & Autocomplete / Sugggestions
 - File Upload / Download and Media Processing
 - Notification Systems
 - B2B Multi-tenant Backends (Enterprise SaaS)

429 - Too many request
	- X-Ratelimit-Remaning - remaining limit
	- X-Ratelimit-Limit - Define limit
	- X-Ratelimit-Retry-After - number of seconds to wait before retry again without being throttled.

And RDBMS / File can be used to store Rate Limit Rules. workers reads rules from storage statically or dynamically and cache for quick look up

## 1. Purpose of Rate Limiting

**Why do we need it?**

- **Prevent resource exhaustion**: Stop malicious users or buggy clients from overwhelming your servers
- **Fair resource allocation**: Ensure all users get reasonable access, not just the fastest/greediest
- **Cost control**: Limit expensive operations (like OpenAI API calls that cost money per request)
- **Service tier differentiation**: Free users get 100 req/hour, paid users get 10,000 req/hour
- **Security**: Mitigate DDoS attacks, brute-force login attempts, credential stuffing
- **Dependency protection**: If you call third-party APIs with their own limits, you need to stay within bounds

**Interview tip**: Always start by asking the interviewer about the specific goals. Different goals lead to different designs.

## 2. Core Algorithms/Techniques

### Token Bucket

**How it works**: Bucket holds tokens, refilled at constant rate. Each request consumes a token.

```
Bucket capacity: 100 tokens
Refill rate: 10 tokens/second
Request arrives → check if token available → consume token → allow request
```

**Pros**:

- Allows bursts (if bucket is full, user can make 100 requests instantly)
- Smooth over time

**Cons**:

- More complex state (current tokens + last refill time)

**When to use**: When you want to allow occasional bursts but control average rate

### Leaky Bucket

**How it works**: Requests enter a queue (bucket), processed at constant rate. Overflow requests rejected.

```
Queue capacity: 100 requests
Process rate: 10 requests/second
Request arrives → add to queue → if queue full, reject
```

**Pros**:

- Perfectly smooth output rate
- Simple conceptually

**Cons**:

- No burst allowance
- Queue management overhead

**When to use**: When you need absolutely predictable, smooth traffic to downstream services

### Fixed Window

**How it works**: Count requests in fixed time windows (e.g., 0:00-0:59, 1:00-1:59)

```
Window: 1 minute
Limit: 100 requests
Time 12:00:00 - 12:00:59 → count requests
At 12:01:00 → reset counter to 0
```

**Pros**:

- Extremely simple to implement
- Memory efficient (just a counter + timestamp)

**Cons**:

- **Boundary problem**: User can make 100 requests at 12:00:59 and 100 at 12:01:00 = 200 requests in 2 seconds

**When to use**: Simple use cases where boundary bursts are acceptable

### Sliding Window Log

**How it works**: Keep timestamp of each request, count requests in last N seconds

```
Limit: 100 requests per minute
Store: [timestamp1, timestamp2, ..., timestampN]
Request arrives → remove timestamps older than 60 seconds → count remaining → check limit
```

**Pros**:

- Most accurate
- No boundary problem

**Cons**:

- High memory usage (store every request timestamp)
- Expensive to clean old entries

**When to use**: When accuracy is critical and traffic volume is moderate

### Sliding Window Counter (Hybrid)

**How it works**: Combination of fixed windows with weighted calculation

```
Current window: 100 requests
Previous window: 80 requests
Current time: 30 seconds into current window

Estimated count = 80 × (30/60) + 100 = 40 + 100 = 140
```

**Pros**:

- Good accuracy
- Low memory (just 2 counters)
- Smooths boundary problem

**Cons**:

- Approximation (not perfectly accurate)

**When to use**: Production systems—best balance of accuracy, memory, and performance

**Interview recommendation**: For most system design interviews, suggest **Sliding Window Counter** as your primary choice, mention Token Bucket for burst handling.

## 3. High-Level System Design

### Basic Architecture

```
Client Request
    ↓
Load Balancer
    ↓
Rate Limiter Middleware ← → Cache (Redis)
    ↓                          ↓
API Servers              Rules Engine
    ↓
Database / OpenAI API
```
![](assets/2%20-%20Availability%20-%20Rate%20Limiting/file-20260203204855632.png)
### Should you use middleware?

**Yes, when**:

- You want centralized rate limiting logic
- Multiple services need rate limiting
- You want to decouple rate limiting from business logic

**No, when**:

- Very simple application (just add a decorator/wrapper)
- Single service
- Extreme performance requirements (avoid extra network hop)

**For your OpenAI project** (simple case):

```python
# Simple in-memory approach (single server)
from collections import defaultdict
from time import time

class SimpleRateLimiter:
    def __init__(self, max_requests=10, window_seconds=60):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = defaultdict(list)  # user_id -> [timestamps]
    
    def is_allowed(self, user_id):
        now = time()
        # Clean old requests
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if now - req_time < self.window
        ]
        
        # Check limit
        if len(self.requests[user_id]) < self.max_requests:
            self.requests[user_id].append(now)
            return True
        return False

# Usage in your Flask/FastAPI app
limiter = SimpleRateLimiter(max_requests=10, window_seconds=60)

@app.post("/chat")
def chat(request):
    user_id = request.user.id
    
    if not limiter.is_allowed(user_id):
        return {"error": "Rate limit exceeded"}, 429
    
    # Call OpenAI
    response = openai.ChatCompletion.create(...)
    return response
```

**When to graduate to Redis-based**:

- Multiple servers (shared state needed)
- High traffic (need persistence)
- More sophisticated rules

## 4. Rate Limiting Keys/Dimensions

**What to limit by?**

1. **User ID** (authenticated users)
    
    - Most common
    - Fair per-user limits
    - Requires authentication
2. **IP Address** (unauthenticated)
    
    - Simple
    - Can block malicious actors
    - Problem: shared IPs (corporate networks, NAT)
3. **API Key**
    
    - For API services
    - Clean separation between clients
4. **Geography**
    
    - Comply with regional regulations
    - Handle regional load
    - Prevent abuse from specific regions
5. **Composite keys**
    
    - `user_id + endpoint` → different limits per endpoint
    - `user_id + tier` → free vs paid users
    - `ip + endpoint` → protect login endpoints

**Interview tip**: Start with user ID, mention you'd add IP-based limits for unauthenticated endpoints.

## 5. Rules Engine

**Simple approach** (your OpenAI project):
```python
RATE_LIMITS = {
    "free_user": {"requests": 10, "window": 3600},  # 10/hour
    "paid_user": {"requests": 1000, "window": 3600},  # 1000/hour
    "admin": {"requests": -1, "window": 3600},  # unlimited
}

def get_limit(user):
    tier = user.subscription_tier
    return RATE_LIMITS.get(tier, RATE_LIMITS["free_user"])
```

**Complex rules engine** (enterprise):
```python
class RulesEngine:
    def get_limit(self, context):
        user = context.user
        endpoint = context.endpoint
        geography = context.geo_location
        
        # Check special cases first
        if user.is_admin:
            return float('inf')
        
        # Geography-specific limits
        if geography == "EU":
            base_limit = 500  # GDPR compliance
        else:
            base_limit = 1000
        
        # Endpoint-specific adjustments
        if endpoint == "/expensive-operation":
            base_limit = base_limit // 10
        
        # User tier multiplier
        multiplier = {"free": 0.1, "paid": 1.0, "enterprise": 5.0}
        final_limit = base_limit * multiplier.get(user.tier, 0.1)
        
        return final_limit
```

**Should you cache rules?**

**Yes** if:
- Rules are complex/database-driven
- High request volume
- Rules change infrequently

```python
# Cache rules for 5 minutes
@cache(ttl=300)
def get_rate_limit_rule(user_id, endpoint):
    return db.query("SELECT limit, window FROM rate_limits WHERE ...")
```

## 6. Low-Level Implementation Details

### Redis-Based Sliding Window Counter
```python
import redis
import time

class RedisRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def is_allowed(self, key, max_requests, window_seconds):
        """
        Uses Redis sorted sets with scores as timestamps
        """
        now = time.time()
        window_start = now - window_seconds
        
        pipe = self.redis.pipeline()
        
        # Remove old entries
        pipe.zremrangebyscore(key, 0, window_start)
        
        # Count current requests in window
        pipe.zcard(key)
        
        # Add current request
        pipe.zadd(key, {str(now): now})
        
        # Set expiration
        pipe.expire(key, window_seconds)
        
        results = pipe.execute()
        current_count = results[1]
        
        return current_count < max_requests

# Usage
redis_client = redis.Redis(host='localhost', port=6379)
limiter = RedisRateLimiter(redis_client)

user_key = f"rate_limit:user:{user_id}"
if limiter.is_allowed(user_key, max_requests=100, window_seconds=60):
    # Process request
else:
    # Reject with 429
```

**Alternative: Fixed window with Redis**

```python
def is_allowed_fixed_window(user_id, max_requests, window_seconds=60):
    current_window = int(time.time() / window_seconds)
    key = f"rate_limit:{user_id}:{current_window}"
    
    current = redis.incr(key)
    
    if current == 1:
        redis.expire(key, window_seconds)
    
    return current <= max_requests
```

**Space complexity comparison**:

- Fixed window: O(1) per user
- Sliding window log: O(max_requests) per user
- Sliding window counter: O(1) per user (2 counters)

## 7. Distributed Systems Design

### Architecture for Scale
```
                     ┌─── Rate Limiter 1 ───┐
                     │                      │
Client → LB → API 1 ─┤                      ├─→ Redis Cluster
                     │                      │   (Shared State)
                     └─── Rate Limiter 2 ───┘
                    
                     ┌─── Rate Limiter 3 ───┐
                     │                      │
Client → LB → API 2 ─┤                      ├─→ Redis Cluster
                     │                      │
                     └─── Rate Limiter 4 ───┘
```

### Load Balancer Role
**Yes, you need a load balancer because**:
- Distributes requests across multiple API servers
- Health checks (remove failed nodes)
- SSL termination

**Load balancing strategies**:

1. **Round Robin**: Simple, but rate limiting state scattered
2. **Consistent Hashing on User ID**: Same user → same server (good for local caching)
3. **Least Connections**: Better for varying request durations

**Interview insight**: Mention that consistent hashing can reduce cache misses but creates imbalance if user traffic is skewed.

### Shared Cache: Redis
**Why Redis?**
- Fast (in-memory)
- Atomic operations (INCR, ZADD)
- Built-in expiration
- Distributed (Redis Cluster for scale)

**Read vs Write Cache?**

Rate limiting is **mostly writes**:
- Every request = write (increment counter or add timestamp)
- Read only to check current count

**Caching strategy**:
```
Local Cache (in-process)     →  Redis (shared)
- Rules/configuration         - Request counts
- User tier info             - Timestamps
- TTL: 5-10 minutes          - Real-time data
```

**Example with local + Redis**:
```python
import time
from functools import lru_cache

class TwoTierRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    @lru_cache(maxsize=10000)
    def get_user_limit(self, user_id):
        """Cache user limits locally for 5 min"""
        # This would normally query DB or config service
        return {"max": 100, "window": 60}
    
    def is_allowed(self, user_id):
        # Get limit from local cache (fast)
        limit_config = self.get_user_limit(user_id)
        
        # Check count in Redis (shared state)
        key = f"rate_limit:{user_id}"
        count = self.redis.incr(key)
        
        if count == 1:
            self.redis.expire(key, limit_config["window"])
        
        return count <= limit_config["max"]
```

### Geographic Rate Limiting

**Approach 1: Separate limits per region**
```python
def get_rate_limit_key(user_id, region):
    return f"rate_limit:{region}:{user_id}"

# EU users: 100 req/hour
# US users: 500 req/hour
# Asia users: 300 req/hour

region = get_user_region(request.ip)
key = get_rate_limit_key(user_id, region)
limit = REGIONAL_LIMITS[region]
```

**Approach 2: Regional Redis clusters**
```
EU Users  → EU Load Balancer → EU Redis Cluster
US Users  → US Load Balancer → US Redis Cluster
Asia Users → Asia Load Balancer → Asia Redis Cluster
```
Benefits: Lower latency, regulatory compliance (data residency)

### Handling Race Conditions
**Problem**: Two requests arrive simultaneously
```
Request A: Read count (50) → Check limit (OK) → Increment (51)
Request B: Read count (50) → Check limit (OK) → Increment (52)
Both allowed even if limit is 50!
```

**Solution 1: Atomic operations (Redis)**
```lua
-- Lua script executed atomically in Redis
local current = redis.call('incr', KEYS[1])
if current == 1 then
    redis.call('expire', KEYS[1], ARGV[1])
end
if current > tonumber(ARGV[2]) then
    return 0  -- Reject
else
    return 1  -- Allow
end
```

```python
# Python client
RATE_LIMIT_SCRIPT = """
... (Lua script above)
"""

script = redis.register_script(RATE_LIMIT_SCRIPT)
result = script(keys=[key], args=[window, max_requests])
```

**Solution 2: Distributed locks** (slower, not recommended for rate limiting)

## 8. Handling Rate Limit from User Perspective

### Response Headers (Best Practice)
```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1699564800
Retry-After: 60

{
  "error": "Rate limit exceeded",
  "message": "You have exceeded 100 requests per hour. Try again in 60 seconds."
}
```

### Client-Side Strategies

**1. Exponential Backoff**
```python
import time

def call_api_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url)
        
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            wait_time = min(retry_after, 2 ** attempt)
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
            continue
        
        return response
    
    raise Exception("Max retries exceeded")
```

**2. Client-Side Rate Limiting**

```python
import time
from collections import deque

class ClientRateLimiter:
    def __init__(self, max_requests, window):
        self.max_requests = max_requests
        self.window = window
        self.requests = deque()
    
    def wait_if_needed(self):
        now = time.time()
        
        # Remove old requests
        while self.requests and self.requests[0] < now - self.window:
            self.requests.popleft()
        
        # If at limit, wait
        if len(self.requests) >= self.max_requests:
            sleep_time = self.window - (now - self.requests[0])
            time.sleep(sleep_time)
            self.requests.popleft()
        
        self.requests.append(time.time())

# Usage
limiter = ClientRateLimiter(max_requests=10, window=60)

for i in range(100):
    limiter.wait_if_needed()
    response = call_api()
```

**3. Request Queuing**

For background jobs, queue requests and process at allowed rate.

## 9. Complete Example: Your OpenAI Project

### Simple Version (Single Server)

```python
from flask import Flask, request, jsonify
from functools import wraps
import time
from collections import defaultdict

app = Flask(__name__)

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
    
    def is_allowed(self, user_id, max_req=10, window=60):
        now = time.time()
        self.requests[user_id] = [
            t for t in self.requests[user_id]
            if now - t < window
        ]
        
        if len(self.requests[user_id]) < max_req:
            self.requests[user_id].append(now)
            return True, max_req - len(self.requests[user_id])
        
        return False, 0

limiter = RateLimiter()

def rate_limit(max_requests=10, window=60):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = request.headers.get('User-ID', 'anonymous')
            allowed, remaining = limiter.is_allowed(user_id, max_requests, window)
            
            if not allowed:
                return jsonify({
                    "error": "Rate limit exceeded",
                    "retry_after": window
                }), 429
            
            response = f(*args, **kwargs)
            
            # Add rate limit headers
            if isinstance(response, tuple):
                response, status = response
            else:
                status = 200
            
            headers = {
                'X-RateLimit-Limit': str(max_requests),
                'X-RateLimit-Remaining': str(remaining),
            }
            
            return response, status, headers
        
        return wrapped
    return decorator

@app.route('/chat', methods=['POST'])
@rate_limit(max_requests=10, window=60)
def chat():
    # Call OpenAI
    response = openai.ChatCompletion.create(...)
    return jsonify(response)
```

### Production Version (Redis + Distributed)

```python
import redis
import time
from flask import Flask, request, jsonify

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

RATE_LIMIT_SCRIPT = """
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local current_time = tonumber(ARGV[3])

local window_start = current_time - window

-- Remove old entries
redis.call('ZREMRANGEBYSCORE', key, 0, window_start)

-- Count current requests
local current_count = redis.call('ZCARD', key)

if current_count < limit then
    redis.call('ZADD', key, current_time, current_time)
    redis.call('EXPIRE', key, window)
    return {1, limit - current_count - 1}
else
    return {0, 0}
end
"""

rate_limit_script = redis_client.register_script(RATE_LIMIT_SCRIPT)

def check_rate_limit(user_id, max_requests=10, window=60):
    key = f"rate_limit:{user_id}"
    now = time.time()
    
    result = rate_limit_script(
        keys=[key],
        args=[max_requests, window, now]
    )
    
    allowed = bool(result[0])
    remaining = result[1]
    
    return allowed, remaining

@app.route('/chat', methods=['POST'])
def chat():
    user_id = request.headers.get('User-ID')
    
    allowed, remaining = check_rate_limit(user_id, max_requests=100, window=3600)
    
    if not allowed:
        return jsonify({"error": "Rate limit exceeded"}), 429, {
            'X-RateLimit-Remaining': '0',
            'Retry-After': '3600'
        }
    
    # Your OpenAI logic
    response = call_openai_api(request.json['message'])
    
    return jsonify(response), 200, {
        'X-RateLimit-Remaining': str(remaining)
    }
```

## 10. System Design Interview Framework

When asked about rate limiting in an interview:

**1. Clarify requirements (2-3 minutes)**

- "What are we rate limiting? API requests, user actions, data ingress?"
- "What's the scale? Requests per second? Number of users?"
- "Do we need different limits for different user tiers?"
- "Single region or global?"

**2. High-level design (5 minutes)**

- Draw: Client → LB → API Servers → Redis → Backend
- Explain: "Rate limiter sits as middleware between LB and API"
- Choose algorithm: "I'd use sliding window counter for accuracy and efficiency"

**3. Deep dive (10-15 minutes)**

- Algorithm details (show Redis implementation)
- Handling distributed state
- Race condition handling
- Geographic considerations if relevant

**4. Trade-offs and alternatives (5 minutes)**

- "Fixed window is simpler but has boundary problem"
- "Token bucket allows bursts, which might or might not be desired"
- "For extreme scale, we could use local rate limiting with periodic sync"

**5. Edge cases and monitoring**

- "What if Redis goes down? Fail open or closed?"
- "How do we monitor false positives?"
- "How do users know they're rate limited?"

## Key Takeaways

1. **Start simple**: For your OpenAI project, in-memory Python dictionary is fine initially
2. **Graduate to Redis**: When you have multiple servers or need persistence
3. **Choose sliding window counter**: Best balance for production
4. **Use atomic operations**: Lua scripts in Redis prevent race conditions
5. **Design for observability**: Always return rate limit headers
6. **Think distributed**: Shared state (Redis), load balancing, geographic distribution
7. **Be kind to clients**: Clear error messages, retry-after headers, documentation

Good luck with your interview! The key is showing you can think through the problem from simple to complex, make informed trade-offs, and handle real-world distributed systems challenges.

# Note


# Reference

