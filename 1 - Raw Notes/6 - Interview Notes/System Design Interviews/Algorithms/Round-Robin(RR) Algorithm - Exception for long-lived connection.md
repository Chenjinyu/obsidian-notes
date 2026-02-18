Date: 2026-02-16
Course:
Tags: [[Round Robin]] [[Round-Robin(RR) Algorithm]][[System Design]] [[Algorithms]] [[System Design Interview]]

# Content

**Round Robin does NOT replace existing connections and it does NOT cause an error.**  
It simply keeps assigning **new connections** in order, **ignoring how long old ones stay open**.

Long-lived connections just… stay open.

---
### What actually happens step by step
Assume 3 servers: A, B, C  
Round Robin sequence: A → B → C → A → B → C …
Now imagine:
- Connections to **A** are long-lived (WebSockets, streaming)
- Connections to **B** and **C** are short-lived
#### Timeline
1. Client 1 → A (long connection, stays open)
2. Client 2 → B (short, closes quickly)
3. Client 3 → C (short, closes quickly)
4. Client 4 → A (**another** long connection)
5. Client 5 → B
6. Client 6 → C

Result after a while:
- Server **A** has many active connections
- Servers **B** and **C** are mostly idle

Round Robin **does not care**. It never checks connection count or load.

---
### Key points to be very clear about
- ❌ **No connection replacement**
- ❌ **No forced closing**
- ❌ **No error by default**
- ✅ Existing connections stay until the client or server closes them
- ✅ Only **new connections** are scheduled

If a server becomes overloaded:
- The load balancer **keeps sending traffic anyway**
- Eventually the server itself may:
    - Respond slowly
    - Time out
    - Reject connections
    - Crash (worst case)

That failure is **not caused by Round Robin directly**, but by its lack of awareness.

---
### Why this is a problem
Round Robin assumes:
> All connections cost roughly the same
When that assumption is false (long-lived connections):
- Load becomes uneven
- One server can get overwhelmed
- Latency increases

This is why Round Robin is **bad for**:
- WebSockets
- Streaming
- gRPC streams
- File uploads
- Chat systems

---

### What systems do instead
For long-lived or uneven connections, use:
- **Least Connections**
- **Weighted Least Connections**
- **Least Response Time**
- **Connection-aware load balancing**

These **avoid sending new traffic to already busy servers**.

---
### Mental model (remember this)
> **Round Robin is blind.**  
> It hands out tickets in order and never looks back.

# Note


# Reference

