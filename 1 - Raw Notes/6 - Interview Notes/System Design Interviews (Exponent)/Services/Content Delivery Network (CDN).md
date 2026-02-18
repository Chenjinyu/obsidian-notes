Date: 2026-01-30
Course:
Tags: [[System Design Interview]]

# Content

A Content Delivery Network (CDN) is a geographically distributed network of servers that caches website content (images, HTML, videos) at "edge" locations close to users. By serving data from the nearest server, it dramatically improves speed, reduces latency, enhances reliability, and protects against traffic spikes or DDoS attacks. [[1]

### Popular CDN Providers
- Cloudflare
- Akamai
- Amazon CloudFront (AWS)
- Microsoft Azure CDN
- Fastly
- Google Cloud CDN 

Key Aspects of a CDN
- Edge Servers: Instead of users connecting to a single origin server, a CDN uses "Points of Presence" (PoPs - is a CDN’s **physical location** (a data center / edge site)) worldwide to deliver content.
- Caching Mechanism: The CDN caches (stores) static content like CSS, JavaScript, and images, reducing the need for the origin server to handle every request.
- Performance & Reliability: By minimizing the physical distance data travels, loading times are significantly faster. If one data center fails, traffic is routed to another, improving uptime.
- Security: Many CDNs provide security features like DDoS mitigation and Web Application Firewalls (WAF).
- 
Differences: Caching vs. CDN
- Caching: A general technique of storing data temporarily to reduce future requests. It can occur on a user's browser, a local server, or a network edge.
- CDN: A specific, global infrastructure that _uses_ caching as its primary mechanism to distribute content worldwide.

Benefits of Using a CDN
- Reduced Bandwidth Costs: By offloading traffic from the origin server, CDNs can reduce bandwidth usage by up to 80%.
- Better User Experience: Faster load times lead to higher engagement and lower bounce rates.
- Global Reach: Content is delivered rapidly regardless of the user's location. 

# Note


# Reference

