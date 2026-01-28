Date: 2026-01-27
Course: https://www.tryexponent.com/courses/system-design-interviews/system-design-glossary
Tags: 

# Content

# System Design Glossary

This glossary covers fundamental system design concepts to help you communicate technical ideas clearly in interviews. Don't memorize definitions—focus on understanding how concepts connect so you can reason about trade-offs and explain your design decisions effectively.

## Communication & Networking[](https://www.tryexponent.com/courses/system-design-interviews/system-design-glossary#communication-networking)

_Understanding how services communicate is fundamental to system design. These concepts cover the protocols, patterns, and performance characteristics that enable distributed systems to exchange data efficiently and reliably._

**API (Application Programming Interface)**: Think of this as the way a software system interacts with other systems/people. Specifies available requests, data formats, and expected responses. Modern APIs typically use REST or GraphQL over HTTP.

**API Gateway**: Entry point for API requests. Handles authentication, rate limiting, request routing, and response transformation. Acts as a single interface to multiple microservices.

**Bandwidth**: Maximum rate of data transfer across a network. Measured in bits per second (Mbps, Gbps). Often confused with throughput—bandwidth is capacity while throughput is actual usage.

**DNS (Domain Name System)**: Translates domain names into IP addresses. Hierarchical system with caching at multiple levels. Supports load balancing and geographic routing. DNS propagation can take 24-48 hours (TTL), affecting deployment strategies.

**GraphQL**: Query language for APIs allowing clients to request exactly the data they need. Unlike REST, a single endpoint handles all requests. Reduces over-fetching and under-fetching but adds server complexity.

**HTTP/HTTPS**: Protocol for transmitting web data. HTTPS adds SSL/TLS encryption for security. Understanding status codes (200, 404, 500), headers, and methods is essential for API design.

**Latency**: Time delay between request and response. Affected by network distance, processing time, and database queries.

**REST/RESTful**: Architectural style using standard HTTP methods (GET, POST, PUT, DELETE) for stateless communication. Resources identified by URLs, responses typically in JSON. Stateless nature enables easy scaling since servers don't maintain session data between requests.

**Throughput**: Amount of data processed in a given time period. Often measured in requests per second (RPS) or queries per second (QPS). Distinct from latency—you can have high throughput with high latency.

**WebSocket**: Protocol providing full-duplex communication channels over a single TCP connection. Used for real-time features like chat, live updates, or gaming where low-latency bidirectional communication is needed.

Note

To learn more, refer to our lessons on [Web Protocol](https://www.tryexponent.com/courses/software-engineering/system-design-interviews/web-protocols) and [APIs](https://www.tryexponent.com/courses/software-engineering/system-design-interviews/system-design-apis).

## Architecture Patterns[](https://www.tryexponent.com/courses/system-design-interviews/system-design-glossary#architecture-patterns)

_System architecture determines how components are organized and interact. These patterns represent common approaches to structuring applications, from traditional client-server models to modern distributed architectures._

**Backend**: Server-side code handling business logic, data processing, and database operations. Languages: Python, Java, Node.js, Go, Ruby. Often organized into multiple layers or services.

**Client**: Initiates requests to servers. Examples include web browsers, mobile apps, and IoT devices. Contains presentation logic and user interface code.

**Cookie**: Small text file stored by browser to maintain state across stateless HTTP requests. Used for session management, personalization, tracking. Security considerations: httpOnly (prevents JavaScript access), secure (HTTPS only), SameSite (CSRF protection).

**Frontend**: Client-side code users interact with directly. Includes UI, styling, and client-side logic. Technologies: HTML, CSS, JavaScript, React, Vue, Angular.

**Microservices**: Architectural style organizing applications as collections of loosely coupled services. Each service handles specific business capability. Enables independent deployment and scaling but adds operational complexity and network overhead.

**Middleware**: Software layer between client and server or between different services. Examples: authentication middleware, logging, request parsing, error handling.

**Monolith**: Single unified application containing all functionality. Simpler to develop, test, and deploy initially. Becomes harder to scale and maintain as codebase grows, but suitable for many use cases.

**Native App**: Built specifically for a platform (iOS, Android) using platform-specific languages. Offers better performance, offline capabilities, and device feature access. Distributed through app stores.

**Proxy**: Intermediary server between clients and servers. Forward proxy acts on behalf of clients (hides client identity). Reverse proxy acts on behalf of servers (load balancing, caching, SSL termination).

**Server**: Responds to client requests with data or services. Runs business logic, handles authentication, and manages data. Can be specialized: web server (HTTP handling), application server (business logic), database server (data storage).

**Service-Oriented Architecture (SOA)**: Architectural pattern where services communicate over network. Broader and more established than microservices, typically using protocols like SOAP or REST.

**Session**: Period of user interaction with application. Session data can be stored server-side (session store like Redis) or client-side (cookies, JWT tokens). Trade-offs between security and scalability.

**SLA (Service Level Agreement)**: Contract specifying expected service quality between provider and customer. Includes metrics like uptime percentage, response time, support response time. Often includes penalties for violations.

**Web App**: Runs in browsers, accessed via URLs. Cross-platform by default, easier to update. Progressive Web Apps (PWAs) add offline capabilities and install-ability.

**Webhook**: HTTP callback triggered by specific events. Server makes POST request to configured URL when event occurs. Used for integrations and real-time notifications (e.g., payment confirmation, CI/CD pipelines).

Note

To learn more, refer to our lesson on [Cloud Architecture](https://www.tryexponent.com/courses/software-engineering/system-design-interviews/cloud-architecture).

## Data Storage[](https://www.tryexponent.com/courses/system-design-interviews/system-design-glossary#data-storage)

_Data storage decisions impact performance, consistency, and scalability. These concepts cover database types, data modeling strategies, and the fundamental trade-offs in distributed data systems._

**ACID Properties**: Atomicity (all-or-nothing transactions), Consistency (valid state transitions), Isolation (concurrent transactions don't interfere), Durability (committed data persists). Critical for financial systems and data integrity.

**CAP Theorem**: In distributed systems, you can only guarantee two of three: Consistency (all nodes see same data), Availability (system responds to requests), Partition Tolerance (system works despite network failures). Fundamental trade-off in distributed database design.

**CMS**: Content management system. This is a system for storing content, and is often hosted inside/used as a database.

**Database/DBMS**: Database management system. System for storing, retrieving, and managing data. Handles CRUD operations (Create, Read, Update, Delete). Key considerations: indexing, replication, backup strategies.

**Data Warehouse**: Centralized repository optimized for analysis and reporting. Stores historical data from multiple sources. Examples: Snowflake, BigQuery, Redshift.

**Data Lake**: Storage repository holding vast amounts of raw data in native format. More flexible than data warehouses but requires more processing for analysis.

**Denormalization**: Adding redundancy to improve read performance. Common in NoSQL and data warehouses. Trades storage and update complexity for faster queries by reducing joins.

**Indexing**: Data structure improving query speed at cost of write performance and storage. Like a book index, allows database to find data without scanning entire table. Common types: B-tree, hash, full-text.

**NoSQL Database**: Non-relational databases offering flexibility and horizontal scaling. Types include document stores (MongoDB), key-value stores (Redis, DynamoDB), column-family (Cassandra), graph databases (Neo4j). Follows BASE model (Basically Available, Soft state, Eventually consistent).

**Normalization**: Organizing database to reduce redundancy. Involves splitting data into multiple related tables. Reduces storage but can slow queries requiring joins.

**Relational Database**: Organizes data into tables with rows and columns. Examples: PostgreSQL, MySQL, Oracle. Supports ACID properties ensuring data consistency. Best for structured data with complex relationships.

**Replication**: Copying data across multiple database servers. Master-slave (one writer, multiple readers) or multi-master (multiple writers). Improves availability, read performance, and disaster recovery.

**Sharding**: Horizontal partitioning of data across multiple database instances. Each shard contains subset of data (e.g., users 1-1M on shard 1, 1M-2M on shard 2). Enables linear scaling but complicates cross-shard queries and rebalancing.

**SQL (Structured Query Language)**: Language for managing relational databases. Used to query, update, and manipulate data in tables with defined schemas.

**Transaction**: Group of database operations executed as single unit. Either all succeed or all fail. Essential for maintaining data consistency in operations like money transfers or inventory management.

Note

To learn more, refer to our lessons on [CAP theorem](https://www.tryexponent.com/courses/software-engineering/system-design-interviews/cap-theorem), [SQL vs. NoSQL](https://www.tryexponent.com/courses/software-engineering/system-design-interviews/sql-nosql), [Database Sharding](https://www.tryexponent.com/courses/software-engineering/system-design-interviews/database-sharding), and [Replication](https://www.tryexponent.com/courses/software-engineering/system-design-interviews/replication).

## Caching & Performance[](https://www.tryexponent.com/courses/system-design-interviews/system-design-glossary#caching-performance)

_Caching is one of the most effective ways to improve system performance. These concepts explain how to store and retrieve frequently accessed data quickly, reducing latency and database load._

**Cache**: Fast storage layer (typically in-memory) for frequently accessed data. Reduces database load and latency. Strategies: write-through (write to cache and DB), write-back (write to cache, async to DB), cache-aside (check cache first). Key metric: cache hit ratio.

**Cache Invalidation**: Updating or removing stale data from cache. One of the hardest problems in computer science. Strategies include TTL-based, event-based, or manual purging.

**CDN (Content Delivery Network)**: Geographically distributed servers caching static content near users. Reduces latency and origin server load. Essential for global applications serving images, videos, or large files.

**Eviction Policy**: Rules for removing items when cache is full. LRU (Least Recently Used), LFU (Least Frequently Used), FIFO (First In First Out). Choice affects cache effectiveness.

**Redis/Memcached**: Popular in-memory data stores used for caching. Redis supports complex data structures, persistence, and pub/sub. Memcached is simpler, purely for caching, and extremely fast.

**TTL (Time To Live)**: Expiration time for cached data. Balances data freshness with cache effectiveness. Short TTL keeps data current but increases cache misses and load on origin.

Note

To learn more, refer to our lessons on [Caching](https://www.tryexponent.com/courses/software-engineering/system-design-interviews/system-design-caching) and [CDNs](https://www.tryexponent.com/courses/software-engineering/system-design-interviews/content-delivery-network).

## Scalability & Reliability[](https://www.tryexponent.com/courses/system-design-interviews/system-design-glossary#scalability-reliability)

_Building systems that handle growth and stay available under failure requires deliberate design choices. These concepts cover techniques for scaling horizontally, distributing load, and maintaining uptime._

**Availability**: Percentage of time system is operational. Measured in "nines": 99.9% (8.76 hours downtime/year), 99.99% (52.6 minutes/year), 99.999% (5.26 minutes/year). Achieved through redundancy, failover, and health monitoring.

**Circuit Breaker**: Design pattern preventing cascading failures. When service fails repeatedly, circuit "opens" and requests fail fast rather than waiting for timeout. Automatically "closes" after cooldown period to retry.

**Consensus Algorithm**: Protocol enabling distributed systems to agree on single value despite failures. Examples: Paxos, Raft. Foundation of distributed databases and coordination services like Zookeeper.

**Consistent Hashing**: Technique for distributing data across nodes that minimizes reorganization when nodes are added/removed. Essential for distributed caching and databases. Uses hash ring to map data to servers.

**Failover**: Automatic switching to redundant system when primary fails. Active-passive (backup waits idle until needed) or active-active (both handle traffic simultaneously). Critical for high availability.

**Horizontal Scaling**: Adding more machines to handle load (scaling out). Easier with stateless services. Most common cloud-native approach as it's theoretically unlimited.

**Load Balancer**: Distributes traffic across multiple servers to prevent overload. Layer 4 (transport/IP) or Layer 7 (application/HTTP) routing. Algorithms: round-robin, least connections, IP hash. Critical for horizontal scaling and availability.

**Rate Limiting**: Restricting number of requests users can make in time period. Prevents abuse and ensures fair resource usage. Implemented with token bucket or leaky bucket algorithms. Typically returns 429 status code when exceeded.

**Stateless vs Stateful**: Stateless services don't store session data between requests—easier to scale. Stateful services maintain session information—harder to scale but sometimes necessary.

**Vertical Scaling**: Adding resources (CPU, RAM, storage) to existing machines (scaling up). Simpler but limited by hardware maximums and requires downtime. Good for databases with strong consistency requirements.

Note

To learn more, refer to our lessons on [Consistent Hashing](https://www.tryexponent.com/courses/software-engineering/system-design-interviews/consistent-hashing), [Reliability](https://www.tryexponent.com/courses/software-engineering/system-design-interviews/reliability-strategies), [Availability](https://www.tryexponent.com/courses/software-engineering/system-design-interviews/availability-strategies), and [Load Balancing](https://www.tryexponent.com/courses/software-engineering/system-design-interviews/load-balancers).

## Messaging & Queues[](https://www.tryexponent.com/courses/system-design-interviews/system-design-glossary#messaging-queues)

_Asynchronous communication enables systems to handle varying workloads and decouple services. These patterns are essential for building resilient, event-driven architectures._

**Message Queue**: Asynchronous communication system where producers send messages that consumers process later. Examples: RabbitMQ, Apache Kafka, AWS SQS. Enables service decoupling, handles traffic spikes, and provides retry mechanisms.

**Pub/Sub (Publish-Subscribe)**: Messaging pattern where publishers send messages to topics, and subscribers receive messages from topics they're interested in. Decouples senders and receivers. Used in event-driven architectures.

Note

To learn more, refer to our lesson on [Asynchronous Processing](https://www.tryexponent.com/courses/software-engineering/system-design-interviews/asynchronous-processing).

## Security[](https://www.tryexponent.com/courses/system-design-interviews/system-design-glossary#security)

_Protecting user data and system resources is non-negotiable. These concepts cover authentication, authorization, and encryption—the foundations of secure system design._

**Authentication**: Verifying user identity. Methods: passwords, OAuth, SSO (Single Sign-On), multi-factor authentication (MFA), biometrics. Answers "who are you?"

**Authorization**: Determining what authenticated users can access. Often implemented with RBAC (role-based access control) or ABAC (attribute-based access control). Answers "what can you do?"

**CORS (Cross-Origin Resource Sharing)**: Security feature controlling which domains can access resources. Browsers enforce CORS to prevent malicious sites from making unauthorized requests to APIs.

**Encryption**: Converting data to unreadable format. Symmetric (same key encrypts/decrypts, faster) or asymmetric (public/private key pairs, more secure for key exchange). Essential for data in transit (TLS) and at rest (database encryption).

**JWT (JSON Web Token)**: Compact token format for securely transmitting information between parties. Self-contained (includes all necessary info), commonly used for stateless authentication. Contains header, payload, and signature.

**OAuth**: Open standard for token-based authorization. Allows third-party apps to access user data without sharing passwords. Used for "Sign in with Google/Facebook." Defines flows for different client types (web, mobile, server).

**SSL/TLS**: Protocols for secure communication over networks. TLS is modern version of SSL. Establishes encrypted connection between client and server, verifies server identity with certificates.

Note

To learn more, refer to our lessons on [Encryption](https://www.tryexponent.com/courses/software-engineering/system-design-interviews/encryption), [Authentication and Authorization](https://www.tryexponent.com/courses/software-engineering/system-design-interviews/authentication-authorization).

## Monitoring & Operations[](https://www.tryexponent.com/courses/system-design-interviews/system-design-glossary#monitoring-operations)

_Deploying and maintaining systems requires visibility and safe deployment practices. These concepts cover how to observe system health and roll out changes with minimal risk._

**Blue-Green Deployment**: Running two identical production environments. Deploy to inactive (green), test, then switch traffic from active (blue). Enables instant rollback if issues arise.

**Canary Deployment**: Gradually rolling out changes to small subset of users before full deployment. Monitor for issues with limited blast radius. Named after "canary in coal mine" early warning concept.

**Health Check**: Endpoint or mechanism indicating if service is functioning properly. Load balancers use health checks to route traffic only to healthy instances. Prevents cascading failures.

**Logging**: Recording system events for debugging, auditing, and analysis. Centralized logging systems (ELK stack: Elasticsearch, Logstash, Kibana; or Splunk) aggregate logs from distributed services.

**Monitoring**: Tracking system metrics (CPU, memory, disk, requests, errors, latency) to ensure health. Tools: Prometheus, Grafana, Datadog, New Relic. Essential for detecting issues before users are impacted.

## Data Processing[](https://www.tryexponent.com/courses/system-design-interviews/system-design-glossary#data-processing)

_Different data processing patterns suit different use cases. These concepts distinguish between processing data in real-time versus in batches, and the tools that enable each approach._

**Batch Processing**: Processing large volumes of data at scheduled intervals (hourly, daily, weekly). Example: generating daily reports, ETL jobs. Tools: Apache Hadoop, Spark. Optimizes for throughput over latency.

**ETL (Extract, Transform, Load)**: Process of extracting data from sources, transforming it (cleaning, aggregating, enriching), and loading into destination (typically data warehouse). Critical for analytics and reporting.

**Stream Processing**: Processing data in real-time as it arrives. Example: fraud detection, real-time analytics, monitoring. Tools: Apache Kafka, Flink, Storm, AWS Kinesis. Optimizes for low latency.

Note

Preparing for data engineering interviews? Check out our [data engineering interview prep course](https://www.tryexponent.com/courses/data-engineering) instead.

# Note


# Reference

