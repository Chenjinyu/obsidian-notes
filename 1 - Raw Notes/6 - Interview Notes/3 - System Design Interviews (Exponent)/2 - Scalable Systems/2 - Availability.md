Date: 2026-01-29
Course: https://www.tryexponent.com/courses/system-design-interviews/reliability-strategies
Tags:  [[interview]] [[System Design Interview]] [[Availability]]

# Content

An **available system** is _able to perform its functionality_. This seems obvious; who would ever deploy a system that doesn't do its job? In reality, things are more complicated. **High availability (HA)** is difficult to achieve for two reasons.
1. Scaling, or building a system to accommodate changes in traffic, is hard.
2. Networks and hardware will fail.

Availability is usually reported as a percentage of uptime / total time. It's impossible to guarantee 100% availability, but most cloud providers include a high availability guarantee — something approaching the highly-coveted 'five nines', or 99.999% availability — in their service level agreements (SLAs.)

> **Tip:** Remember that although **availability** and **reliability** are related, _they are not the same_. Reliability implies availability, but availability doesn't imply reliability. That said, much of the strategies below are also helpful in [improving system reliability](https://www.tryexponent.com/courses/system-design-interview/fundamentals-system-design/reliability-strategies), so don't be afraid to use them as such.

In your system design interviews, you may be asked a follow-up question around increasing your system's availability. Here are a few effective strategies to consider.
## Rate Limiting[](https://www.tryexponent.com/courses/system-design-interviews/availability-strategies#rate-limiting)
Rate limiting refers to capping the number of times an operation can occur within an interval. The main reason you'd want to impose rate limiting is to protect your service from overuse - intentional or not. You may wonder "how does rate-limiting requests improve availability if we're dropping requests?" It's important to note that you're not rejecting _all_ requests good and bad. You're simply capping usage by particular users, organizations, IP addresses, etc... sometimes even other parts of your system.
It's possible to enforce rate limits on both the client and server-side. Doing this will minimize latency, maximize throughput, and help manage traffic and avoid the excess cost.
#### Use cases
- Prevent an autoscaling component from running over budget.
- Preserve the availability of a public API given a DoS attack or accidental overuse.
- Help SaaS providers control access and cost on a per-customer basis.
#### Techniques & considerations
- **Token bucket:** A token bucket strategy recognizes that not all requests require equal "effort." When a request is made, the service attempts to withdraw a certain number of tokens in order to fulfill the request. A request that requires multiple operations may "cost" multiple tokens. If the bucket is empty, the service has reached its limit. Tokens are replenished at a fixed rate, allowing the service to recover.
- A **leaky bucket** works similarly. Requests are "held" in a bucket. Each new request fills the bucket higher and higher. When the bucket is full (and the limit has been reached), new requests are discarded, or leaked.
- **Fixed and sliding window:** Fixed window rate limiting is simplicity itself - for example, 1000 requests per 15-minute window. Spikes are possible, as there's no rule preventing all 1000 requests from coming in within the same 30 seconds. Sliding window "smooths" the interval. Instead of 1000 requests every 15 minutes, you might define a rule such as 15 requests _within the last_ 30 seconds.
## Queue-Based Load Leveling[](https://www.tryexponent.com/courses/system-design-interviews/availability-strategies#queue-based-load-leveling)
Like rate-limiting, queue-based load leveling is a strategy to protect against service overuse. Instead of dropping requests like rate-limiting does (another way to think about rate-limiting is load _"shedding"_), load _leveling_ introduces intentional latency.
The problem is most pronounced in cases where multiple tasks demand the same service _concurrently_. System load can be hard to predict under these circumstances, and if the service becomes overloaded it may fail. In queue-based load leveling, the solution is to decouple the task(s) and service(s) and introduce a **queue** between the two. A simple message queue will store requests and pass them to the service in an orderly fashion.
A drive-through is the perfect real-world analog for queue-based load leveling. As a restaurateur, you wouldn't try to serve 1000 customers who've all arrived at the same time. Instead, cars are funneled through a queue in a FIFO (first-in-first-out) fashion.

#### Use cases
Consider this strategy anytime a service is:
- susceptible to overloading
- higher latency is acceptable during spikes, and
- it's important that requests are processed in order.

#### Techniques & considerations
Be careful when designing your queue and be mindful of the limitations of your downstream service. Queue depth, message size, and rate of response are all important considerations depending on the rest of your system.
Also, this strategy assumes it's easy to decouple tasks from services. In legacy or monolithic architecture this might not be the case.
## Gateway Aggregation[](https://www.tryexponent.com/courses/system-design-interviews/availability-strategies#gateway-aggregation)
Another strategy for dealing with complicated requests, or decreasing client-backend "chattiness" Is to introduce a gateway in front of the backend service. The gateway aggregates requests and dispatches them accordingly before collecting results and sending them back to the client.
#### Use cases
- Cut down on cross-service "chatter", especially in microservice architecture where operations require coordination between many small services.
- Decrease latency (if your service is complex and users already rely on high latency networks like mobile.)
#### Techniques & considerations
Gateways are simple, but if yours isn't designed well you'll have built a potential point of failure. Make sure your gateway can handle the anticipated load and scale as you grow. Implement reliable design techniques like [circuit breakers or retries](https://www.tryexponent.com/courses/system-design-interview/fundamentals-system-design/reliability-strategies) and be sure to load test the gateway. If it performs multiple functions, you might want to add an aggregation service in front of the gateway, freeing it up to perform its other functions and route requests correctly and quickly.

## Fundamentals review[](https://www.tryexponent.com/courses/system-design-interviews/availability-strategies#fundamentals-review)
If you haven't already, check out the following lessons on system design fundamentals that relate to system availability.

- [Web Protocols](https://www.tryexponent.com/courses/system-design-interview/fundamentals-system-design/web-protocols)
- [Load Balancers](https://www.tryexponent.com/courses/system-design-interview/fundamentals-system-design/load-balancers)
- [APIs](https://www.tryexponent.com/courses/system-design-interview/fundamentals-system-design/system-design-apis)
- [Replication](https://www.tryexponent.com/courses/system-design-interview/fundamentals-system-design/replication)
- [Authentication and Authorization](https://www.tryexponent.com/courses/system-design-interview/fundamentals-system-design/authentication-authorization)
- [Cloud Architecture](https://www.tryexponent.com/courses/system-design-interview/fundamentals-system-design/cloud-architecture)

# Note


# Reference

