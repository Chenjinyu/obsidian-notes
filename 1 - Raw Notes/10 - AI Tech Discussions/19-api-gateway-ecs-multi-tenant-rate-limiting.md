---
sr-due: 2026-10-26
sr-interval: 1
sr-ease: 2.5
---

# API Gateway, ECS, Multi-Tenant Rate Limiting and Resilience

Discussion summary — 2026-10-25/26. Examples are illustrative.

## Real-world use cases

| Scenario | Problem | Design |
|---|---|---|
| Enterprise Order API | Ten client applications share one company's contractual quota | JWT tenant identity + shared Redis tenant bucket |
| SaaS plan upgrade | Raise Tenant A from 1,000 to 5,000 RPS without redeploy | Registry update, cache invalidation/TTL |
| Noisy-neighbor workload | Tenant A's CPU-heavy calls starve Tenant B | Tenant concurrency limits, bulkheads, admission control |
| Flash-sale spike | Traffic outruns ECS and database capacity | Edge throttling, load shedding, autoscaling |
| Redis outage | Rate-limit state unavailable | Controlled fail-open, conservative local limits; fail-closed for critical operations |
| New tenant onboarding | Tenant C joins an existing shared ECS cluster | Register tenant; existing tasks load configuration on first request |

## 1. Why API Gateway if FastAPI already runs on ECS?

FastAPI provides REST-style endpoints and business logic. ECS runs containers. ALB routes traffic to healthy targets. API Gateway is **optional**: a managed API front door for supported authentication/authorization integration, API routing, throttling and API management. ALB + FastAPI can be sufficient, particularly if shared libraries and application middleware already cover requirements.

| Component | Responsibility | Important limitation |
|---|---|---|
| API Gateway | API front door, authorizers, managed throttling | No arbitrary native per-JWT-tenant token buckets |
| ALB | Distribute requests among healthy ECS targets | Does not recognize newly registered tenants or create tasks |
| ECS/FastAPI | Business logic and application admission checks | Instances do not share in-memory counters |
| Redis | Shared atomic token-bucket state | Availability and state consistency must be designed |
| Tenant Registry | Tenant status, plan, quotas, config version | Not a per-request counter |
| ECS Service Auto Scaling | Adjust desired task count using workload metrics | Does not scale just because a tenant registered |

Typical flow: Client → API Gateway (optional) → ALB/VPC integration → ECS FastAPI → dependencies. Details of API Gateway integrations differ between HTTP and REST API products.

## 2. CIDR, API Keys, OAuth and JWT

**CIDR:** `192.168.0.0/20` represents an IP range. WAF IP sets can allow/deny known public egress networks, but IP/CIDR is a weak primary tenant identity because of NAT, VPNs, dynamic IPs and shared networks.

**API Keys:** API Gateway **REST API** usage plans can associate API keys with throttling and quotas, but enforcement is **best-effort**. An API key is not sufficient authentication. Ten keys do not necessarily mean ten tenants.

**OAuth/JWT:** A tenant can have many OAuth clients. A confidential client may use Client ID and Client Secret to request an access token from an authorization server. The secret is **not** placed inside the JWT. A signed JWT can carry a trusted custom `tenant_id` claim and `scope`, along with `iss`, `aud`, `exp`, `sub`. Validate signature, issuer, audience, expiration and required scopes: **decoding is not verification**.

Example illustrative claims:

```json
{"sub":"client-123","tenant_id":"tenant-A","scope":"orders:read orders:write","iss":"https://auth.example.com","aud":"orders-api","exp":1793000000}
```

API Gateway HTTP API JWT Authorizer can validate supported token properties and scopes, but does **not** dynamically maintain one bucket per arbitrary JWT `tenant_id`.

## 3. Token Bucket, RPS and client fairness

Token Bucket has **capacity** (burst size), **refill rate** (sustained rate), and **current balance**. Each admitted request spends a token. When empty, return HTTP **429** immediately; requests are **not automatically queued**. Clients may retry with backoff/jitter, or jobs can explicitly enter a durable queue.

Example: capacity 100, refill 10 tokens/s, 150 simultaneous requests. An ideal atomic bucket admits up to 100 immediately; the other 50 are rejected, not held for five seconds. Gateway's best-effort throttling should not be described as an exact admission guarantee.

**Correct key:** `rate_limit:tenant-A`, not `rate_limit:client-id`, when the contract limits Tenant A's **aggregate** requests across its ten OAuth clients.

Optionally enforce **hierarchical limits**:
- Tenant A total: 1,000 RPS.
- Each client: at most 300 RPS to reduce internal monopolization.

Strictly allocating 10% to each of ten clients can waste idle capacity. Client ceilings plus a shared tenant ceiling improve utilization; guaranteed minimum shares require reservations or weighted-fair scheduling. Check and debit both buckets **atomically** (e.g., Redis Lua script) to avoid races and partial deductions.

**RPS is not concurrency:** A tenant below its 1,000 RPS quota can still saturate CPU with 30-second expensive requests. Protect with per-tenant concurrency limits, bulkheads/isolated worker pools, bounded queues and load shedding. Autoscaling is not instantaneous and cannot by itself rescue an overloaded database.

## 4. Control plane vs data plane: how tenant config reaches ECS

**Control plane:** Tenant Management API (which can itself run on ECS) registers/updates tenants in PostgreSQL or DynamoDB. Tenant Registry is the source of truth for `tenant_id`, active status, plan, quota and version. It may emit `TenantCreated` or `TenantConfigurationUpdated` events.

**Data plane:** ALB routes any incoming request to an existing healthy ECS Task. The application obtains a **verified** Tenant ID from authentication context, looks in its local cache, then shared configuration cache/registry on a miss, caches the result and processes the request.

**No new ECS Task is required when Tenant C registers.** Tasks do not need to poll or preload the entire registry. Config is fetched **on demand**.

**Updates:** Use TTL and/or event-driven invalidation. EventBridge, SNS or Kafka can notify appropriate consumers; a **single SQS queue with competing consumers does not broadcast each message to all ECS Tasks**. Use proper fan-out or shared-cache invalidation, with TTL/version checks as recovery. Disabled tenants and security-sensitive changes need stricter freshness and authorization safeguards than a routine quota upgrade.

Distinct responsibilities: JWT identifies **which tenant** sent the request; registry defines **how that tenant is handled**; Redis holds **shared live admission state**.

## 5. Who launches more ECS Tasks?

**ALB** only routes requests to healthy targets. **ECS Service Auto Scaling** uses CloudWatch/scaling policies (CPU, memory, suitable ALB request metrics or custom signals) to adjust service desired count. ECS starts tasks and registers healthy ones with the target group.

New tenant registration **does not** automatically scale ECS. A single very busy tenant might trigger scale-out; 1,000 idle tenants might not. An explicit TenantCreated → EventBridge → Lambda/controller → ECS UpdateService integration is possible for **proactive capacity planning**, but is not the default.

## 6. Redis failure: controlled fail-open, fail-closed and recovery

**Unrestricted fail-open** sends all requests to ECS and may overwhelm databases before autoscaling catches up.

For suitable low-risk reads, use **controlled fail-open**:
1. Set a short Redis timeout; avoid tying up all request workers.
2. Fall back to conservative in-process per-tenant token buckets with small/empty initial burst.
3. Add per-task concurrency limits, load shedding, monitoring and alerts.
4. Restore shared Redis admission when healthy.

For critical payment, inventory mutation, security-sensitive or strictly metered operations, consider **fail-closed** or independent authoritative safeguards. An HTTP GET is not automatically cheap or harmless.

**Approximate fallback example:** Tenant A has 1,000 RPS and five healthy tasks. Provisionally allow ~200 RPS per task. Uneven ALB distribution may cause rejections despite spare capacity. If the cluster scales to ten tasks while stale local limits remain at 200, aggregate traffic may reach ~2,000 RPS. Task restarts can reset burst balances. Cached task counts, conservative budgets and safety margins help, but **independent local buckets cannot guarantee a strict global quota without coordination**.

**AWS failure domains:** For Redis node/AZ failures, configure suitable same-region Multi-AZ replication/failover. Cross-region disaster recovery is a separate design: replication lag, failover orchestration, connection routing and lost token-bucket state all matter. Same-region automatic failover does not imply seamless cross-region failover.

## 7. Interview questions and answers

**Why API Gateway when FastAPI + ECS + ALB already works?** Optional centralized API management and policies; not mandatory.

**Can I use CIDR as tenant identity?** Only as supplemental network filtering for known public ranges; use verified claims for identity.

**Can Gateway directly rate-limit by JWT tenant_id?** Not as an arbitrary built-in dynamic token bucket. REST API usage plans work by API key, best-effort; custom shared limiter can work by tenant ID.

**Ten Client IDs for Tenant A: one bucket or ten?** One tenant bucket for aggregate quota, optionally layered client ceilings.

**How does an ECS Task discover Tenant C?** First request supplies verified Tenant ID; task loads configuration on cache miss. No redeploy or tenant-specific task.

**Who scales ECS?** ECS Service Auto Scaling reacts to workload policies, not the ALB detecting new tenants.

**What if Redis is down?** Controlled fail-open with conservative local admission and concurrency caps where appropriate; fail-closed where correctness demands.

**Can local buckets enforce an exact global rate?** Not across changing task membership without shared coordination.

## 8. Staff Engineer interview summary (English)

> I separate the control plane from the data plane. The Tenant Management API stores tenant configuration in a registry, while ECS Tasks load configuration on demand using cache-aside and versioned invalidation. The ALB distributes traffic; ECS Service Auto Scaling adjusts capacity based on workload, not registrations. I validate the caller's JWT and use its verified tenant ID as the key for an atomic Redis-backed token bucket, ensuring all clients of a tenant share one quota. I add client ceilings, concurrency limits and bulkheads as needed. If Redis fails, I use a policy-driven controlled fail-open with conservative local budgets for suitable endpoints, and fail-closed or stronger safeguards for critical operations. I acknowledge that independent local buckets cannot guarantee an exact global quota.

**Memorable line:** “During a dependency failure, I prioritize backend protection over perfect quota utilization.”

## Related notes

- [REST APIs](01-rest-apis.md)
- [Caching and Coordination](08-caching-and-coordination.md)
- [Traffic Management and Resilience](16-traffic-management-and-resilience.md)
- [Message Queues](13-message-queues.md)
