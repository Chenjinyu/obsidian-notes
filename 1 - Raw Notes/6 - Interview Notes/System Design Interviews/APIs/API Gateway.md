Date: 2026-01-29
Course: https://www.tryexponent.com/courses/system-design-interviews/system-design-apis
Tags: [[API]] [[interview]] [[System Design Interview]]

# Content
Although APIs offer security to the systems on either end, they are susceptible to overuse or abuse. If you're concerned about this, you may want to implement an _API gateway_ to collect requests and route them accordingly.

An API gateway is a reverse proxy that acts as a single entry point for microservices and back-end APIs.
![](assets/API%20Gateway/file-20260129233216883.png)
All client requests are routed to the gateway, which directs them accordingly—to the API if it is available, or redirected if the request fails to meet security standards.

Generally, use cases for API gateways include _user authentication_, _rate limiting_, and _billing_ if you're monetizing an API.
# Note


# Reference

