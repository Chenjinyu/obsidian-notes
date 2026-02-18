Date: 2026-02-16
Course:
Tags: [[Round Robin]] [[System Design Interview]][[Scalabe Systems]] [[Load Balancing]]

# Content

**Round Robin** is the simplest and most common **load-balancing algorithm**.
### What it does
It sends incoming requests to servers **one by one in a fixed order**, then loops back to the start.
Example with 3 servers:
```
Request 1 → Server A
Request 2 → Server B
Request 3 → Server C
Request 4 → Server A
Request 5 → Server B
… and so on
```
No intelligence, no feedback — just rotation.
### Why it’s used
Round Robin is popular because it is:
- **Simple** to implement
- **Predictable**
- **Low overhead** (no runtime metrics needed)
### Where it’s normally used
You’ll see Round Robin used in:
- **Basic HTTP load balancers**
- **DNS load balancing**
- **Stateless web services**
- **High-throughput systems** with very short requests
### When it’s a good choice
Round Robin works well when:
- All servers have **similar hardware**
- Requests take **roughly the same time**
- Connections are **short-lived**
- You want **maximum simplicity**
### When it’s a bad choice
It struggles when:
- Request duration varies a lot
- Some connections stay open much longer than others
- One server slows down or becomes overloaded
- Servers have unequal capacity
It keeps sending traffic even if a server is already busy.
### Common variant
**Weighted Round Robin**
- Each server gets a weight
- Higher weight = more requests in the cycle

Example:
```
A (weight 2), B (weight 1)
A → A → B → A → A → B
```
### Round Robin vs Least Connections (quick contrast)

| Aspect                 | Round Robin     | Least Connections |
| ---------------------- | --------------- | ----------------- |
| Decision based on      | Order           | Current load      |
| Adapts to slow servers | ❌ No            | ✅ Yes             |
| Overhead               | Very low        | Slightly higher   |
| Best for               | Uniform traffic | Variable traffic  |

### One-sentence summary
> Round Robin distributes requests evenly by rotating through servers, making it ideal for simple, fast, and uniform workloads.

If you want, next I can explain **Weighted Round Robin**, **IP Hash**, or help you choose the right strategy for a real system you’re designing.

# Note


# Reference

