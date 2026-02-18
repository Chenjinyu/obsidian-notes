Date: 2026-01-29
Course: https://www.tryexponent.com/courses/system-design-interviews/system-design-apis
Tags: [[API]] [[interview]] [[System Design Interview]]

# Content
Although APIs offer security to the systems on either end, they are susceptible to overuse or abuse. If you're concerned about this, you may want to implement an _API gateway_ to collect requests and route them accordingly.

An API gateway is a reverse proxy that acts as a single entry point for microservices and back-end APIs.
![](assets/API%20Gateway/file-20260129233216883.png)
All client requests are routed to the gateway, which directs them accordingly—to the API if it is available, or redirected if the request fails to meet security standards.

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

# Note


# Reference

