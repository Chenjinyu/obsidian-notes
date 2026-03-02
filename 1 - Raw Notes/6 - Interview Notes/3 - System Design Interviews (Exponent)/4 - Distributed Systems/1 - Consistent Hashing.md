Date: 2026-02-02
Course:
Tags: [[API]]  [[interview]] [[System Design Interview]] [[../../../../High Level]] [[Low Level]] [[1 - Consistent Hashing]] [[Distributed System]]

# Consistent Hashing: Complete System Design Interview Guide

Consistent hashing is a methodology for storing data (key and objects) across different servers. It's advantageous over traditional hashing methods because it efficiently adapts to the adding or removal of servers to the system architecture.


##### Virtual Nodes resolve uneven distribution
![](assets/1%20-%20Consistent%20Hashing/file-20260216200918985.png)

Let's take a look at what might happen when server 1 fails. Note that none of the keys have to be rehashed. Instead, all the servers mapped on the circle associated with server 1 are removed. In this case, the key may be reassigned to a different server (since the closest one in the clockwise direction may no longer be server 1).

**The advantages of this method include:**
- Not all keys have to be reassigned to different servers.
- The hash value of the keys do not need to be recomputed.
![](assets/1%20-%20Consistent%20Hashing/file-20260216200720997.png)
Therefore, we can see the advantages that consistent hashing offers over traditional hashing methods! Just as an aside, in real life, caching systems like **Memcached** and **Redis**, support out-of-the-box solutions for consistent hashing.
## 1. The Problem: Why Traditional Hashing Fails in Distributed Systems

### Traditional Hash Table Approach
Imagine you have a simple cache with 3 servers:

```python
# Traditional approach
def get_server(key, num_servers=3):
    hash_value = hash(key)
    server_index = hash_value % num_servers
    return server_index

# Examples:
hash("user_123") % 3 = 2  → Server 2
hash("user_456") % 3 = 1  → Server 1
hash("user_789") % 3 = 0  → Server 0
```

**Visual:**
```
Keys distributed across 3 servers:
Server 0: [user_789, user_111, ...]
Server 1: [user_456, user_222, ...]
Server 2: [user_123, user_333, ...]
```

### The Catastrophic Problem: Server Addition/Removal

**Scenario**: One server fails, now you have 2 servers
```python
# Same keys, now with 2 servers
hash("user_123") % 2 = 0  → Server 0 (was Server 2) ❌
hash("user_456") % 2 = 0  → Server 0 (was Server 1) ❌
hash("user_789") % 2 = 1  → Server 1 (was Server 0) ❌
```

**Result**: Nearly ALL keys are remapped!
```
Before (3 servers):              After (2 servers):
Server 0: [user_789, ...]   →    Server 0: [user_123, user_456, ...]
Server 1: [user_456, ...]   →    Server 1: [user_789, ...]
Server 2: [user_123, ...]   →    (gone)
```

**Impact**:
- **100% cache miss rate** during transition
- **Massive database load** (cache stampede)
- **Data migration nightmare** if storing data (not just caching)
- **Downtime** during rebalancing

**Mathematical analysis**:
- With N servers, adding/removing 1 server causes **~(N-1)/N keys to remap**
- 3 servers → 2 servers: 66% of keys remap
- 10 servers → 9 servers: 90% of keys remap
- 1000 servers → 999 servers: 99.9% of keys remap

**Interview insight**: "The problem with modulo hashing is that it creates a dependency between the hash value and the number of servers. When N changes, almost all keys remap. We need a solution where adding/removing a server only affects ~1/N of the keys."

---
## 2. Consistent Hashing: The Solution

### Core Concept

Instead of `hash(key) % N`, we:

1. Map both **keys** and **servers** to the same hash space (0 to 2^32-1)
2. Arrange them on a circle (ring)
3. Each key is assigned to the **next server clockwise** on the ring
### Visualization
```
Hash Ring (0 to 2^32-1):

                    0/2^32
                      ▲
                      |
          Server A ━━━●━━━ Server B
                 ╱         ╲
                ╱           ╲
               ●             ●
            key_3           key_1
              ╱               ╲
             ╱                 ╲
    Server C ●←────────────────● key_2
    
Assignments:
- key_1 (hash=100) → next server clockwise → Server B (hash=150)
- key_2 (hash=800) → next server clockwise → Server C (hash=900)
- key_3 (hash=300) → next server clockwise → Server A (hash=400)
```

### Simple Implementation
```python
import hashlib
from bisect import bisect_right

class ConsistentHash:
    def __init__(self):
        self.ring = {}  # hash_value -> server_name
        self.sorted_keys = []  # sorted hash values
    
    def _hash(self, key):
        """Hash function: string -> 0 to 2^32-1"""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_server(self, server_name):
        """Add a server to the ring"""
        hash_value = self._hash(server_name)
        self.ring[hash_value] = server_name
        self.sorted_keys.append(hash_value)
        self.sorted_keys.sort()
    
    def remove_server(self, server_name):
        """Remove a server from the ring"""
        hash_value = self._hash(server_name)
        del self.ring[hash_value]
        self.sorted_keys.remove(hash_value)
    
    def get_server(self, key):
        """Find which server a key belongs to"""
        if not self.ring:
            return None
        
        hash_value = self._hash(key)
        
        # Find the first server clockwise (binary search)
        index = bisect_right(self.sorted_keys, hash_value)
        
        # Wrap around if we're past the last server
        if index == len(self.sorted_keys):
            index = 0
        
        server_hash = self.sorted_keys[index]
        return self.ring[server_hash]

# Usage
ch = ConsistentHash()
ch.add_server("server_A")
ch.add_server("server_B")
ch.add_server("server_C")

print(ch.get_server("user_123"))  # → server_A
print(ch.get_server("user_456"))  # → server_B
```

### What Happens When a Server is Removed?
```
Before (3 servers):
     0°          90°         180°        270°        360°
     |-----------|-----------|-----------|-----------|
     A           B           C           A (wrap)
     ↑           ↑           ↑
   key_1       key_2       key_3

After removing Server B:
     0°          90°         180°        270°        360°
     |-----------|-----------|-----------|-----------|
     A                       C           A (wrap)
     ↑           ↑           ↑
   key_1      key_2(→C)    key_3

Only key_2 moved from B → C
key_1 and key_3 stay on their original servers!
```

**Key benefit**: Only **~1/N** of keys are remapped when a server is added/removed.

---
## 3. The Virtual Nodes Problem & Solution
### Problem: Uneven Distribution
With real servers only, distribution can be very uneven:
```
Real example with 3 servers and MD5 hashing:

Ring positions (0 to 2^32):
Server A: hash=500,000,000      (11.6% of ring)
Server B: hash=2,000,000,000    (34.9% of ring)
Server C: hash=3,500,000,000    (53.5% of ring)

       0        500M      2B         3.5B      4.3B
       |---------|---------|----------|---------|
       ←─ A ────→←─── B ───→←──── C ──────────→
       11.6%      34.9%          53.5%

Result: Server C handles 53% of traffic! Huge imbalance.
```

**Why does this happen?**
- Hash functions produce pseudo-random values
- With only 3-10 servers, you have very few points on a huge ring (0 to 4 billion)
- Statistical variance is high with small samples
- Servers can cluster together or spread unevenly

### Solution: Virtual Nodes (Replicas)
Instead of mapping each physical server to **one** point on the ring, map it to **many** points.
**Concept**: Each physical server gets 100-500 virtual nodes
```python
class ConsistentHashWithVirtualNodes:
    def __init__(self, num_virtual_nodes=150):
        self.num_virtual_nodes = num_virtual_nodes
        self.ring = {}  # hash_value -> physical_server_name
        self.sorted_keys = []
    
    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_server(self, server_name):
        """Add a server with multiple virtual nodes"""
        for i in range(self.num_virtual_nodes):
            # Create virtual node key
            virtual_key = f"{server_name}:vnode{i}"
            hash_value = self._hash(virtual_key)
            
            self.ring[hash_value] = server_name  # Points to physical server
            self.sorted_keys.append(hash_value)
        
        self.sorted_keys.sort()
    
    def remove_server(self, server_name):
        """Remove all virtual nodes of a server"""
        for i in range(self.num_virtual_nodes):
            virtual_key = f"{server_name}:vnode{i}"
            hash_value = self._hash(virtual_key)
            
            del self.ring[hash_value]
            self.sorted_keys.remove(hash_value)
    
    def get_server(self, key):
        if not self.ring:
            return None
        
        hash_value = self._hash(key)
        index = bisect_right(self.sorted_keys, hash_value)
        
        if index == len(self.sorted_keys):
            index = 0
        
        server_hash = self.sorted_keys[index]
        return self.ring[server_hash]  # Returns physical server

# Usage
ch = ConsistentHashWithVirtualNodes(num_virtual_nodes=150)
ch.add_server("server_A")
ch.add_server("server_B")
ch.add_server("server_C")
```

### Visual: Virtual Nodes Distribution
```
Without virtual nodes (3 servers, 3 points):
   0°              90°             180°            270°           360°
   |----------------|----------------|---------------|--------------|
   A                                 B               C              A
   └────────────────────────────────┘└──────────────┘└─────────────┘
        75% of ring to A                 25% to B        Gap to C

With virtual nodes (3 servers, 150 vnodes each = 450 points):
   0°              90°             180°            270°           360°
   |----------------|----------------|---------------|--------------|
   A₁ C₂ B₃ A₄ C₅ A₆ B₇ C₈ A₉ B₁₀ C₁₁ A₁₂ ... (many more points)
   └─────────────────────────────────────────────────────────────┘
                    ~33% to each server (much more balanced)
```

### Mathematical Analysis
**Standard deviation of load with N servers**:
Without virtual nodes:
```
σ ≈ 1/√N

N=3:  σ ≈ 58%  (one server could handle 91%, another 9%)
N=10: σ ≈ 32%  (still significant imbalance)
```

With V virtual nodes per server:
```
σ ≈ 1/√(N × V)

N=3, V=150:  σ ≈ 4.7%   (much better!)
N=10, V=100: σ ≈ 3.2%   (excellent balance)
```

**Interview insight**: "Virtual nodes reduce variance from O(1/√N) to O(1/√(N×V)). With 150 virtual nodes per server, load imbalance is typically under 5%."

---
## 4. Benefits of Consistent Hashing vs Traditional Hashing

### Comparison Table

|Aspect|Traditional Hashing (Modulo)|Consistent Hashing|
|---|---|---|
|**Keys remapped on server change**|~(N-1)/N ≈ **90-99%**|~**1/N** ≈ 1-10%|
|**Load balancing**|Perfect (1/N each)|Uneven without vnodes|
|**Load balancing with vnodes**|N/A|Nearly perfect (~1/N each)|
|**Scalability**|Poor (massive reshuffling)|Excellent (minimal impact)|
|**Complexity**|O(1)|O(log N) with binary search|
|**Memory overhead**|Minimal|O(N × V) for virtual nodes|
|**Use case**|Static server count|Dynamic server count|
### Concrete Example
**Scenario**: Cache system with 1 million keys, 10 servers
**Add 1 new server (10 → 11)**:
Traditional hashing:
```
Keys to remap = ~909,090 (90.9%)
Cache misses during transition = ~909,090
Database queries = ~909,090
Time to recover = hours (with cache warmup)
```

Consistent hashing:
```
Keys to remap = ~90,909 (9.1%)
Cache misses during transition = ~90,909
Database queries = ~90,909
Time to recover = minutes
```

**Impact**:
- **10x fewer** cache misses
- **10x less** database load
- **10x faster** recovery
- No downtime needed

---

## 5. Real-World Use Cases
### 1. Amazon DynamoDB
```
Partition key: "user_123"
           ↓
    Consistent hash
           ↓
Virtual node on ring
           ↓
  Physical server: node-47

When adding servers:
- Only ~1/N of data moves
- No full rebalancing needed
- Users see no impact
```

### 2. Memcached/Redis Cluster
```python
# Client-side sharding with consistent hashing
class RedisCluster:
    def __init__(self, redis_nodes):
        self.ch = ConsistentHashWithVirtualNodes()
        for node in redis_nodes:
            self.ch.add_server(node)
    
    def get(self, key):
        server = self.ch.get_server(key)
        redis_client = get_redis_connection(server)
        return redis_client.get(key)
    
    def set(self, key, value):
        server = self.ch.get_server(key)
        redis_client = get_redis_connection(server)
        return redis_client.set(key, value)

# Usage
cluster = RedisCluster([
    "redis-1.example.com:6379",
    "redis-2.example.com:6379",
    "redis-3.example.com:6379"
])

cluster.set("user_123", "John Doe")
# Automatically goes to correct server based on consistent hash
```

### 3. Load Balancers (with Session Affinity)
```
User requests:
    user_123 → hash → always routes to Server A
    user_456 → hash → always routes to Server B

Benefits:
- Session stickiness (same user → same server)
- If Server B fails, only user_456 is affected
- Other users' sessions remain intact
```

### 4. Content Delivery Networks (CDN)
```
Video file: "movie_123.mp4"
           ↓
    Consistent hash
           ↓
Cache server: edge-47 (Dallas)

When new edge server added:
- Only ~1/N of files need to move
- Most cache stays hot
- Minimal origin server load
```

---

## 6. System Design Interview Deep Dive
### Question: "Design a distributed cache like Memcached"

**Step 1: Clarify (1-2 min)**
```
You: "A few questions:
- Scale: How many servers? How many requests per second?
- Do servers join/leave frequently, or is it stable?
- Do we need data persistence, or is it pure cache?
- Is this client-side or server-side partitioning?"

Interviewer: "100 cache servers, 1M QPS, servers can fail. Client-side partitioning."
```

**Step 2: High-Level Design (3-4 min)**

Draw on whiteboard:
```
┌─────────────┐
│   Client    │
│  (with      │
│  consistent │
│  hash lib)  │
└──────┬──────┘
       │
       ├───────────────┬───────────────┬──────────
       ▼               ▼               ▼
   ┌────────┐      ┌────────┐      ┌────────┐
   │Cache   │      │Cache   │      │Cache   │
   │Server 1│      │Server 2│ ...  │Server N│
   └────────┘      └────────┘      └────────┘
```

**You explain**: "We'll use consistent hashing to distribute keys across cache servers. Each client maintains a consistent hash ring with all server nodes. When a cache server fails, only 1/N of the keys remap."

**Step 3: Deep Dive - Consistent Hashing (8-10 min)**
```
Interviewer: "How does consistent hashing work?"
```

**Your answer** (use the whiteboard):
```
1. Hash both keys and servers to the same space (0 to 2^32-1)

   Ring: 0 ─────────── 2^31 ─────────── 2^32-1
                                          │
                                        wraps to 0

2. Place servers on the ring:
   hash("server_1") = 500M   →  Server 1 at position 500M
   hash("server_2") = 1.5B   →  Server 2 at position 1.5B
   hash("server_3") = 3B     →  Server 3 at position 3B

3. Place keys on the ring:
   hash("user_123") = 1B     →  Key at position 1B

4. Assign key to next server clockwise:
   user_123 (1B) → next server → Server 2 (1.5B)

                0/4.3B
                  ┃
         Server 1 ●━━━━━━━━━━━● Server 2
              ╱   500M      1.5B   ╲
             ╱                      ╲
            ╱         ● user_123     ╲
           ●          (1B)            ●
        3B                           
      Server 3
```

```
Interviewer: "What if servers aren't evenly distributed?"
```

**Your answer**:
"Good question! With only 3-10 real servers, we can get significant load imbalance due to random hash values. The solution is **virtual nodes**:
Each physical server is mapped to 150-200 points on the ring instead of just 1.
```python
# Instead of:
hash("server_1") → one point

# We do:
hash("server_1:vnode0") → point 1
hash("server_1:vnode1") → point 2
...
hash("server_1:vnode149") → point 150
```

This spreads each server across the ring, achieving much better load balance."
Draw:
```
Without vnodes:              With 150 vnodes per server:
┌─────────────────┐          ┌─────────────────┐
│ S1: 60%         │          │ S1: 33.2%       │
│ S2: 25%         │          │ S2: 33.5%       │
│ S3: 15%         │          │ S3: 33.3%       │
└─────────────────┘          └─────────────────┘
 Big imbalance!               Nearly perfect!
```

```
Interviewer: "What happens when a server fails?"
```

**Your answer**:
"Let's trace through it:
1. Server 2 fails at position 1.5B on the ring
2. All keys that were assigned to Server 2 (clockwise from Server 1 to Server 2) now map to Server 3 (the next server clockwise)
    
```
Before:                          After Server 2 fails:
   S1 ──→ user_123 ──→ S2          S1 ──→ user_123 ──→ S3
   500M    1B         1.5B         500M    1B         3B
           ↓
      Goes to S2                       Now goes to S3
```

3. Only the keys between S1 and S2 are affected (~1/3 in this case)
4. Other keys (between S2-S3 and S3-S1) remain on their original servers
    
In a 100-server system, only ~1% of keys remap when one server fails."

**Step 4: Implementation Details (5 min)**
```
Interviewer: "Show me the code structure."
```

```python
class ConsistentHashRing:
    def __init__(self, num_vnodes=150):
        self.num_vnodes = num_vnodes
        self.ring = {}  # hash_value -> physical_server
        self.sorted_hashes = []  # sorted list for binary search
        
    def add_node(self, node_id):
        """Add a physical server with virtual nodes"""
        for i in range(self.num_vnodes):
            vnode_key = f"{node_id}:vn{i}"
            hash_val = self._hash(vnode_key)
            self.ring[hash_val] = node_id
            self.sorted_hashes.append(hash_val)
        self.sorted_hashes.sort()
    
    def remove_node(self, node_id):
        """Remove all virtual nodes of a server"""
        for i in range(self.num_vnodes):
            vnode_key = f"{node_id}:vn{i}"
            hash_val = self._hash(vnode_key)
            del self.ring[hash_val]
            self.sorted_hashes.remove(hash_val)
    
    def get_node(self, key):
        """Find which server handles this key"""
        if not self.ring:
            return None
        
        hash_val = self._hash(key)
        
        # Binary search for first server >= hash_val
        idx = bisect_right(self.sorted_hashes, hash_val)
        if idx == len(self.sorted_hashes):
            idx = 0  # Wrap around
        
        server_hash = self.sorted_hashes[idx]
        return self.ring[server_hash]
    
    def _hash(self, key):
        """MD5 hash to 32-bit integer"""
        return int(hashlib.md5(key.encode()).hexdigest()[:8], 16)


class MemcachedClient:
    def __init__(self, server_list):
        self.ring = ConsistentHashRing()
        self.connections = {}
        
        for server in server_list:
            self.ring.add_node(server)
            self.connections[server] = create_connection(server)
    
    def get(self, key):
        server = self.ring.get_node(key)
        return self.connections[server].get(key)
    
    def set(self, key, value):
        server = self.ring.get_node(key)
        return self.connections[server].set(key, value)
```

```
Interviewer: "What's the time complexity?"
```

**Your answer**:
- `add_node`: O(V log(N×V)) where V = vnodes, N = servers (sorting)
- `remove_node`: O(V × N×V) naive, but can optimize to O(V log(N×V))
- `get_node`: **O(log(N×V))** using binary search ← most important (per request)
- Space: O(N × V)

For 100 servers with 150 vnodes each:
- Ring size: 15,000 entries
- `get_node` lookup: log₂(15,000) ≈ 14 comparisons (very fast!)

**Step 5: Trade-offs and Extensions (3-5 min)**
```
Interviewer: "Any limitations or improvements?"
```

**Your answer**:

**Limitations:**
1. **No replication**: If server fails, data is lost (just cache, so maybe OK)
2. **Hot keys**: If one key is super popular, all traffic goes to one server
3. **Thundering herd**: When server fails, 1/N of keys miss cache simultaneously

**Solutions:**
1. **Replication**: Store each key on K consecutive servers

```python
def get_nodes(self, key, count=3):
    """Get primary + replica servers"""
    nodes = []
    hash_val = self._hash(key)
    idx = bisect_right(self.sorted_hashes, hash_val)
    
    for _ in range(count):
        if idx >= len(self.sorted_hashes):
            idx = 0
        server = self.ring[self.sorted_hashes[idx]]
        if server not in nodes:  # Avoid duplicates (same physical server)
            nodes.append(server)
        idx += 1
    
    return nodes
```
2. **Hot key handling**: Detect hot keys and replicate to multiple servers
3. **Gradual migration**: When adding servers, migrate data slowly to avoid spike

**Weighted nodes for heterogeneous servers:**
```python
# Powerful server gets 2x virtual nodes
ring.add_node("beefy_server", num_vnodes=300)
ring.add_node("weak_server", num_vnodes=150)
# Beefy server handles ~2x traffic
```

---
## 7. Advanced Topics
### Jump Consistent Hash (Google's Improvement)

**Problem with standard consistent hashing**: O(log N) lookup, O(N×V) memory
**Jump Consistent Hash**: O(1) memory, O(log N) time, but servers must be numbered 0 to N-1
```python
def jump_consistent_hash(key, num_buckets):
    """
    Google's jump consistent hash
    Paper: https://arxiv.org/abs/1406.2294
    """
    b, j = -1, 0
    
    while j < num_buckets:
        b = j
        key = ((key * 2862933555777941757) + 1) & 0xFFFFFFFFFFFFFFFF
        j = int((b + 1) * (float(1 << 31) / float((key >> 33) + 1)))
    
    return b

# Usage
server = jump_consistent_hash(hash("user_123"), num_servers=10)
```

**Trade-off**:
- ✅ Much simpler (no ring structure)
- ✅ Better memory usage
- ❌ Servers must be numbered sequentially
- ❌ Can't remove servers from middle (only shrink from end)

**When to use**: Cloud services where you control server IDs (like Google)

### Rendezvous Hashing (Highest Random Weight)
Alternative to consistent hashing:
```python
def rendezvous_hash(key, servers):
    """Each server gets a weight for this key; pick highest"""
    def weight(server, key):
        return hash(f"{server}:{key}")
    
    return max(servers, key=lambda s: weight(s, key))

# Adding/removing server only affects 1/N of keys
# No ring structure needed!
```

**Comparison:**
- Consistent hashing: O(log N) lookup, O(N×V) space
- Rendezvous hashing: O(N) lookup, O(N) space
- Jump hash: O(log N) lookup, O(1) space

---

## 8. Interview Checklist

When discussing consistent hashing, make sure to cover:
✅ **Problem statement**: Why modulo hashing fails (90%+ key remapping)
✅ **Solution overview**: Hash ring with keys and servers
✅ **Core algorithm**:
- Hash keys and servers to same space
- Assign key to next server clockwise
- Binary search for O(log N) lookup
✅ **Virtual nodes**:
- Why needed (load balance)
- How many (100-200 typically)
- Impact on variance (O(1/√(N×V)))
✅ **Benefits**:
- Only 1/N keys remap on server change
- Incremental scalability
- Minimal disruption
✅ **Implementation details**:
- Data structures (sorted array + hash map)
- Time complexity
- Space complexity
✅ **Real-world usage**:
- DynamoDB, Cassandra
- Memcached, Redis
- CDNs, load balancers
✅ **Trade-offs**:
- Complexity vs modulo hashing
- Memory overhead (virtual nodes)
- Alternatives (jump hash, rendezvous)

---

## 9. Sample Interview Dialogue

**Interviewer**: "We're building a distributed cache. We have 100 cache servers and expect to add/remove servers frequently as traffic changes. How would you distribute keys across servers?"
**You**: "I'd use consistent hashing. The main insight is that with traditional modulo hashing—where we do `hash(key) % N`—adding or removing even a single server causes about 90% of all keys to remap to different servers. This creates a massive cache miss storm.

Consistent hashing solves this by mapping both keys and servers onto a circular hash space. Each key is assigned to the next server clockwise on the ring. When a server is removed, only the keys that were on that server need to remap—about 1/N of the total—to the next server in the ring."

**Interviewer**: "How do you ensure even load distribution?"

**You**: "Great question. With only 100 real servers on a hash space of 2^32 values, we can get unlucky with hash values and end up with severe load imbalance—one server might get 50% of the traffic.

The solution is virtual nodes. Instead of placing each physical server at one point on the ring, we place it at 150-200 points using different hash inputs like 'server_1:vnode0', 'server_1:vnode1', etc. This spreads each server across the ring and reduces load variance from O(1/√N) to O(1/√(N×V)). With 150 virtual nodes, typical load imbalance is under 5%."

**Interviewer**: "What's your implementation approach?"

**You**: "I'd maintain two data structures:
1. A hash map: `hash_value → physical_server_id`
2. A sorted array of all hash values for binary search

To find which server handles a key:
1. Hash the key
2. Binary search the sorted array to find the first hash value ≥ key's hash
3. Look up the corresponding server in the hash map

This gives us O(log(N×V)) lookup time, which for 100 servers × 150 vnodes = 15,000 entries is about 14 comparisons—very fast."

**Interviewer**: "What happens when a server fails?"

**You**: "When server S fails, all 150 of its virtual nodes are removed from the ring. Keys that were mapped to those virtual nodes now map to the next servers clockwise—distributed across many different physical servers since the virtual nodes were spread around the ring.

Importantly, keys that were on other servers are completely unaffected. So we've limited the blast radius to just 1/N of the keyspace. The cache miss rate spikes briefly for those affected keys, but the other 99% of keys continue to hit cache normally."

---

## 10. Key Takeaways
🎯 **Core concept**: Map keys and servers to a ring; assign keys to next server clockwise
🎯 **Main benefit**: Only ~1/N keys remap when adding/removing servers (vs ~99% with modulo)
🎯 **Virtual nodes**: Essential for load balancing; use 100-200 per server
🎯 **Time complexity**: O(log N) lookup with binary search
🎯 **Space complexity**: O(N × V) where V = virtual nodes per server
🎯 **Use cases**: Distributed caches (Memcached, Redis), databases (DynamoDB, Cassandra), CDNs, load balancers
🎯 **Interview strategy**:
1. Explain the problem (modulo hashing fails)
2. Explain the solution (hash ring)
3. Address load balancing (virtual nodes)
4. Discuss implementation (binary search)
5. Cover trade-offs and alternatives
Good luck with your interview! Remember: interviewers care more about your thought process and ability to discuss trade-offs than perfect recall of every detail. Show you understand **why** consistent hashing exists and **when** to use it.

# Note


# Reference

