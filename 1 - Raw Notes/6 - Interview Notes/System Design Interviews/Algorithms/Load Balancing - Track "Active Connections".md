Date: 2026-02-16
Course:
Tags: [[Load Balancing]] [[System Design]] [[Algorithms]]

# Content

Load balancers track **“active connections”** by **owning the connection state**. Once you see that, everything clicks.
Below is the clean mental model, then the technical details.

---
## One-sentence summary
> Load balancers track active connections by sitting in the traffic path, maintaining a connection table, and incrementing or decrementing counts as connections open and close.

---
## Core idea (mental model)
> **If traffic passes _through_ the load balancer, it can count connections.  
> If traffic is only _redirected_, it can’t.**

Tracking active connections requires the load balancer to:
- See when a connection **starts**
- See when a connection **ends**

That means the load balancer must sit **in the data path**, not just give out addresses.

---
## How it works in practice
### 1. Connection termination (most common)
The load balancer **terminates the client connection** and opens a **new connection to the backend**.
```
Client ──TCP──> Load Balancer ──TCP──> Server
```
What the LB tracks:
- Client → LB connection count
- LB → Server connection count (this is what “Least Connections” uses)
When:
- A client connects → counter +1
- A connection closes (FIN/RST/timeout) → counter −1

This is **Layer 4 (TCP)** or **Layer 7 (HTTP)** load balancing.

---
### 2. Proxy-based tracking (Layer 7)
At Layer 7 (HTTP/gRPC):
- The load balancer acts as a **reverse proxy**
- Each request or stream is explicitly managed
The LB tracks:
- Open HTTP/1.1 keep-alive connections
- Active HTTP/2 or gRPC streams
- WebSocket sessions
This allows:
- Least Connections
- Least Active Requests
- Least Response Time
Very accurate, slightly more overhead.
---
### 3. NAT / connection table (Layer 4)
For TCP/UDP load balancing:
- The LB maintains a **connection table**
- Similar to a firewall or NAT device
Each entry tracks:
- Source IP:port
- Destination IP:port
- Backend server chosen
- TCP state (SYN, ESTABLISHED, FIN, TIME_WAIT)

As long as the entry exists → the connection is “active”.

---
## What counts as an “active connection”?
Usually:
- TCP state = **ESTABLISHED**
- Or a stream/request not fully closed
Closed when:
- FIN/ACK handshake completes
- RST received
- Idle timeout expires
Important detail:
> Idle but open connections **still count**.
This is why long-lived idle connections can distort load.

---
## What load balancers **cannot** track
### ❌ DNS-based load balancing
DNS only returns an IP.
- No visibility into connections
- No idea when connections end
- Cannot do Least Connections
### ❌ Direct Server Return (DSR)
If responses bypass the LB:
- It may not see connection teardown
- Tracking becomes approximate or impossible

---
## Sticky sessions interaction
If **session affinity** is enabled:
- New connections from the same client are forced to the same server
- Least Connections is partially overridden
Trade-off:
- Better session consistency
- Worse load distribution

---
## Why this matters (engineering reality)
Least Connections is only as good as:
- The accuracy of connection tracking
- Timeout tuning
- Whether the LB is in the full traffic path
Bad timeouts = wrong load decisions.

---


# Note


# Reference

