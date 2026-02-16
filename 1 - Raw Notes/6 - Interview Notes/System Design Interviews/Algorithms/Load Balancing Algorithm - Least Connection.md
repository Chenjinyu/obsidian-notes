Date: 2026-02-16
Course:
Tags: 

# Content
**Least Connections** is a **load-balancing algorithm**. Its job is to decide **which server should handle the next incoming request**.
### What it does (plain English)

Instead of sending traffic evenly in a round-robin order, **Least Connections sends each new request to the server that currently has the fewest active connections**.
The assumption is simple and usually true:
> Fewer active connections = more available capacity right now.

### Why it’s useful
Not all requests take the same amount of time.
- Some finish in milliseconds
- Others stay open for seconds or minutes

If you just rotate traffic evenly, one server might get stuck handling long-running requests while another is mostly idle. Least Connections adapts **in real time**.
### Where it’s normally used
You’ll see Least Connections used in:
1. **Load balancers**
    - Hardware load balancers
    - Software load balancers (reverse proxies)
2. **Web applications**
    - APIs with variable request durations
    - Streaming or file uploads
3. **Microservices**
    - When different requests have very different processing costs
4. **TCP-based services**
    - Databases, chat servers, WebSockets, gRPC

### When it’s a good choice
Use Least Connections when:
- Request duration varies a lot
- Connections stay open for a long time
- Servers are roughly equal in power

### When it’s _not_ ideal
It’s less effective when:
- Servers have very different hardware capacities (unless **weighted**)
- Requests are extremely short and uniform
- Connection count doesn’t reflect actual load (e.g., CPU-heavy tasks)

### Common variant
**Weighted Least Connections**
- Each server has a weight (capacity)
- A stronger server is allowed more connections before being considered “busy”
### One-sentence summary
> Least Connections is a load-balancing strategy that routes new requests to the server with the fewest active connections, and it’s best for systems with uneven or long-running requests.


# Note


# Reference

