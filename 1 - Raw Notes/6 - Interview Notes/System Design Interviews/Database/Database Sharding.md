Date: 2026-02-05
Course:
Tags: 

# Content

Database sharding is **horizontal partitioning**: you split one logical database/table into **multiple independent databases (shards)**, and each shard stores **a subset of the rows**.
Instead of one big `users` table on one database, you might have:
- `users_shard_1` stores users with IDs 0–9,999,999
- `users_shard_2` stores users with IDs 10,000,000–19,999,999
- …

Your app (or a routing layer) decides **which shard** to read/write for a given key.
## Why people shard
- **Scale writes and storage** beyond a single DB machine
- **Increase throughput** by distributing load
- **Isolate blast radius** (one shard can be sick without killing all data)
- **Geo/latency** (place shards closer to users in some designs)

## Sharding vs replication (common confusion)
- **Replication** copies the _same_ data to multiple nodes (for HA/read scaling).
- **Sharding** splits data so each node holds _different_ data (for write/storage scaling).  
    Often you do both: _each shard has replicas_.
    
## Common sharding strategies
1. **Hash-based sharding**
- `shard = hash(user_id) % N`
- Pros: even distribution
- Cons: changing N causes lots of movement (mitigate with consistent hashing)
    

2. **Range-based sharding**
    

- `user_id 1–1M` → shard A, `1M–2M` → shard B
    
- Pros: range queries are easy
    
- Cons: hotspots if IDs/time are skewed
    

3. **Directory/lookup-based sharding**
    

- A mapping service/table: `user_id -> shard_id`
    
- Pros: flexible, easy rebalancing
    
- Cons: extra dependency; must be highly available
    

4. **Geo-based sharding**
    

- Users in NA → shard NA, EU → shard EU
    
- Pros: latency/compliance
    
- Cons: cross-region queries are harder
    

## What becomes harder with sharding

- **Joins across shards** (often need app-level joins)
    
- **Transactions across shards** (need Saga/2PC-like approaches or redesign)
    
- **Re-sharding/rebalancing** (moving data safely is hard)
    
- **Global secondary indexes** (must be distributed too)
    
- **Operational complexity** (backups, schema changes across shards)
    

## Interview-ready one-liner

> “Sharding splits rows across multiple databases by a shard key to scale storage and write throughput; it improves scale but makes cross-shard queries and transactions harder.”

If you tell me your use case (orders/payments, multi-tenant SaaS, social app, etc.), I can recommend a good **shard key** and show how routing + rebalancing would work.

# Note


# Reference

