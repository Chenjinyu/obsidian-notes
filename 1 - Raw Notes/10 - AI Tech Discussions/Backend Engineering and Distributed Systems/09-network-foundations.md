---
sr-due: <% tp.date.now("YYYY-MM-DD", 3) %>
sr-interval: 1
sr-ease: 2.5
---

# Network Foundations — What Happens When One Service Calls Another?

## Definition and mental model

Networking moves data between processes on different machines. An API call is the application-level operation; DNS, transport connections, encryption, and HTTP make that call possible. A useful mental picture is **find the destination → establish communication → protect it → exchange an application message**. Existing cached answers and connections can skip some setup work.

For your Python service calling a job API, understand these layers before choosing REST, gRPC, or streaming.

| Concept | Meaning | What it does not guarantee |
|---|---|---|
| DNS | Resolves names to records, often IP addresses | Not a guarantee that the destination is healthy or unchanged |
| IP address | Network address used to route packets | Does not identify an individual application by itself |
| Port | Identifies a transport endpoint/service on a host | Does not prove which application or user is behind it |
| Socket | An operating-system interface for network communication | Not necessarily a WebSocket |
| TCP | Reliable, ordered byte stream with congestion/flow control | No message boundaries or business-level exactly-once effect |
| UDP | Datagram transport | No built-in ordered reliable delivery |
| TLS | Authenticated encrypted transport when correctly configured | Does not authorize a caller to access a particular job |
| HTTP | Application protocol with methods, headers, statuses, and bodies | Does not require REST architecture |

TCP commonly establishes a connection with SYN, SYN-ACK, ACK. TLS negotiation is another layer; it is not the same handshake. A TCP acknowledgment confirms transport receipt, not that a database transaction committed. An HTTP success response can carry a stronger application contract, depending on the API.

## Real-world use cases

| Real-world scenario | Network foundations involved | Why understanding the layers matters |
|---|---|---|
| Opening an online store over HTTPS | DNS finds an endpoint; the client establishes a supported transport, negotiates TLS, and exchanges HTTP messages. | A DNS failure, certificate failure, and application error require different diagnoses even if the page simply appears unavailable. |
| Service calling a database repeatedly | A connection pool reuses established transport connections for database requests. | Reuse avoids repeated setup, but stale connections, pool limits, and timeouts still affect reliability. |
| Service discovery during scaling | New application instances appear while old instances are removed. | Clients or proxies must learn current endpoints and stop routing work to unhealthy or retired ones. |
| Real-time voice call | Media commonly uses UDP-based protocols with application-level handling of loss and timing. | An old audio packet may be less useful than the next one; media systems need jitter handling, congestion control, and security above raw UDP. |
| Fast multiplayer movement updates | A game may send position updates using a datagram-based transport while protecting purchases or inventory changes through reliable application operations. | Different message types have different latency, ordering, and correctness requirements. |
| Dashboard with many concurrent API reads | HTTP/2 can multiplex multiple streams on one connection. | Multiplexing changes connection usage, but TCP packet loss can still delay delivery across streams on that connection. |
| Mobile browsing on a lossy network | HTTP/3 uses QUIC streams over UDP, with integrated TLS security. | Loss recovery can avoid TCP-style cross-stream transport blocking; actual performance still depends on the network and implementation. |
| IoT device behind a home router | A device initiates an outbound connection to a backend or broker. | NAT and firewall behavior explain why a cloud service usually cannot simply open a new inbound connection to that device. |

**Walk through a failed checkout call:** if name resolution fails, no HTTP request reaches the payment service. If TLS certificate verification fails, the client should not bypass verification to proceed. If the client sends the request and then times out, the payment may already have been accepted. These failures look similar to a user but require different recovery behavior.

**Interview practice:** trace an HTTPS request from name lookup to application response, then identify which layer could explain a timeout, connection reset, or certificate error. A transport acknowledgment is not proof that a business transaction committed.

## Trace an HTTPS call

1. Parse the URL and decide whether a proxy is involved.
2. Resolve the hostname, possibly using cached DNS records.
3. Reuse a suitable pooled connection, or establish a new transport connection.
4. For a new HTTPS connection, negotiate TLS and validate the server certificate/hostname. With mutual TLS, the client can also present a certificate.
5. Send the HTTP request. An edge proxy or load balancer may terminate TLS and open a separate upstream connection.
6. The application authenticates and authorizes the request, performs work, and responds.
7. Read the complete response or close it appropriately so connection-pool resources are released.

Failure can occur at each step. “The API is slow” could mean slow DNS, waiting for an available pooled connection, connection establishment, TLS, backend work, or downloading a large response. Separate these measurements rather than treating latency as one unexplained number.

## HTTP versions and connection reuse

| Version | Transport picture | Interview point |
|---|---|---|
| HTTP/1.1 | Commonly TCP, optionally protected by TLS | Persistent connections can carry successive requests; concurrency often uses multiple connections |
| HTTP/2 | Multiple HTTP streams over one TCP connection | Multiplexing reduces application-level blocking, but packet loss can stall TCP delivery affecting streams |
| HTTP/3 | HTTP over QUIC, built on UDP | QUIC supplies secure reliable streams; “uses UDP” does not mean HTTP messages become unreliable |

HTTP keep-alive/connection reuse is different from an SSE response remaining open. Pooling reuses transport for requests; SSE keeps sending events within one response. A WebSocket is an application messaging protocol, not a synonym for a socket.

## Runnable Python: TCP has bytes, not message boundaries

Save as `tcp_frames.py`; Python 3.11+ and no packages are required. This local program starts a server on an available port, sends one length-prefixed message in deliberately separated writes, and reads its echoed reply.

```python
import asyncio

MAX_MESSAGE = 4096

async def read_frame(reader):
    size = int.from_bytes(await reader.readexactly(4), "big")
    if size > MAX_MESSAGE:
        raise ValueError("Frame too large")
    return await reader.readexactly(size)

async def handle(reader, writer):
    try:
        async with asyncio.timeout(2):
            body = await read_frame(reader)
            writer.write(len(body).to_bytes(4, "big") + body)
            await writer.drain()
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle, "127.0.0.1", 0)
    async with server:
        port = server.sockets[0].getsockname()[1]
        reader, writer = await asyncio.open_connection("127.0.0.1", port)
        try:
            body = "job-123:completed".encode("utf-8")
            packet = len(body).to_bytes(4, "big") + body
            writer.write(packet[:6])
            await writer.drain()
            await asyncio.sleep(0.02)
            writer.write(packet[6:])
            await writer.drain()
            async with asyncio.timeout(2):
                print((await read_frame(reader)).decode("utf-8"))
        finally:
            writer.close()
            await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
```

Expected: `job-123:completed`. A write can be split across reads; several writes can arrive together. The receiver uses an explicit length to find the boundary. HTTP, WebSocket, and gRPC supply their own framing; ordinary API code should not reinvent it. Production raw-socket servers also catch malformed frames, limit connection counts, and handle early EOF gracefully.

### TLS configuration and HTTP pooling

```python
import ssl
import httpx

context = ssl.create_default_context()
assert context.check_hostname
assert context.verify_mode == ssl.CERT_REQUIRED

# Use a context manager once around many requests in an application lifespan.
with httpx.Client(
    verify=context,
    timeout=httpx.Timeout(5, connect=2, pool=1),
    limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
) as client:
    pass  # client.get(...) uses this pool and verification policy.
```

Do not fix certificate errors by disabling verification. Configure the correct CA trust and hostname. Numbers here are illustrative; choose them from concurrency and latency requirements. A per-phase timeout is not automatically a total deadline.

## Supporting techniques, failure cases, and use cases

Use connection pooling for repeated outbound API calls. Bound pool size and waiting: unlimited concurrency can exhaust sockets and overload dependencies. Use retries only for safe transient failures. TLS failures due to bad configuration do not improve with endless retries.

DNS TTL, connection lifetime, and service discovery interact: resolving a changed address does not relocate an already-open connection. Deployment draining and reconnect behavior matter. NATs, firewalls, and proxies may close idle connections, motivating timeouts, heartbeats, and recovery in the streaming guides.

For monitoring, track DNS/connect/TLS latency when available, active sockets, pool waits, timeout categories, retransmission/error signals, response sizes, and request duration. Connection success and application health are different checks.

## Quick recall and interview practice

**Remember:** DNS finds; TCP delivers ordered bytes; TLS protects; HTTP describes requests/responses. None alone guarantees a business operation happened once.

**Interview answer:** “I would trace the call through DNS, connection pooling, transport setup, TLS, and application processing. I would separate phase timeouts from the end-to-end deadline and measure where latency occurs.”

1. Does TCP preserve the boundary between two calls to send?
2. Is a TCP ACK evidence that an order was saved?
3. How does HTTP/2 multiplexing differ from opening many HTTP/1.1 connections?
4. Why does HTTP/3 over UDP still provide reliable HTTP streams?
5. How are keep-alive, heartbeat, and SSE different?

References: [Python sockets](https://docs.python.org/3/library/socket.html), [Python TLS](https://docs.python.org/3/library/ssl.html), [HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110.html), [HTTP/3](https://www.rfc-editor.org/rfc/rfc9114.html). Related: [REST](01-rest-apis.md), [SSE](03-server-sent-events.md), [Retries](06-retries-backoff-jitter.md).
