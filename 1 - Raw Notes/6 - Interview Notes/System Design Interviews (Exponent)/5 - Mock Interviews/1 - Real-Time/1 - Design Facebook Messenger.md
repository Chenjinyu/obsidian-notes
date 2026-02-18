Date: 2026-02-17
Course: https://www.tryexponent.com/courses/system-design-interviews/facebook-messenger-whatsapp
Tags: [[Mock Interview]]

# Content

The takeaways from the video:
1. list the features, like: real-time messaging, groups, online status, media uploads, read receipts, and notificaitons.
2. the requirements, like: high volume, low latency, scalable, Reliable, Secure.

the architecture choose:
1. CDN before connect to Load balancer
2. API Gateway / Load balancer connect to chat micro-services with scale policy.
3. chat micro-services use pub/sub queue to publish event to any other subscriber services. 
4. Database, choose cassandra, because based on the CAP theorem, the chat application needs availability more than consistency. so its AP pattern,
5. Cache layer to reduce latency. 

## One-line distinction (memorize this)
- **API Gateway** = _how requests are routed, shaped, and managed_
- **WAF** = _which requests are allowed or blocked_
They are **complementary**, not interchangeable.
# Note
- [[../../1 - APIs/API Gateway|API Gateway]]
- 
# Reference

