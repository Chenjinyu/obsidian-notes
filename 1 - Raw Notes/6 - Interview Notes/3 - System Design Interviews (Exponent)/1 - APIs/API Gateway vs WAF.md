Date: 2026-02-18
Course:
Tags: [[API Gateway]] [[Firewall]]

# Content

## One-line distinction (memorize this)
- **API Gateway** = _how requests are routed, shaped, and managed_
- **WAF** = _which requests are allowed or blocked_
They are **complementary**, not interchangeable.

---

## What an API Gateway does
Think of **Amazon API Gateway** as the **front door manager for APIs**.
### Core responsibilities
API Gateway focuses on **API management and behavior**:
1. **Routing**
    - `/login` → auth service
    - `/messages` → chat service
    - `/users/{id}` → user service
2. **Request/response transformation**
    - Change headers
    - Rewrite paths
    - Map request formats (REST ↔ backend)
3. **Authentication & authorization**
    - JWT validation
    - IAM auth
    - Cognito integration
    - API keys
4. **Rate limiting & quotas**
    - 100 req/sec per user
    - Daily usage limits
    - Burst control
5. **Protocol handling**
    - REST
    - HTTP
    - WebSocket
    - gRPC (via HTTP APIs)
6. **Observability**
    - Metrics per endpoint
    - Latency tracking
    - Error rates

### What API Gateway is _not_
- Not a security firewall
- Not good at blocking attacks like SQL injection
- Not designed for DDoS filtering

---

## What a WAF does
Think of **AWS WAF** as a **bouncer with a rulebook**.
### Core responsibilities
WAF focuses on **security filtering**:
1. **Block malicious patterns**
    - SQL injection
    - XSS (cross-site scripting)
    - Command injection
2. **IP-based rules**
    - Block known bad IPs
    - Allow only certain countries
    - Allowlist your office IPs
3. **Rate-based blocking**
    - “If one IP sends 5,000 requests in 5 minutes → block”
4. **Bot & scraper protection**
    - Credential stuffing
    - Bad bots
    - Fake user agents
5. **Managed rule sets**
    - AWS-managed OWASP rules
    - No custom code required

### Where WAF attaches
WAF sits **in front of**:
- **Amazon CloudFront**
- Application Load Balancer
- API Gateway

---
## Side-by-side comparison (clear separation)

| Aspect               | API Gateway    | WAF                |
| -------------------- | -------------- | ------------------ |
| Primary role         | API management | Security filtering |
| Knows API structure  | ✅ Yes          | ❌ No               |
| Blocks SQL injection | ❌ No           | ✅ Yes              |
| Auth (JWT, IAM)      | ✅ Yes          | ❌ No               |
| Rate limiting        | Per API/user   | Per IP / pattern   |
| DDoS mitigation      | ❌ No           | ✅ Partial          |
| Request shaping      | ✅ Yes          | ❌ No               |
| Used by developers   | Mostly         | Rarely             |

---
## How they work together (best practice)
In a **proper AWS architecture**, they stack like this:
```
User
 ↓
CloudFront
 ↓
WAF  ← blocks bad traffic
 ↓
API Gateway ← manages APIs
 ↓
Load Balancer / Lambda / Microservices
```

### Real example for your chat app
- **WAF**
    - Blocks bots trying to spam `/login`
    - Rate-limits abusive IPs
- **API Gateway**
    - Authenticates users
    - Routes `/messages` to chat service
    - Enforces per-user rate limits

---
## When you need one, the other, or both
### Use **only WAF** if:
- You already have ALB + microservices
- You just need protection
- No complex API logic

### Use **only API Gateway** if:
- You’re exposing APIs publicly
- You need auth, routing, quotas
- You trust upstream protection

### Use **both** (recommended for production)
- Public-facing APIs
- Mobile or web clients
- Anything with login, payments, or chat

---

## Straight advice (no fluff)
If your app is:
- **Internal** → ALB + WAF is often enough
- **Public internet** → API Gateway + WAF is the grown-up choice
- **Chat/messenger app** → You _will_ want WAF eventually (bots are relentless)

# Note


# Reference

