Date: 2026-01-29
Course: https://www.tryexponent.com/courses/system-design-interviews/reliability-strategies
Tags: [[System Design Interview]] [[Load Balancing]]

# Content

A _load balancer_ is a type of server that distributes incoming web traffic across multiple backend servers. Load balancers are an important component of scalable Internet applications: they allow your application(s) to scale up or down with demand, achieve higher availability, and efficiently utilize server capacity.

![load balancer](https://exponent-content.s3.amazonaws.com/load_balancer_891b3528f0.png)

## Why we need load balancers[](https://www.tryexponent.com/courses/system-design-interviews/load-balancers#why-we-need-load-balancers)

In order to understand why and how load balancers are used, it's important to remember a few concepts about distributed computing.

First, web applications are deployed and hosted on **servers**, which ultimately live on hardware machines with finite resources such as memory (RAM), processor (CPU), and network connections. As the traffic to an application increases, these resources can become limiting factors and prevent the machine from serving requests; this limit is known as the system's **capacity**. At first, some of these scaling problems can be solved by simply increasing the memory or CPU of the server or by using the available resources more efficiently, such as multithreading.

At a certain point, though, increased traffic will cause any application to exceed the capacity that a single server can provide. The only solution to this problem is to add more servers to the system, also known as **horizontal scaling.** When more than one server can be used to serve a request, it becomes necessary to decide _which_ server to send the request to. That's where load balancers come into the picture.

## **How load balancers work**[](https://www.tryexponent.com/courses/system-design-interviews/load-balancers#how-load-balancers-work)

A good load balancer will efficiently distribute incoming traffic to maximize the system's capacity utilization and minimize the queueing time. Load balancers can distribute traffic using several different strategies:

- Round robin [[../Algorithms/Round-Robin(RR) Algorithm|Round-Robin(RR) Algorithm]]: Servers are assigned in a repeating sequence, so that the next server assigned is guaranteed to be the least recently used.
- Least connections [[../Algorithms/Load Balancing Algorithm - Least Connection|Load Balancing Algorithm - Least Connection]]: Assigns the server currently handling the fewest number of requests.
- Consistent hashing [[../Distributed Systems/1 - Consistent Hashing|Consistent Hashing]]: Similar to database sharding, the server can be assigned consistently based on IP address or URL.

Since load balancers must handle the traffic for the entire server pool, they need to be efficient and highly available. Depending on the chosen strategy and performance requirements, load balancers can operate at higher or lower network layers (HTTP vs. TCP/IP) or even be implemented in hardware. Engineering teams typically don't implement their own load balancers and instead use an industry-standard **reverse proxy** (like HAProxy or Nginx) to perform load balancing and other functions such as SSL termination and health checks. Most cloud providers also offer out-of-the-box load balancers, such as Amazon's Elastic Load Balancer (ELB).

## When to use a load balancer[](https://www.tryexponent.com/courses/system-design-interviews/load-balancers#when-to-use-a-load-balancer)

You should use a load balancer whenever you think the system you're designing would benefit from increased capacity or redundancy. Often load balancers sit right between external traffic and the application servers. In a microservice architecture, it's common to use load balancers in front of each internal service so that every part of the system can be scaled independently.

Be aware, load balancing _cannot_ solve many scaling problems in system design. For example, an application can also succumb to database performance, algorithmic complexity, and other types of resource contention. Adding more web servers won't compensate for inefficient calculations, slow database queries, or unreliable third-party APIs. In these cases, it may be necessary to design a system that can process tasks asynchronously, such as a job queue (see the Web Crawler question for an example).

Load balancing is notably distinct from **rate limiting**, which is when traffic is intentionally throttled or dropped in order to prevent abuse by a particular user or organization.

## Advantages **of load balancers**[](https://www.tryexponent.com/courses/system-design-interviews/load-balancers#advantages-of-load-balancers)

- **Scalability.** Load balancers make it easier to scale up and down with demand by adding or removing backend servers.
- **Reliability**. Load balancers provide redundancy and can minimize downtime by automatically detecting and replacing unhealthy servers.
- **Performance**. By distributing the workload evenly across servers, load balancers can improve the average response time.

## Considerations[](https://www.tryexponent.com/courses/system-design-interviews/load-balancers#considerations)

- **Bottlenecks**. As scale increases, load balancers can themselves become a bottleneck or single point of failure, so multiple load balancers must be used to guarantee availability. [DNS round robin](https://en.wikipedia.org/wiki/Round-robin_DNS) can be used to balance traffic across different load balancers.
- **User** **sessions.** The same user's requests can be served from different backends unless the load balancer is configured otherwise. This could be problematic for applications that rely on session data that isn't shared across servers.
- **Longer deploys.** Deploying new server versions can take longer and require more machines since the load balancer needs to roll over traffic to the new servers and drain requests from the old machines.

# Note


# Reference

