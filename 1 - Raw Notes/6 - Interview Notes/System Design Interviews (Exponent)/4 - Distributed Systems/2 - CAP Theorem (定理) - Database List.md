Date: 2026-02-17
Course:
Tags: [[System Design Interview]] [[CAP Theorem]]

# Content
```
CAP THEOREM DATABASE CLASSIFICATION
====================================

CAP Theorem: A distributed database can only guarantee 2 of 3:
  - Consistency (C): All nodes see the same data at the same time
  - Availability (A): Every request gets a response (success or failure)
  - Partition Tolerance (P): System continues despite network splits

In reality, network partitions WILL happen, so you must choose:
  - CP (Consistency + Partition Tolerance) → Sacrifice Availability
  - AP (Availability + Partition Tolerance) → Sacrifice Consistency

Note: There's no "CA" in distributed systems because partitions are inevitable.


# ═════════════════════════════════════════════════════════════════════════════
#  CP DATABASES: Prioritize CONSISTENCY over Availability
#  
#  Trade-off: During network partition, the system becomes unavailable
#             rather than risk returning stale data.
# ═════════════════════════════════════════════════════════════════════════════

CP_DATABASES = {
    "MongoDB": {
        "type": "Document Store",
        "consistency_model": "Strong consistency with Primary-Secondary replication",
        "behavior_on_partition": """
            - Writes ONLY to primary replica
            - If primary becomes unreachable → writes BLOCKED until new primary elected
            - Reads from primary are strongly consistent
            - Reads from secondaries can be stale (unless read concern 'majority')
            - Election process takes time → temporary unavailability
        """,
        "use_cases": [
            "Financial transactions",
            "Inventory management",
            "Order processing systems",
            "Where data accuracy is critical"
        ],
        "example": """
            # MongoDB with strong consistency
            from pymongo import MongoClient, WriteConcern, ReadConcern
            
            client = MongoClient('mongodb://localhost:27017/')
            db = client.mydb
            
            # Write concern: majority (wait for majority of replicas to acknowledge)
            collection = db.get_collection(
                'orders',
                write_concern=WriteConcern(w='majority', wtimeout=5000)
            )
            
            # Read concern: majority (only read data acknowledged by majority)
            collection = db.get_collection(
                'orders',
                read_concern=ReadConcern(level='majority')
            )
            
            # If partition happens and primary is unreachable:
            # ❌ Writes will FAIL (timeout)
            # ✅ Ensures no inconsistent data
        """
    },
    
    "HBase": {
        "type": "Wide Column Store (Hadoop ecosystem)",
        "consistency_model": "Strong consistency (single master per region)",
        "behavior_on_partition": """
            - Each region served by single RegionServer
            - If RegionServer unreachable → region becomes unavailable
            - Master reassigns region to another server (takes time)
            - No writes/reads to that region during reassignment
        """,
        "use_cases": [
            "Time-series data with strong consistency needs",
            "Real-time analytics requiring accurate counts",
            "Audit logs"
        ]
    },
    
    "Redis (Cluster mode with wait)": {
        "type": "In-Memory Key-Value Store",
        "consistency_model": "Configurable - can enforce sync replication",
        "behavior_on_partition": """
            - WAIT command forces synchronous replication
            - WAIT <num_replicas> <timeout>
            - If replicas unreachable → write blocked until timeout
            - Cluster splits: minority partition becomes read-only
        """,
        "use_cases": [
            "Session storage requiring consistency",
            "Rate limiting counters",
            "Distributed locks"
        ],
        "example": """
            import redis
            
            r = redis.Redis(host='localhost', port=6379)
            
            # Write with synchronous replication
            r.set('order:123', 'pending')
            
            # WAIT: block until 2 replicas acknowledge, max 1000ms
            replicas = r.execute_command('WAIT', 2, 1000)
            
            if replicas < 2:
                # Not enough replicas responded → partition likely
                # ❌ Write might not be durable
                print("WARNING: Replication incomplete")
        """
    },
    
    "Consul": {
        "type": "Service Discovery / Key-Value Store",
        "consistency_model": "Strong consistency via Raft consensus",
        "behavior_on_partition": """
            - Uses Raft protocol (like etcd, ZooKeeper)
            - Requires majority quorum for writes
            - If no majority → cluster becomes READ-ONLY
            - Leader election requires majority → temporary unavailability
        """,
        "use_cases": [
            "Service configuration",
            "Distributed locks",
            "Leader election"
        ]
    },
    
    "etcd": {
        "type": "Distributed Key-Value Store (Kubernetes backend)",
        "consistency_model": "Strong consistency via Raft consensus",
        "behavior_on_partition": """
            - Requires majority (quorum) for writes
            - 3-node cluster: needs 2 nodes reachable
            - 5-node cluster: needs 3 nodes reachable
            - If quorum lost → writes BLOCKED
            - Reads can serve stale data unless linearizable read requested
        """,
        "use_cases": [
            "Kubernetes cluster state",
            "Distributed configuration",
            "Coordination service"
        ]
    },
    
    "ZooKeeper": {
        "type": "Coordination Service",
        "consistency_model": "Strong consistency via ZAB (ZooKeeper Atomic Broadcast)",
        "behavior_on_partition": """
            - Requires majority quorum
            - If leader isolated → new leader elected (unavailability window)
            - Minority partition cannot accept writes
            - Guarantees linearizability
        """,
        "use_cases": [
            "Distributed locks",
            "Leader election",
            "Configuration management",
            "Kafka coordination (historically)"
        ]
    },
    
    "Google Cloud Spanner": {
        "type": "NewSQL (Distributed SQL with ACID)",
        "consistency_model": "External consistency (strongest form, uses TrueTime)",
        "behavior_on_partition": """
            - Uses Paxos for consensus across datacenters
            - Requires majority for writes
            - If datacenter partition → minority can't write
            - Reads are ALWAYS consistent (even across globe)
        """,
        "use_cases": [
            "Global financial systems",
            "Multi-region transactional apps",
            "Where strong consistency + global scale needed"
        ]
    },
    
    "FoundationDB": {
        "type": "Distributed Key-Value Store",
        "consistency_model": "Strict serializability",
        "behavior_on_partition": """
            - Requires quorum for transactions
            - Lost quorum → database becomes unavailable
            - No stale reads ever served
        """,
        "use_cases": [
            "Used as backend for Apple CloudKit",
            "Snowflake metadata layer",
            "Systems requiring ACID guarantees"
        ]
    }
}


# ═════════════════════════════════════════════════════════════════════════════
#  AP DATABASES: Prioritize AVAILABILITY over Consistency
#  
#  Trade-off: During network partition, different nodes may return
#             different data (eventual consistency).
# ═════════════════════════════════════════════════════════════════════════════

AP_DATABASES = {
    "Cassandra": {
        "type": "Wide Column Store",
        "consistency_model": "Tunable consistency (eventual by default)",
        "behavior_on_partition": """
            - Every node can accept reads and writes
            - During partition: both sides continue operating
            - Data reconciled later via conflict resolution (last-write-wins)
            - Configurable per-query: CL=ONE (fast), CL=QUORUM (balanced), CL=ALL (slow)
        """,
        "use_cases": [
            "IoT sensor data (millions of writes/sec)",
            "Time-series data (metrics, logs)",
            "Social media feeds",
            "Where downtime is unacceptable"
        ],
        "example": """
            from cassandra.cluster import Cluster
            from cassandra import ConsistencyLevel
            
            cluster = Cluster(['node1', 'node2', 'node3'])
            session = cluster.connect('mykeyspace')
            
            # AP behavior: Write with consistency level ONE
            # ✅ Fast - returns as soon as ANY node acknowledges
            # ⚠️  Other nodes might not have data yet
            query = session.prepare("INSERT INTO events (id, data) VALUES (?, ?)")
            query.consistency_level = ConsistencyLevel.ONE
            
            session.execute(query, (uuid4(), 'event data'))
            
            # During partition:
            # ✅ Writes succeed on isolated nodes
            # ⚠️  Different nodes might have different data
            # ⏱️  Eventually consistent after partition heals
        """
    },
    
    "DynamoDB": {
        "type": "Key-Value / Document Store (AWS)",
        "consistency_model": "Eventual consistency by default, strong consistency optional",
        "behavior_on_partition": """
            - Designed for 99.99% availability
            - Multi-AZ replication within region
            - Eventual consistency: reads might return stale data
            - Strong consistency reads: might fail if replicas unreachable
        """,
        "use_cases": [
            "Gaming leaderboards",
            "Shopping carts",
            "Session storage",
            "Mobile app backends"
        ],
        "example": """
            import boto3
            
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Users')
            
            # Write (always consistent)
            table.put_item(Item={'user_id': '123', 'name': 'Alice'})
            
            # AP behavior: Eventual consistency read (default)
            response = table.get_item(
                Key={'user_id': '123'},
                ConsistentRead=False  # Might return stale data, but always available
            )
            
            # CP behavior: Strong consistency read (optional)
            response = table.get_item(
                Key={'user_id': '123'},
                ConsistentRead=True  # Latest data, but might fail if partition
            )
        """
    },
    
    "CouchDB": {
        "type": "Document Store",
        "consistency_model": "Eventual consistency with multi-master replication",
        "behavior_on_partition": """
            - All nodes are equal (no primary)
            - Every node accepts reads and writes
            - Conflicts detected and resolved via revision history
            - MVCC (Multi-Version Concurrency Control) for conflict resolution
        """,
        "use_cases": [
            "Mobile offline-first apps (PouchDB sync)",
            "Distributed content management",
            "Systems requiring multi-master writes"
        ]
    },
    
    "Riak": {
        "type": "Key-Value Store",
        "consistency_model": "Eventual consistency, tunable",
        "behavior_on_partition": """
            - Based on Amazon Dynamo paper
            - Uses vector clocks for conflict resolution
            - N=3, R=2, W=2 (typical config)
            - During partition: accepts writes, resolves conflicts later
        """,
        "use_cases": [
            "Session storage",
            "User profiles",
            "High-write workloads"
        ]
    },
    
    "Couchbase": {
        "type": "Document Store",
        "consistency_model": "Eventual consistency with cross-datacenter replication",
        "behavior_on_partition": """
            - XDCR (Cross Datacenter Replication) continues during partition
            - Each datacenter independently available
            - Conflicts resolved via timestamp or custom logic
        """,
        "use_cases": [
            "Content management",
            "User profiles",
            "Catalog data"
        ]
    },
    
    "Amazon S3": {
        "type": "Object Storage",
        "consistency_model": "Strong consistency (as of Dec 2020)",
        "behavior_on_partition": """
            NOTE: S3 changed in 2020 from eventual to strong consistency
            
            Before 2020: Classic AP
              - Writes immediately available
              - Reads might return stale version
              - List operations eventually consistent
            
            After 2020: More CP-like
              - Strong read-after-write consistency
              - Still prioritizes availability in multi-region setup
        """,
        "use_cases": [
            "Static website hosting",
            "Data lakes",
            "Backup storage",
            "CDN origin"
        ]
    },
    
    "Voldemort": {
        "type": "Key-Value Store (LinkedIn)",
        "consistency_model": "Eventual consistency (inspired by Dynamo)",
        "behavior_on_partition": """
            - Decentralized like Cassandra
            - Continues operation during partition
            - Vector clocks for versioning
        """,
        "use_cases": [
            "LinkedIn's user data storage",
            "High-throughput key-value needs"
        ]
    }
}
```


```
# ═════════════════════════════════════════════════════════════════════════════
#  COMPARISON TABLE
# ═════════════════════════════════════════════════════════════════════════════

COMPARISON = """
┌────────────────────┬─────────────┬──────────────────────────────────────┐
│ Database           │ CAP Choice  │ What Happens During Partition        │
├────────────────────┼─────────────┼──────────────────────────────────────┤
│ MongoDB            │ CP          │ Writes blocked until new primary     │
│ HBase              │ CP          │ Region unavailable until reassigned  │
│ Redis (wait)       │ CP          │ Writes blocked if replicas down      │
│ etcd               │ CP          │ Writes blocked if no quorum          │
│ ZooKeeper          │ CP          │ Minority partition read-only         │
│ Consul             │ CP          │ No writes without majority           │
│ Spanner            │ CP          │ Minority datacenter can't write      │
│ FoundationDB       │ CP          │ Database unavailable without quorum  │
├────────────────────┼─────────────┼──────────────────────────────────────┤
│ Cassandra          │ AP          │ Both sides accept writes, sync later │
│ DynamoDB           │ AP          │ Continues serving (eventual reads)   │
│ CouchDB            │ AP          │ Multi-master, resolves conflicts     │
│ Riak               │ AP          │ All nodes accept writes              │
│ Couchbase          │ AP          │ XDCR continues, conflicts resolved   │
│ Voldemort          │ AP          │ Decentralized, always available      │
└────────────────────┴─────────────┴──────────────────────────────────────┘


┌────────────────────────────────────────────────────────────────────────┐
│                        DECISION GUIDE                                  │
└────────────────────────────────────────────────────────────────────────┘

Choose CP (Consistency Priority) when:
  ✅ Data correctness is critical (financial, inventory, orders)
  ✅ Stale data causes real problems (e.g., double-spending)
  ✅ Can tolerate brief unavailability during failures
  ✅ Need ACID transactions across multiple records
  
  Examples:
    - Bank account balances → MongoDB, Spanner
    - Inventory counts → MongoDB, PostgreSQL (single node)
    - Order processing → MongoDB, FoundationDB
    - Kubernetes state → etcd
    - Distributed locks → ZooKeeper, Consul

Choose AP (Availability Priority) when:
  ✅ Downtime is unacceptable (user-facing systems)
  ✅ Eventual consistency is acceptable (social feeds, metrics)
  ✅ High write throughput required (IoT, analytics)
  ✅ Multi-datacenter writes needed
  
  Examples:
    - IoT sensor data → Cassandra
    - Social media timelines → Cassandra, DynamoDB
    - Shopping carts → DynamoDB
    - Time-series metrics → Cassandra
    - Content delivery → CouchDB, Couchbase
```


# ═════════════════════════════════════════════════════════════════════════════
#  INTERVIEW TALKING POINTS
# ═════════════════════════════════════════════════════════════════════════════

```
INTERVIEW_POINTS = """
KEY INTERVIEW ANSWERS:

Q: "Give examples of CP databases"
A: "MongoDB with majority write concern, etcd (used by Kubernetes), ZooKeeper,
    Google Spanner, HBase, FoundationDB. These prioritize consistency over
    availability — they'll reject writes during network partitions rather
    than risk serving stale data. For example, etcd requires a quorum of
    nodes to be reachable for writes, and if that quorum is lost, it becomes
    read-only until the partition heals."

Q: "Give examples of AP databases"
A: "Cassandra, DynamoDB (with eventual consistency), Riak, CouchDB. These
    prioritize availability — they continue accepting reads and writes even
    during network partitions, and use techniques like last-write-wins or
    vector clocks to resolve conflicts after the partition heals. For example,
    Cassandra with consistency level ONE will write to any available node
    and sync later, ensuring the system stays up even if most nodes fail."

Q: "Can you tune CAP behavior?"
A: "Yes, some databases let you tune per-query. DynamoDB offers eventual vs
    strong consistency reads. Cassandra's consistency level (ONE, QUORUM, ALL)
    lets you choose: ONE is AP (fast, less consistent), ALL is CP (slow,
    strongly consistent). This gives flexibility — you might use strong
    consistency for financial transactions but eventual for analytics."

Q: "What about PostgreSQL / MySQL?"
A: "Traditional single-node SQL databases are CA (Consistent + Available) but
    NOT partition tolerant. Once you add replication for partition tolerance,
    you become either CP (synchronous replication, writes block if replica
    down) or AP (asynchronous replication, replicas might lag). Most production
    setups use async replication, making them AP-ish."

Q: "Is MongoDB CP or AP?"
A: "MongoDB is CP by default when using write concern 'majority' and read
    concern 'majority'. During a partition, if the primary becomes unreachable,
    writes are blocked until a new primary is elected. However, if you use
    write concern 'w:1' and read from secondaries without concern, you can
    get AP behavior with eventual consistency. So it's tunable, but designed
    as CP by default."

Q: "When would you choose AP over CP?"
A: "When availability is more critical than immediate consistency. Examples:
    - Social media feeds (okay if posts appear out of order briefly)
    - IoT metrics (losing a few data points is acceptable, but downtime isn't)
    - Shopping carts (temporary inconsistency is fine, losing the cart isn't)
    - Global CDN (serve stale content rather than fail to serve)
    
    If stale data causes real problems (bank balances, inventory, seat
    reservations), choose CP instead."
```




# Note


# Reference

