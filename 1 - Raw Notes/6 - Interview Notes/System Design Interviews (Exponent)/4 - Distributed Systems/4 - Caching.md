Date: 2026-02-16
Course: https://www.tryexponent.com/courses/system-design-interviews/system-design-caching
Tags: [[System Design Interview]] [[Distributed System]] [[Caching]]

# Content

Caching is a data storage technique that is ubiquitous throughout computer systems and plays an important role in designing scalable Internet applications. A _cache_ is any data store that can store and retrieve data quickly for future use, enabling faster response times and decreasing load on other parts of your system.

## **Why we need caching**[](https://www.tryexponent.com/courses/system-design-interviews/system-design-caching#why-we-need-caching)

Without caching, computers and the Internet would be impossibly slow due to the **access time** of retrieving data at every step. Caches take advantage of a principle called **locality** to store data closer to where it is likely to be needed. This principle is at work even within your computer: as you browse the web, your web browser caches images and data temporarily on your hard drive; data from your hard drive is cached in memory, etc.

In large-scale Internet applications, caching can similarly make data retrieval more efficient by reducing repeated calculations, database queries, or requests to other services. This frees up resources to be used for other operations and serve more traffic volume. In a looser sense, caching can also refer to the storage of pre-computed data that would otherwise be difficult to serve on demand, like personalized newsfeeds or analytics reports.

## How caching works[](https://www.tryexponent.com/courses/system-design-interviews/system-design-caching#how-caching-works)

Caching can be implemented in many different ways in modern systems:

**In-memory application cache.** Storing data directly in the application's memory is a fast and simple option, but each server must maintain its own cache, which increases overall memory demands and cost of the system.

**Distributed in-memory cache.** A separate caching server such as Memcached or Redis can be used to store data so that multiple servers can read and write from the same cache.
![](assets/4%20-%20Caching/file-20260216230911570.png)
**Database cache.** A traditional database can still be used to cache commonly requested data or store the results of pre-computed operations for retrieval later.
**File system cache.** A file system can also be used to store commonly accessed files; CDNs are one example of a distributed file system that take advantage of geographic locality.
![](assets/4%20-%20Caching/file-20260216230928908.png)
## Caching policies[](https://www.tryexponent.com/courses/system-design-interviews/system-design-caching#caching-policies)

One question you may be wondering is, "If caching is so great, why not cache everything?"

There are two main reasons: cost and accuracy. Since caching is meant to be fast and temporary, it is often implemented with more expensive and less resilient hardware than other types of storage. For this reason, caches are typically smaller than the primary data storage system and must selectively choose which data to keep and which to remove (or _evict_). This selection process, known as a **caching policy**, helps the cache free up space for the most relevant data that will be needed in the future.

Here are some common examples of caching policies:

- **First-in first-out (FIFO).** Similar to a queue, this policy evicts whichever item was added longest ago and keeps the most recently added items.
- **Least recently used (LRU).** This policy keeps track of when items were last retrieved and evicts whichever item has not been accessed recently. [See the related programming question](https://tryexponent.com/courses/software-engineering/lru-cache).
- **Least frequently used (LFU).** This policy keeps track of how often items are retrieved and evicts whichever item is used least frequently, regardless of when it was last accessed.

In addition, caches can quickly become out-of-date from the true state of the system. This speed/accuracy tradeoff can be reduced by implementing an **eviction policy** - most commonly by **limiting the time-to-live (TTL)** of each cache entry, and updating the cache entry before or after database writes (write-through vs. write-behind).

## Cache coherence[](https://www.tryexponent.com/courses/system-design-interviews/system-design-caching#cache-coherence)

One final consideration is how to ensure appropriate cache consistency given our requirements.

- A **write-through cache** updates the cache and main memory simultaneously, meaning there's no chance either can go out of data. It also simplifies the system.
- In a **write-behind cache,** memory updates occur asynchronously. This may lead to inconsistency, but it speeds things up significantly.

Another option is called **cache-aside** or **lazy loading** where data is loaded into the cache on-demand. First, the application checks the cache for requested data. If it's not there (also called a "**cache miss**") the application fetches the data from the data store and updates the cache. This simple strategy keeps the data stored in the cache relatively "relevant" - as long as you choose a cache eviction policy and limited TTL combination that matches data access patterns.
![](assets/4%20-%20Caching/file-20260216230944969.png)
## Concept check[](https://www.tryexponent.com/courses/system-design-interviews/system-design-caching#concept-check)

There are 3 big decisions you'll have to make when designing a cache.

- How big should the cache be?
	- At a high level, consider how latency reduction will impact your users vs. the added cost of increased complexity and expensive hardware. Then consider anticipated request volume and the size and distribution of cached objects. From there, design your cache such that it meets your cache hit rate targets.
- How should I evict cached data?
	- This will depend on your application, but LRU is by far the most common option. It's simple to implement and works best under most circumstances.
- Which expiration policy should I choose?
	- A common, simple approach is to set an absolute TTL based on data usage patterns. Consider the impact of stale data on your users and how quickly data changes. You likely won't get this right the first time.

# Note


# Reference

