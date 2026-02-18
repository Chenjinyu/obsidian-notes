Date: 2026-01-29
Course: https://www.tryexponent.com/courses/system-design-interviews/reliability-strategies
Tags:  [[interview]] [[System Design Interview]] [High Level]

# Content

A **reliable** system can _perform its function_, _tolerate errors,_ and _prevent unauthorized access or abuse._ Reliability implies availability, but it's more than that. Building for reliability means added security, error-handling, disaster recovery, and countless other contingencies.

Why? Because things will fail. Whether due to network outages, hardware failure, a botched roll-out, or a malicious attack, any system with dependencies must include logic to deal with failures. Most failures in distributed systems come from either:

- **Hardware errors:** Network outages, server failure, etc. These won't be fixed quickly, and are often called **non-transient errors.**
- **Application errors:** Bugs, failure to accommodate spikes in traffic, etc. These should resolve quickly and are also known as **transient errors.**

It should logically follow that beefing up system reliability will have implications for **performance** and **cost** in terms of complexity, engineering time, and money. When implementing reliability techniques in an interview scenario, it's helpful to:

- Refer back to the requirements you've defined upfront. This will help you focus on mitigating the most important / most likely risks.
- Assume failures will happen, and design your system to recover gracefully (in alignment with predefined requirements) from the very beginning.
- Include testing strategies and monitoring techniques to help you benchmark your system in terms of requirements, monitor its health, and make changes as needed. We'll cover a few common strategies in a later lesson.

Here are a few effective reliability strategies to consider.

## Retries[](https://www.tryexponent.com/courses/system-design-interviews/reliability-strategies#retries)

Under a **simple retry** strategy, an application detecting a failure will immediately retry. This might work well if the failure detected is unusual and unlikely to repeat, but for common transient failures (e.g. network failures) repeat retries may overload the downstream system once the network issue is resolved. **Delayed retry** holds the retry back for a set amount of time allowing the system to recover. Many engineers implement an **exponential backoff strategy** that systematically decreases the rate of re-transmission in search of an acceptable retry rate.

#### Use cases

- Simple retry for unusual and transient errors. We recommend implementing some type of request limit to prevent overload.
- Delayed retries using exponential backoff for more common transient errors.

#### Techniques & considerations

Retry buildup in high-traffic systems can lead to extremely high system load once the error is resolved. This is called the **thundering herd** problem, and it can cause even more problems than the transient error as your resource(s) struggle to cope with the request volume. A simple solution is to introduce **jitter**, or "randomness" to the delay intervals so that client requests don't synchronize.

From a UX perspective, keep in mind that in some cases it's better to fail fast and simply let users know. In this case, implement a low retry limit and alert users that they'll need to try again later.

## Circuit Breakers[](https://www.tryexponent.com/courses/system-design-interviews/reliability-strategies#circuit-breakers)

A robust retry policy can alleviate short-lived transient errors... but what about non-transient errors? Or transient errors with uncertain recovery times?

While a retry pattern assumes that the operation will ultimately succeed, a **circuit breaker** accepts failure and stops the application from repeatedly trying to execute. This saves computing power and helps prevent the cascading failures we discussed above. Importantly, a circuit breaker has a built-in mechanism to test for whether a service has been restored unblock traffic accordingly. Circuit breakers can occupy a few states analogous to physical circuit breakers.

> **Remind me how a circuit breaker works?** Physical circuit breakers cut power as soon as they detect that an electrical system is not working properly. But unlike other failsafes, they're not single-use. Once the circuit has been repaired, you can simply flip the switch, and power is restored. A circuit breaker strategy works similarly. The breaker detects a problem, cuts off requests, and restores access when repairs are complete.

For example, let's say an application sends a request.

All is working well and the circuit breaker is in a **closed state**. It monitors the number of recent failures, and if this number exceeds a threshold within a given interval, the circuit breaker is set to **open**. No further requests are let through. A timer is set, giving the system time to fix the issue without receiving new requests. Once the timer expires, the circuit breaker is set to **half-open**; A few requests are allowed through to test the system. If all are successful, the breaker reverts to its closed state and the failure counter is reset. If _any_ requests fail, the breaker reverts to open and the timer starts again.

#### Use cases

- Prevents cascading failures when a shared resource goes down.
- Allows for a fast response in cases where performance and response time are critical (by immediately rejecting operations that are likely to timeout or fail).
- Circuit breakers' failure counters combined with event logs contain valuable data that can be used to identify failure-prone resources.

#### Techniques & considerations

There are a few main points to remember when implementing circuit breakers.

- You'll need to address exceptions raised when a resource protected with a circuit breaker is unavailable. Common solutions are to temporarily switch to more basic functionality, try a different data source, or to alert the user.
- Configure the circuit breaker in a way that makes sense for 1) the recovery patterns you anticipate, and 2) your performance and response time requirements. Setting the timer correctly can be nuanced. It may take some trial and error.

## Saga[](https://www.tryexponent.com/courses/system-design-interviews/reliability-strategies#saga)

Saga is a strategy used most often in microservice architecture where completing an action (also known as a **distributed transaction**) entails successfully completing a set of **local transactions** across multiple independent services. What if you encounter a failure halfway through? This type of failure can wreak havoc with your system.

Imagine you run an ecommerce site. When a customer buys an item, their cart is updated, their payment is charged, the item is pulled from inventory, shipped, and invoiced. If you fail to pull the item from inventory, you'll need to reverse the charge to your customer - but without any structured **compensating transactions** in place to reverse the transactions _that have already_ s_ucceeded_, you're stuck.

A saga is an alternate structure. Instead of a single distributed transaction, the component local transactions are decoupled, grouped, and executed sequentially. Each string of related local transactions is a saga. If your saga coordinator (more on that below) detects a failure, it invokes a predefined set of "countermeasures", effectively reversing the actions already taken. In the case of our ecommerce site, the inventory number would revert back to its previous state, and payment and cart updates would be reversed.

To implement a saga strategy, you can either coordinate saga participants via **choreography**, a decentralized approach where each local transaction triggers others, or **orchestration**, where a centralized controller directs saga participants.

#### Use cases

- Maintains data consistency across multiple services.
- Well-suited to any microservice application where **idempotency** (the ability to apply the same operation multiple times without changing the result beyond the first try) is important, like when charging credit cards.
- For microservices in which there aren't many participants or the set of counter transactions required is discrete and small consider choreographed saga as there's no single point of failure.
- For more complex microservices, consider orchestrated saga.

#### Techniques & considerations

Sagas can introduce quite a lot of complexity into your system. You'll have to build the set(s) of compensating transactions that are triggered by different failures. Depending on your application, this might require substantial work upfront to understand user behavior and potential failure modes.

## Fundamentals review[](https://www.tryexponent.com/courses/system-design-interviews/reliability-strategies#fundamentals-review)

If you haven't already, check out the following lessons on system design fundamentals that relate to system reliability.

- [Consistent Hashing](https://www.tryexponent.com/courses/system-design-interview/fundamentals-system-design/consistent-hashing)
- [CDNs](https://www.tryexponent.com/courses/system-design-interview/fundamentals-system-design/content-delivery-network) (Content Delivery Network)
- [Load Balancers](https://www.tryexponent.com/courses/system-design-interview/fundamentals-system-design/load-balancers)
- [Caching Strategies](https://www.tryexponent.com/courses/system-design-interview/fundamentals-system-design/system-design-caching)
- [Asynchronous Processing](https://www.tryexponent.com/courses/system-design-interview/fundamentals-system-design/asynchronous-processing)
- [Database Sharding](https://www.tryexponent.com/courses/system-design-interview/fundamentals-system-design/database-sharding)

# Note


# Reference

