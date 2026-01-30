# Popular System Design Interview Questions

Here are some popular system design interview questions:

## Core System Design Questions

1.  **Design a URL Shortener (e.g., TinyURL).**
    *   Requirements: Shorten long URLs, redirect to original URL, custom URLs, analytics (optional).
    *   Considerations: Hash function, collision resolution, database schema, scaling, availability.

2.  **Design a Distributed Cache (e.g., Memcached, Redis).**
    *   Requirements: Key-value store, high read/write throughput, consistency models.
    *   Considerations: Data partitioning, consistency (eventual vs. strong), eviction policies, fault tolerance, replication.

3.  **Design a Chat Application (e.g., WhatsApp, Facebook Messenger).**
    *   Requirements: One-on-one chat, group chat, message delivery, online/offline status, push notifications.
    *   Considerations: Real-time communication (WebSockets), message storage, scalability, notification service, client-server interaction.

4.  **Design a Ride-Sharing Service (e.g., Uber, Lyft).**
    *   Requirements: Matching riders and drivers, real-time location tracking, fare calculation, payment processing.
    *   Considerations: Geospatial indexing, matching algorithms, real-time updates, scalability, fault tolerance.

5.  **Design a News Feed System (e.g., Facebook, Twitter).**
    *   Requirements: Personalize feed, publish posts, view posts, handle large fan-outs.
    *   Considerations: Feed generation (pull vs. push), data consistency, storage, caching, ranking algorithms.

6.  **Design a Global Image Sharing Platform (e.g., Instagram, Flickr).**
    *   Requirements: Upload images, view images, add filters, follow users, generate feed.
    *   Considerations: Storage (BLOBs), image processing (thumbnail generation), content delivery networks (CDNs), metadata storage, scaling uploads/downloads.

7.  **Design a Video Streaming Service (e.g., Netflix, YouTube).**
    *   Requirements: Upload video, transcode video, stream video, search, recommendations.
    *   Considerations: Large file storage, video encoding/transcoding, CDNs, adaptive bitrate streaming, content recommendation systems.

8.  **Design an API Rate Limiter.**
    *   Requirements: Limit requests per user/IP/API key, prevent abuse.
    *   Considerations: Algorithms (token bucket, leaky bucket), distributed counters, storage for rate limit data.

9.  **Design a Notification System.**
    *   Requirements: Send notifications (email, SMS, push), handle different types of notifications, queuing.
    *   Considerations: Message queues, templates, fan-out, reliability, idempotency.

10. **Design a Web Crawler.**
    *   Requirements: Discover new URLs, download content, handle duplicates, politeness.
    *   Considerations: URL frontier, distributed fetching, parsing, data storage, robots.txt, politeness policies.

## Scalability and Reliability Questions

1.  **How would you scale a read-heavy application?**
2.  **How would you scale a write-heavy application?**
3.  **Describe different database scaling strategies (sharding, replication).**
4.  **How do you handle failures in a distributed system?**
5.  **Explain eventual consistency vs. strong consistency.**
6.  **What are common trade-offs in distributed systems (CAP theorem)?**

## Specific Component Design Questions

1.  **Design a Load Balancer.**
2.  **Design a Distributed ID Generator.**
3.  **Design an Authentication System (SSO, OAuth).**
4.  **Design a Search Engine (simplified).**

This list covers a range of common system design patterns and challenges encountered in real-world systems.