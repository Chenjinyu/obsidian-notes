Date: 2026-02-04
Course:
Tags: [[System Design Interview]] [[../../../../3 - Zettelkasten/B - Tags/High Level]] [[Low Level]] [[Availability]]

# Gateway Aggregation Pattern: Complete Guide for Microservices

### Excellent topic! Gateway Aggregation (also called BFF - Backend for Frontend) is crucial for building efficient microservices. Let me give you a comprehensive breakdown.

## 1. The Problem: Microservice Chattiness

### Without Gateway (Direct Client-to-Microservices)
**Scenario**: User views a product page
```
Mobile App (3G network, high latency)
    │
    ├──→ GET /products/123          ──→ Product Service    (150ms)
    ├──→ GET /reviews?product=123   ──→ Review Service     (200ms)
    ├──→ GET /inventory/123         ──→ Inventory Service  (100ms)
    ├──→ GET /recommendations/123   ──→ Recommendation     (300ms)
    └──→ GET /pricing/123           ──→ Pricing Service    (120ms)

Total time (sequential): 870ms
Total network round trips: 5
Data transferred: 5 separate responses
User experience: Slow, poor on mobile
```

**Problems:**
1. **High latency**: Multiple round trips, especially bad on mobile (3G/4G)
2. **Chattiness**: 5 separate requests for one page view
3. **Client complexity**: Client must know about 5 different services
4. **Over-fetching**: Each service returns full payload, client only needs subset
5. **Authentication**: Client must authenticate with each service
6. **Error handling**: Client must handle failures from 5 different sources

### With Gateway Aggregation
```
Mobile App (3G network)
    │
    └──→ GET /gateway/product-page/123  ──→ API Gateway
                                               │
         ┌─────────────────────────────────────┼────────────────┐
         │                                     │                │
         │ (All requests in parallel)          │                │
         │                                     │                │
         ▼                                     ▼                ▼
    Product Service (150ms)           Review Service    Inventory Service
         │                                (200ms)            (100ms)
         │                                     │                │
         │                                     ▼                ▼
         │                           Recommendation      Pricing Service
         │                              (300ms)            (120ms)
         │                                     │                │
         └─────────────────┬───────────────────┴────────────────┘
                           │
                           ▼
                    Aggregate Results
                           │
                           ▼
                    Single Response
                           │
                           ▼
                      Mobile App

Total time (parallel): 300ms (longest service)
Total network round trips: 1
Data transferred: 1 optimized response
User experience: Fast! 🚀
```

**Benefits:**

✅ **66% latency reduction** (870ms → 300ms)
✅ **80% fewer network calls** (5 → 1)
✅ **Simpler client** (1 endpoint instead of 5)
✅ **Optimized payload** (only data client needs) 
✅ **Centralized auth** (authenticate once at gateway)

---

## 2. Gateway Aggregation Patterns

### Pattern 1: Simple Aggregation (Fan-Out/Fan-In)

**Use case**: Dashboard that shows data from multiple services

```python
from flask import Flask, jsonify
import asyncio
import aiohttp
from typing import Dict, Any

app = Flask(__name__)

class AggregationGateway:
    def __init__(self):
        self.service_urls = {
            'user': 'http://user-service:8001',
            'orders': 'http://order-service:8002',
            'payments': 'http://payment-service:8003',
            'notifications': 'http://notification-service:8004'
        }
    
    async def fetch_service(self, session, service_name: str, endpoint: str):
        """Fetch data from a single service"""
        url = f"{self.service_urls[service_name]}{endpoint}"
        
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=2)) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": f"{service_name} returned {response.status}"}
        except asyncio.TimeoutError:
            return {"error": f"{service_name} timeout"}
        except Exception as e:
            return {"error": f"{service_name} failed: {str(e)}"}
    
    async def get_user_dashboard(self, user_id: str) -> Dict[str, Any]:
        """
        Aggregate data from multiple services in parallel
        """
        async with aiohttp.ClientSession() as session:
            # Fan-out: Make all requests in parallel
            tasks = [
                self.fetch_service(session, 'user', f'/users/{user_id}'),
                self.fetch_service(session, 'orders', f'/orders?user_id={user_id}'),
                self.fetch_service(session, 'payments', f'/payments?user_id={user_id}'),
                self.fetch_service(session, 'notifications', f'/notifications?user_id={user_id}')
            ]
            
            # Wait for all to complete
            results = await asyncio.gather(*tasks)
            
            # Fan-in: Combine results
            user_data, orders_data, payments_data, notifications_data = results
            
            # Aggregate into single response
            return {
                "user": user_data,
                "recentOrders": orders_data.get('orders', [])[:5],  # Last 5 orders
                "paymentMethods": payments_data.get('methods', []),
                "unreadNotifications": notifications_data.get('unread_count', 0),
                "metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "version": "1.0"
                }
            }

gateway = AggregationGateway()

@app.route('/api/dashboard/<user_id>')
async def dashboard(user_id):
    """Single endpoint that aggregates data from 4 services"""
    dashboard_data = await gateway.get_user_dashboard(user_id)
    return jsonify(dashboard_data)

# Client usage (simple!)
# GET /api/dashboard/user123
# Returns everything in one call
```

**Latency comparison:**

```
Without Gateway (Sequential):
User: 100ms + Orders: 150ms + Payments: 120ms + Notifications: 80ms = 450ms

With Gateway (Parallel):
max(100ms, 150ms, 120ms, 80ms) = 150ms

Improvement: 67% faster! ⚡
```

---

### Pattern 2: GraphQL-Style Field Selection

**Use case**: Client specifies exactly what data it needs
```python
from flask import Flask, request, jsonify
import asyncio
import aiohttp

app = Flask(__name__)

class GraphQLStyleGateway:
    """
    Allow clients to request specific fields
    Reduces over-fetching
    """
    
    async def fetch_product_aggregate(self, product_id: str, fields: list):
        """
        Fetch only requested fields
        
        Example fields:
        ['basic_info', 'reviews', 'inventory', 'related_products']
        """
        
        # Map fields to service calls
        field_to_service = {
            'basic_info': ('product', f'/products/{product_id}'),
            'reviews': ('review', f'/reviews?product_id={product_id}'),
            'inventory': ('inventory', f'/inventory/{product_id}'),
            'related_products': ('recommendation', f'/recommendations/{product_id}'),
            'pricing': ('pricing', f'/pricing/{product_id}'),
            'seller_info': ('seller', f'/sellers?product_id={product_id}')
        }
        
        # Only fetch requested fields
        tasks = []
        field_names = []
        
        async with aiohttp.ClientSession() as session:
            for field in fields:
                if field in field_to_service:
                    service, endpoint = field_to_service[field]
                    tasks.append(self.fetch_service(session, service, endpoint))
                    field_names.append(field)
            
            # Fetch in parallel
            results = await asyncio.gather(*tasks)
            
            # Build response with only requested fields
            response = {}
            for field_name, result in zip(field_names, results):
                response[field_name] = result
            
            return response
    
    async def fetch_service(self, session, service_name, endpoint):
        """Fetch from service"""
        url = f"http://{service_name}-service:8000{endpoint}"
        
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=2)) as resp:
                return await resp.json() if resp.status == 200 else None
        except:
            return None

gateway = GraphQLStyleGateway()

@app.route('/api/products/<product_id>')
async def get_product(product_id):
    """
    Client specifies fields via query params
    GET /api/products/123?fields=basic_info,reviews,inventory
    """
    # Parse requested fields
    fields_param = request.args.get('fields', 'basic_info')
    fields = [f.strip() for f in fields_param.split(',')]
    
    # Fetch only requested data
    data = await gateway.fetch_product_aggregate(product_id, fields)
    
    return jsonify(data)

# Example usage:
# Mobile app (limited bandwidth):
#   GET /api/products/123?fields=basic_info,pricing
#   Only fetches 2 services
#
# Desktop app (full page):
#   GET /api/products/123?fields=basic_info,reviews,inventory,related_products
#   Fetches 4 services
```

**Benefits:**

```
Mobile client payload:
Without field selection: 150KB (full product data)
With field selection: 15KB (only basic_info + pricing)
90% reduction! 📉

Desktop client payload:
Without field selection: 150KB (same full data)
With field selection: 120KB (more fields, but still optimized)
```

---

### Pattern 3: Backend for Frontend (BFF)

**Use case**: Different clients need different data shapes
```
┌─────────────────────────────────────────────────┐
│            Microservices (Backend)              │
├─────────────────────────────────────────────────┤
│  [User] [Product] [Order] [Payment] [Review]   │
└────────┬────────────────────────────────────────┘
         │
         │ Different aggregation for each client
         │
    ┌────┴─────────────────┬─────────────────┐
    │                      │                 │
    ▼                      ▼                 ▼
┌─────────┐          ┌──────────┐      ┌──────────┐
│ Mobile  │          │  Web     │      │  Partner │
│ Gateway │          │ Gateway  │      │  API     │
│ (BFF)   │          │  (BFF)   │      │ Gateway  │
└────┬────┘          └────┬─────┘      └────┬─────┘
     │                    │                  │
     ▼                    ▼                  ▼
┌─────────┐          ┌──────────┐      ┌──────────┐
│ Mobile  │          │  Web     │      │ Partner  │
│   App   │          │   App    │      │  Client  │
└─────────┘          └──────────┘      └──────────┘
```

**Implementation:**

```python
# mobile_gateway.py - Optimized for mobile
class MobileBFF:
    """Backend for Frontend - Mobile optimized"""
    
    async def get_product_page(self, product_id: str):
        """
        Mobile-optimized response:
        - Smaller images
        - Limited reviews (first 3)
        - Essential data only
        """
        async with aiohttp.ClientSession() as session:
            # Fetch in parallel
            product, reviews, inventory = await asyncio.gather(
                self.fetch_product(session, product_id),
                self.fetch_reviews(session, product_id, limit=3),  # Only 3 reviews
                self.fetch_inventory(session, product_id)
            )
            
            # Mobile-optimized response
            return {
                "id": product['id'],
                "name": product['name'],
                "price": product['price'],
                "thumbnail": product['images'][0]['small'],  # Small image only
                "rating": product['rating'],
                "inStock": inventory['quantity'] > 0,
                "topReviews": reviews[:3],  # Top 3 reviews only
                "shipping": {
                    "estimatedDays": 3,
                    "cost": product['shipping_cost']
                }
            }
            # Total payload: ~15KB

# web_gateway.py - Optimized for web
class WebBFF:
    """Backend for Frontend - Web optimized"""
    
    async def get_product_page(self, product_id: str):
        """
        Web-optimized response:
        - High-res images
        - All reviews with pagination
        - Rich product details
        """
        async with aiohttp.ClientSession() as session:
            # Fetch more data for web
            product, reviews, inventory, recommendations, seller = await asyncio.gather(
                self.fetch_product(session, product_id),
                self.fetch_reviews(session, product_id, limit=20),  # More reviews
                self.fetch_inventory(session, product_id),
                self.fetch_recommendations(session, product_id),
                self.fetch_seller(session, product['seller_id'])
            )
            
            # Web-optimized response (richer)
            return {
                "id": product['id'],
                "name": product['name'],
                "description": product['description'],  # Full description
                "price": product['price'],
                "images": product['images'],  # All images (high-res)
                "rating": product['rating'],
                "specifications": product['specs'],  # Technical specs
                "inventory": {
                    "quantity": inventory['quantity'],
                    "warehouse": inventory['location']
                },
                "reviews": {
                    "total": reviews['total_count'],
                    "items": reviews['items'][:20],
                    "pagination": reviews['pagination']
                },
                "recommendations": recommendations,
                "seller": {
                    "name": seller['name'],
                    "rating": seller['rating'],
                    "shipsFrom": seller['location']
                }
            }
            # Total payload: ~150KB (acceptable for web)

# partner_api_gateway.py - Optimized for B2B partners
class PartnerAPIGateway:
    """Backend for Frontend - Partner API"""
    
    async def get_product_data(self, product_id: str):
        """
        Partner-optimized response:
        - Bulk data format
        - Additional wholesale pricing
        - Inventory across warehouses
        """
        async with aiohttp.ClientSession() as session:
            product, inventory_all, pricing_wholesale = await asyncio.gather(
                self.fetch_product(session, product_id),
                self.fetch_all_inventory(session, product_id),  # All warehouses
                self.fetch_wholesale_pricing(session, product_id)
            )
            
            return {
                "sku": product['sku'],
                "product_name": product['name'],
                "retail_price": product['price'],
                "wholesale_pricing": pricing_wholesale,  # Tiered pricing
                "inventory_by_warehouse": inventory_all,
                "minimum_order_quantity": 10,
                "bulk_discount": pricing_wholesale['discount_schedule']
            }
```

**Why BFF pattern?**

```
Mobile App needs:
- Fast response (3G/4G)
- Small payload (data costs)
- Battery efficient
→ Optimized endpoint with minimal data

Web App needs:
- Rich experience
- All details
- High-res images
→ Full-featured endpoint

Partner API needs:
- Bulk operations
- Wholesale pricing
- Multiple warehouses
→ Business-focused endpoint

One-size-fits-all = suboptimal for everyone
BFF = optimized for each client! ✅
```

---

## 3. Advanced Techniques

### Technique 1: Caching at Gateway Level
**Problem**: Multiple clients request same data repeatedly
```python
import redis
import hashlib
import json
from functools import wraps

class CachingGateway:
    def __init__(self):
        self.cache = redis.Redis(host='redis', port=6379)
        self.cache_ttl = 300  # 5 minutes
    
    def cached(self, ttl=300):
        """Decorator to cache gateway responses"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = self._generate_cache_key(func.__name__, args, kwargs)
                
                # Try cache first
                cached_data = self.cache.get(cache_key)
                if cached_data:
                    print(f"✅ Cache HIT for {cache_key}")
                    return json.loads(cached_data)
                
                # Cache miss - fetch from services
                print(f"❌ Cache MISS for {cache_key}")
                result = await func(*args, **kwargs)
                
                # Store in cache
                self.cache.setex(
                    cache_key,
                    ttl,
                    json.dumps(result)
                )
                
                return result
            
            return wrapper
        return decorator
    
    def _generate_cache_key(self, func_name, args, kwargs):
        """Generate unique cache key"""
        key_data = f"{func_name}:{str(args)}:{str(kwargs)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    @cached(ttl=300)
    async def get_product_page(self, product_id: str):
        """Cached aggregation - avoids hitting services repeatedly"""
        # This will be cached for 5 minutes
        return await self._fetch_from_services(product_id)

# Example traffic pattern:
# Request 1: Cache MISS → Fetch from 5 services → 300ms
# Request 2-100 (within 5 min): Cache HIT → Return cached → 5ms
# 
# Latency reduction: 98.3%
# Backend load reduction: 99%
```

**Benefits:**

```
Without caching:
100 requests → 100 backend calls → High load on services

With caching (5 min TTL):
100 requests → 1 backend call → 99% load reduction
First request: 300ms
Subsequent: 5ms (from cache)
```

---

### Technique 2: Circuit Breaker per Service
**Problem**: One slow/failing service shouldn't block entire aggregation
```python
from datetime import datetime, timedelta

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout_seconds=60):
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if self._should_attempt_reset():
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failure_count = 0
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
    
    def _should_attempt_reset(self):
        if not self.last_failure_time:
            return False
        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return elapsed >= self.timeout_seconds

class ResilientGateway:
    def __init__(self):
        # Circuit breaker per service
        self.circuit_breakers = {
            'product': CircuitBreaker(),
            'review': CircuitBreaker(),
            'inventory': CircuitBreaker(),
            'recommendation': CircuitBreaker()
        }
    
    async def get_product_page(self, product_id: str):
        """
        Resilient aggregation - degrades gracefully if services fail
        """
        results = {}
        
        # Product service (critical - no fallback)
        try:
            cb = self.circuit_breakers['product']
            results['product'] = await cb.call(
                self.fetch_product, product_id
            )
        except Exception as e:
            # Product is critical - fail the entire request
            return {"error": "Product service unavailable"}, 503
        
        # Review service (non-critical - has fallback)
        try:
            cb = self.circuit_breakers['review']
            results['reviews'] = await cb.call(
                self.fetch_reviews, product_id
            )
        except Exception as e:
            # Fallback: empty reviews
            results['reviews'] = {
                "items": [],
                "message": "Reviews temporarily unavailable"
            }
        
        # Inventory service (non-critical - has fallback)
        try:
            cb = self.circuit_breakers['inventory']
            results['inventory'] = await cb.call(
                self.fetch_inventory, product_id
            )
        except Exception as e:
            # Fallback: show as "check availability"
            results['inventory'] = {
                "status": "unknown",
                "message": "Check availability at checkout"
            }
        
        # Recommendation service (non-critical - has fallback)
        try:
            cb = self.circuit_breakers['recommendation']
            results['recommendations'] = await cb.call(
                self.fetch_recommendations, product_id
            )
        except Exception as e:
            # Fallback: popular products
            results['recommendations'] = await self.get_popular_products()
        
        return results

# Scenario: Review service is down
# Request 1-5: Try review service, fails, records failures
# Request 6: Circuit breaker OPENS for review service
# Request 6-100: Review service skipped immediately (fail-fast)
#                Other services continue working
#                User gets partial data (acceptable!)
```

**Resilience benefit:**
```
Scenario: Review service crashes

Without circuit breaker:
Every request waits 30s for review service timeout
Total latency: 30s+ (terrible UX)
All other services delayed

With circuit breaker:
First 5 requests: 30s timeout (records failures)
Request 6+: Circuit opens
           → Review service skipped immediately
           → Fallback: empty reviews
           → Total latency: 200ms (other services only)
           → 99.3% latency improvement! ✅

Page still works, just missing reviews
Much better than complete failure!
```

---

### Technique 3: Request Collapsing (Deduplication)
**Problem**: Multiple concurrent requests for same data
```python
import asyncio
from collections import defaultdict

class RequestCollapser:
    """
    Collapse multiple identical requests into single backend call
    """
    def __init__(self):
        self.pending_requests = defaultdict(list)
        self.locks = defaultdict(asyncio.Lock)
    
    async def fetch_with_collapse(self, key: str, fetch_func):
        """
        If multiple requests for same key arrive concurrently,
        only make one backend call and share the result
        """
        async with self.locks[key]:
            # Check if request already in flight
            if key in self.pending_requests:
                # Request in flight - wait for it
                future = asyncio.Future()
                self.pending_requests[key].append(future)
                return await future
            
            # No request in flight - we'll make the call
            self.pending_requests[key] = []
        
        try:
            # Make the actual backend call
            result = await fetch_func()
            
            # Share result with all waiting requests
            for future in self.pending_requests[key]:
                future.set_result(result)
            
            return result
        
        finally:
            # Clean up
            del self.pending_requests[key]

collapser = RequestCollapser()

async def get_product(product_id):
    """Gateway endpoint with request collapsing"""
    return await collapser.fetch_with_collapse(
        f"product:{product_id}",
        lambda: fetch_from_product_service(product_id)
    )

# Example scenario:
# 100 concurrent requests for product:123 arrive
# Without collapsing: 100 backend calls
# With collapsing: 1 backend call, result shared with all 100
# 
# Backend load: 99% reduction
# All requests get response in same time as 1 request
```

---

### Technique 4: Timeout Management

**Problem**: Slow service delays entire aggregation
```python
import asyncio

class TimeoutGateway:
    def __init__(self):
        self.service_timeouts = {
            'product': 2.0,       # Critical - 2s timeout
            'inventory': 1.0,     # Fast service - 1s timeout
            'review': 3.0,        # Can be slower - 3s timeout
            'recommendation': 5.0 # ML service - 5s timeout
        }
        self.overall_timeout = 5.0  # Never exceed 5s total
    
    async def fetch_with_timeout(self, service_name, fetch_func):
        """Fetch with per-service timeout"""
        timeout = self.service_timeouts.get(service_name, 2.0)
        
        try:
            return await asyncio.wait_for(fetch_func(), timeout=timeout)
        except asyncio.TimeoutError:
            print(f"⚠️ {service_name} timed out after {timeout}s")
            return None
    
    async def get_aggregated_data(self, product_id):
        """Aggregate with overall timeout"""
        try:
            # Overall timeout for entire aggregation
            return await asyncio.wait_for(
                self._fetch_all_services(product_id),
                timeout=self.overall_timeout
            )
        except asyncio.TimeoutError:
            # Return partial data if overall timeout exceeded
            return {
                "error": "Request timed out",
                "partial_data": self._get_cached_or_default()
            }
    
    async def _fetch_all_services(self, product_id):
        """Fetch from all services with individual timeouts"""
        # All requests in parallel, each with own timeout
        product_task = self.fetch_with_timeout(
            'product',
            lambda: fetch_product(product_id)
        )
        review_task = self.fetch_with_timeout(
            'review',
            lambda: fetch_reviews(product_id)
        )
        inventory_task = self.fetch_with_timeout(
            'inventory',
            lambda: fetch_inventory(product_id)
        )
        
        # Wait for all (some might timeout and return None)
        product, reviews, inventory = await asyncio.gather(
            product_task,
            review_task,
            inventory_task,
            return_exceptions=True  # Don't fail if one times out
        )
        
        # Build response with available data
        response = {}
        
        if product and not isinstance(product, Exception):
            response['product'] = product
        
        if reviews and not isinstance(reviews, Exception):
            response['reviews'] = reviews
        else:
            response['reviews'] = {"message": "Reviews unavailable"}
        
        if inventory and not isinstance(inventory, Exception):
            response['inventory'] = inventory
        else:
            response['inventory'] = {"status": "unknown"}
        
        return response

# Example:
# Product service: 150ms ✅
# Review service: 10s (hanging) ⚠️
# Inventory service: 100ms ✅
#
# Without timeout: Wait 10s for reviews, then continue
# With timeout: Reviews timeout at 3s, continue with others
#              Total: 3s (acceptable) vs 10s (terrible)
```

---

## 4. Preventing Gateway from Becoming Single Point of Failure

### Strategy 1: Multiple Gateway Instances

```
                  Load Balancer
                       │
           ┌───────────┼───────────┐
           │           │           │
           ▼           ▼           ▼
      ┌────────┐  ┌────────┐  ┌────────┐
      │Gateway │  │Gateway │  │Gateway │
      │   1    │  │   2    │  │   3    │
      └────────┘  └────────┘  └────────┘
           │           │           │
           └───────────┼───────────┘
                       │
              Backend Services
```

**Configuration (Kubernetes):**

```yaml
# gateway-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
spec:
  replicas: 3  # Multiple instances
  selector:
    matchLabels:
      app: api-gateway
  template:
    metadata:
      labels:
        app: api-gateway
    spec:
      containers:
      - name: gateway
        image: mycompany/api-gateway:1.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "1000m"
            memory: "1Gi"
        livenessProbe:  # Health check
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: api-gateway
spec:
  type: LoadBalancer
  selector:
    app: api-gateway
  ports:
  - port: 80
    targetPort: 8080
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-gateway-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-gateway
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**Benefits:**

```
Single gateway:
If crashes → 100% unavailable ❌

Multiple gateways (3 instances):
If 1 crashes → Load balancer routes to other 2
Availability: 100% (assuming 2 can handle load) ✅

Auto-scaling:
Normal load: 3 instances
Peak load: Scales to 10 instances
Always enough capacity ✅
```

---

### Strategy 2: Health Checks & Circuit Breakers

```python
from flask import Flask, jsonify
import requests

app = Flask(__name__)

class GatewayHealthCheck:
    def __init__(self):
        self.backend_services = {
            'product': 'http://product-service:8001',
            'review': 'http://review-service:8002',
            'inventory': 'http://inventory-service:8003'
        }
        self.service_health = {}
    
    def check_backend_health(self):
        """Check health of all backend services"""
        health = {}
        
        for service_name, service_url in self.backend_services.items():
            try:
                response = requests.get(
                    f"{service_url}/health",
                    timeout=1
                )
                health[service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "latency_ms": response.elapsed.total_seconds() * 1000
                }
            except Exception as e:
                health[service_name] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
        
        self.service_health = health
        return health
    
    def is_gateway_healthy(self):
        """Gateway is healthy if critical services are up"""
        critical_services = ['product']  # Product is critical
        
        for service in critical_services:
            if service not in self.service_health:
                return False
            if self.service_health[service]['status'] != 'healthy':
                return False
        
        return True

health_checker = GatewayHealthCheck()

@app.route('/health')
def health():
    """
    Load balancer calls this endpoint
    Returns 200 if healthy, 503 if not
    """
    backend_health = health_checker.check_backend_health()
    gateway_healthy = health_checker.is_gateway_healthy()
    
    status_code = 200 if gateway_healthy else 503
    
    return jsonify({
        "status": "healthy" if gateway_healthy else "unhealthy",
        "backends": backend_health,
        "timestamp": datetime.utcnow().isoformat()
    }), status_code

# Load balancer configuration:
# Checks /health every 5 seconds
# If returns 503 → Remove gateway from pool
# If returns 200 → Add back to pool
# 
# Result: Only healthy gateways receive traffic
```

---

### Strategy 3: Rate Limiting at Gateway

**Prevent gateway overload:**

```python
import redis
from flask import Flask, request, jsonify
import time

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379)

class GatewayRateLimiter:
    """
    Protect gateway from overload
    Limit requests per client
    """
    def __init__(self, max_requests=1000, window_seconds=60):
        self.max_requests = max_requests
        self.window = window_seconds
    
    def is_allowed(self, client_id):
        """Check if client is within rate limit"""
        key = f"rate_limit:{client_id}"
        current = redis_client.incr(key)
        
        if current == 1:
            redis_client.expire(key, self.window)
        
        return current <= self.max_requests

rate_limiter = GatewayRateLimiter(max_requests=1000, window_seconds=60)

@app.before_request
def check_rate_limit():
    """Apply rate limiting to all requests"""
    client_id = request.headers.get('X-Client-ID', request.remote_addr)
    
    if not rate_limiter.is_allowed(client_id):
        return jsonify({
            "error": "Rate limit exceeded",
            "limit": 1000,
            "window": "60 seconds",
            "retry_after": 60
        }), 429  # Too Many Requests

# Protects gateway from:
# - Malicious clients (DDoS)
# - Buggy clients (infinite loops)
# - Ensures fair usage
```

---

## 5. System Design Interview Framework

### Question: "Design an API Gateway for a microservices e-commerce platform"

#### Step 1: Clarify Requirements

**You**: "Let me understand the requirements:
1. **How many microservices** are we aggregating?
2. **What clients** will use this? (Mobile, web, partners?)
3. **Expected traffic**? (requests/sec, peak loads?)
4. **Latency requirements**? (acceptable response time?)
5. **Critical vs non-critical services**? (which can fail gracefully?)"

**Interviewer**: "15 microservices. Mobile and web clients. 10K req/sec normal, 50K peak. Sub-500ms latency required. Product service is critical, others can degrade."

#### Step 2: High-Level Architecture

```
┌──────────────────────────────────────────────────────────┐
│                      CLIENTS                             │
├──────────────────────────────────────────────────────────┤
│    [Mobile App]      [Web App]      [Partner API]        │
└────────┬─────────────────┬────────────────┬──────────────┘
         │                 │                │
         │                 │                │
         ▼                 ▼                ▼
┌──────────────────────────────────────────────────────────┐
│            AWS ALB (Load Balancer)                       │
│  - SSL Termination                                       │
│  - Health Checks                                         │
│  - WAF (DDoS protection)                                 │
└────────┬─────────────────────────────────────────────────┘
         │
         │ Auto-scales: 4-25 gateway instances
         │
    ┌────┴─────┬──────────┬──────────┬─────────┐
    ▼          ▼          ▼          ▼         ▼
┌─────────┐┌─────────┐┌─────────┐┌─────────┐ ... (auto-scale)
│Mobile   ││  Web    ││ Partner ││ Mobile  │
│Gateway  ││ Gateway ││ Gateway ││ Gateway │
│  (BFF)  ││  (BFF)  ││  (BFF)  ││  (BFF)  │  ← Each has:
│         ││         ││         ││         │    - Rate limiting
│ Circuit ││ Circuit ││ Circuit ││ Circuit │    - Circuit breakers
│ Breakers││ Breakers││ Breakers││ Breakers│    - Aggregation logic
└────┬────┘└────┬────┘└────┬────┘└────┬────┘
     │          │          │          │
     └──────────┴──────────┴──────────┘
                │
                ▼
     ┌────────────────────────┐
     │   Redis Sentinel       │  ← High Availability
     │  ┌──────┐  ┌─────────┐ │
     │  │Master│  │Replica 1│ │
     │  └──────┘  └─────────┘ │
     │  ┌─────────┐           │
     │  │Replica 2│           │
     │  └─────────┘           │
     └───────────┬────────────┘
                 │
                 │ Parallel aggregation
                 │
    ┌────────────┼─────────┬──────────────────┬─────────┐
    │            │         │                  │         │
    ▼            ▼         ▼                  ▼         ▼
┌──────────┐  ┌──────┐┌─────────┐  ...   ┌──────────┐┌───────┐
│Product   │  │Inv.  ││Review   │  (15)  │Recommend.││Pricing│
│(CRITICAL)│  │      ││(degrade)│        │(degrade) ││       │
└──────────┘  └──────┘└─────────┘        └──────────┘└───────┘

┌──────────────────────────────────────────────────────────┐
│           Observability Stack                            │
├──────────────────────────────────────────────────────────┤
│  Prometheus  │  Grafana  │  Jaeger  │  ELK  │  Alerts    │
└──────────────────────────────────────────────────────────┘
```
**Key improvements:**
1. ✅ **BFF pattern**: Mobile/Web/Partner gateways optimized for each client
2. ✅ **Auto-scaling**: 4-25 instances based on load
3. ✅ **Redis Sentinel**: High availability cache
4. ✅ **Rate limiting**: Protection from abuse
5. ✅ **Observability**: Monitoring, logging, tracing, alerts
6. ✅ **Circuit breakers inside gateways**: Clear ownership
7. ✅ **WAF at ALB**: DDoS protection

#### Step 3: Explain Aggregation Strategy

**You**: "The gateway will use parallel aggregation with these characteristics:
**Request flow:**

```python
@app.route('/api/product/<product_id>')
async def get_product_page(product_id):
    # 1. Check cache first
    cached = cache.get(f'product_page:{product_id}')
    if cached:
        return cached  # Return in ~5ms
    
    # 2. Fan-out to services in parallel
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_with_circuit_breaker('product', 
                lambda: get_product(session, product_id)),
            fetch_with_circuit_breaker('inventory',
                lambda: get_inventory(session, product_id)),
            fetch_with_circuit_breaker('reviews',
                lambda: get_reviews(session, product_id)),
            fetch_with_circuit_breaker('pricing',
                lambda: get_pricing(session, product_id))
        ]
        
        # Wait for all (with timeout)
        results = await asyncio.wait_for(
            asyncio.gather(*tasks, return_exceptions=True),
            timeout=0.4  # 400ms max
        )
    
    # 3. Aggregate results
    response = build_response(results)
    
    # 4. Cache for future requests
    cache.setex(f'product_page:{product_id}', 300, response)
    
    return response
```

**Latency breakdown:**

```
Without gateway (sequential):
Product: 100ms + Inventory: 80ms + Reviews: 150ms + Pricing: 70ms = 400ms

With gateway (parallel):
max(100ms, 80ms, 150ms, 70ms) + aggregation overhead (10ms) = 160ms

60% latency reduction! ✅
```

#### Step 4: Handle Failure Scenarios

**Interviewer**: "What if Review service is down?"

**You**: "The gateway handles this gracefully using circuit breakers:

```python
# Circuit breaker per service
circuit_breakers = {
    'product': CircuitBreaker(critical=True),   # No fallback - must work
    'inventory': CircuitBreaker(critical=False), # Has fallback
    'reviews': CircuitBreaker(critical=False),   # Has fallback
    'pricing': CircuitBreaker(critical=False)    # Has fallback
}

async def fetch_reviews(product_id):
    try:
        cb = circuit_breakers['reviews']
        return await cb.call(review_service.get, product_id)
    except CircuitBreakerOpen:
        # Fallback: return empty reviews with message
        return {
            "items": [],
            "total": 0,
            "message": "Reviews temporarily unavailable"
        }
    except Exception as e:
        # Service error - also use fallback
        return {
            "items": [],
            "total": 0,
            "message": "Unable to load reviews"
        }
```

**Result:**

- Product page still loads
- Shows 'Reviews temporarily unavailable'
- Other sections work normally
- Much better than entire page failing!

**Circuit breaker state:**

```
Review service fails 5 times → Circuit OPENS
Next 100 requests → Skip review service immediately
                  → Return fallback instantly
                  → No wasted time waiting for timeout
After 60 seconds → Circuit goes HALF_OPEN
                 → Try one request to review service
                 → If succeeds → Circuit CLOSES
                 → If fails → Circuit stays OPEN
```

#### Step 5: Scale the Gateway

**Interviewer**: "How do you handle 50K req/sec during Black Friday?"

**You**: "Multiple strategies:

**1. Horizontal scaling with auto-scaling:**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 10   # Normal load
  maxReplicas: 50   # Black Friday
  metrics:
  - type: Resource
    resource:
      name: cpu
      averageUtilization: 70
  - type: Custom
    custom:
      metric:
        name: requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"  # 1K req/sec per pod
```

**2. Aggressive caching:**

```python
# Popular products cached for longer
def get_cache_ttl(product_id):
    if is_popular_product(product_id):
        return 600  # 10 minutes
    else:
        return 300  # 5 minutes

# During Black Friday:
# - Top 100 products cached
# - Cache hit rate: ~80%
# - Only 20% of traffic hits backend
# - 5x reduction in backend load
```

**3. Request prioritization:**

```python
# VIP customers get priority
if user.is_vip():
    priority_queue.add(request)
else:
    normal_queue.add(request)

# Process priority queue first
# Ensures premium users always get fast response
```

**Capacity calculation:**

```
50,000 req/sec target
Each gateway pod: 1,000 req/sec
Pods needed: 50,000 / 1,000 = 50 pods

With 80% cache hit rate:
Backend traffic: 50,000 * 0.2 = 10,000 req/sec
Much more manageable!
```

---

## 6. Common Interview Mistakes

### ❌ Mistake 1: Not Discussing Failure Handling

**Wrong**: "Gateway aggregates data from multiple services."

**Right**: "Gateway aggregates data from multiple services. Each service call is protected by a circuit breaker with specific fallback strategies:

- Critical services (Product): No fallback - request fails
- Non-critical (Reviews, Recommendations): Fallback to cached/default data This ensures the page still loads even if some services are down."

### ❌ Mistake 2: Ignoring Performance

**Wrong**: "Gateway calls services sequentially."

**Right**: "Gateway calls services in **parallel** using async/await. This reduces latency from sum of all services (500ms) to max of slowest service (150ms). We also implement request collapsing to deduplicate concurrent requests for the same data."

### ❌ Mistake 3: Gateway as Single Point of Failure

**Wrong**: "All traffic goes through the gateway."

**Right**: "All traffic goes through the gateway, so we ensure it's not a single point of failure by:

- Running multiple gateway instances (3-50 based on load)
- Auto-scaling based on CPU and request rate
- Health checks at load balancer
- Circuit breakers prevent cascade failures
- Graceful degradation when services fail"

### ❌ Mistake 4: Not Considering Different Clients

**Wrong**: "One gateway for all clients."

**Right**: "We use the BFF (Backend for Frontend) pattern:

- Mobile Gateway: Optimized for bandwidth (small payloads, compressed images)
- Web Gateway: Full-featured (high-res images, all data)
- Partner API: Business-focused (wholesale pricing, bulk operations) Each gateway aggregates differently based on client needs."

---

## 7. Summary Cheat Sheet

### When to Use Gateway Aggregation

✅ **Use when:**

- Multiple microservices for one client operation
- High network latency (mobile clients)
- Need to reduce chattiness
- Different clients need different data shapes
- Want centralized authentication/authorization

❌ **Don't use when:**

- Simple CRUD operations
- Single service per request
- Real-time bidirectional communication (use WebSocket)
- Client can efficiently call services directly

### Key Benefits

|Benefit|How Gateway Helps|
|---|---|
|**Reduced latency**|Parallel calls instead of sequential|
|**Less chattiness**|1 request instead of N requests|
|**Simpler clients**|Client calls 1 endpoint, not N services|
|**Optimized payloads**|Return only what client needs|
|**Centralized concerns**|Auth, logging, rate limiting in one place|
|**Resilience**|Circuit breakers, fallbacks, graceful degradation|

### Architecture Pattern Template

```
Client
  ↓
Load Balancer
  ↓
Gateway (multiple instances)
  ├─ Cache (Redis)
  ├─ Circuit Breakers (per service)
  └─ Request Collapsing
  ↓
Parallel calls to microservices
  ├─ Critical services (must succeed)
  └─ Non-critical services (with fallbacks)
  ↓
Aggregate & optimize response
  ↓
Return to client
```

### Interview Talking Points

1. **Problem**: "Without gateway, client makes N network calls, high latency on mobile"
    
2. **Solution**: "Gateway aggregates N services into 1 call, parallel execution"
    
3. **Benefits**: "Reduced latency (60-80%), simpler clients, optimized payloads"
    
4. **Resilience**: "Circuit breakers per service, graceful degradation, fallbacks"
    
5. **Scale**: "Multiple gateway instances, auto-scaling, caching, no SPOF"
    
6. **Variations**: "BFF pattern for different clients (mobile vs web vs partner)"
    

Good luck with your interview! The key is demonstrating you understand how gateway aggregation **reduces network roundtrips**, **improves latency through parallelization**, and **provides resilience** while avoiding becoming a single point of failure. 🚀

# Note


# Reference

