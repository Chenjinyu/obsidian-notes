---
sr-due: <% tp.date.now("YYYY-MM-DD", 3) %>
sr-interval: 1
sr-ease: 2.5
---

# gRPC — Typed Remote Calls and Streaming

## Definition and relationship to RPC and Protobuf

**gRPC is an RPC framework for calling remote service methods using a defined contract and generated client/server code.** Its common stack uses HTTP/2 and Protocol Buffers. Your Python client calls a generated stub; the framework handles request framing, serialization integration, transport, and status handling.

RPC is the interaction model. gRPC is a particular framework. Protobuf defines/serializes messages. HTTP/2 is part of the common transport stack. These names describe different responsibilities.

It fits internal service-to-service communication, typed multilingual systems, and services that need streaming. For direct browser use, standard gRPC may require gRPC-Web and a compatible gateway; do not assume the browser exposes the same transport interface as a Python client.

## Four call shapes

| Shape | Client sends | Server sends | Example |
|---|---|---|---|
| Unary | One message | One message | Get job status |
| Server streaming | One message | Many messages | Watch job progress |
| Client streaming | Many messages | One response | Submit a batch of measurements for an aggregate |
| Bidirectional streaming | Many messages | Many messages | Interactive processing with both sides sending independently |

Ordering is preserved within an individual stream's direction. There is no global order across all RPCs. Streaming does not imply unlimited buffering, durable history, or automatic resumption after disconnection.

## Runnable Python implementation

First copy and compile `jobs.proto` from [the Protobuf guide](12-protocol-buffers.md). Install `grpcio` and `grpcio-tools`. Put the generated modules beside the following scripts.

Save as `grpc_server.py` and run `python grpc_server.py`. This is a localhost-only, unauthenticated demo using insecure transport and simulated progress.

```python
import asyncio
import grpc
import jobs_pb2 as pb
import jobs_pb2_grpc as api

class Jobs(api.JobsServicer):
    async def validate(self, request, context):
        if not request.job_id:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "job_id required")
        if request.job_id != "job-123":
            await context.abort(grpc.StatusCode.NOT_FOUND, "Unknown job")

    async def GetJob(self, request, context):
        await self.validate(request, context)
        return pb.JobStatus(job_id=request.job_id, state=pb.RUNNING, progress=40)

    async def WatchJob(self, request, context):
        await self.validate(request, context)
        for progress in (0, 50, 100):
            await asyncio.sleep(0.1)  # Cooperative async work, not blocking sleep.
            yield pb.JobStatus(
                job_id=request.job_id,
                state=pb.COMPLETED if progress == 100 else pb.RUNNING,
                progress=progress,
            )

async def main():
    server = grpc.aio.server()
    api.add_JobsServicer_to_server(Jobs(), server)
    server.add_insecure_port("127.0.0.1:50051")
    await server.start()
    try:
        await server.wait_for_termination()
    finally:
        await server.stop(grace=1)

if __name__ == "__main__":
    asyncio.run(main())
```

Save separately as `grpc_client.py`:

```python
import asyncio
import grpc
import jobs_pb2 as pb
import jobs_pb2_grpc as api

async def main():
    async with grpc.aio.insecure_channel("127.0.0.1:50051") as channel:
        jobs = api.JobsStub(channel)
        try:
            status = await jobs.GetJob(pb.JobRequest(job_id="job-123"), timeout=2)
            print("Unary progress:", status.progress)
            async for update in jobs.WatchJob(
                pb.JobRequest(job_id="job-123"), timeout=3
            ):
                print("Stream progress:", update.progress)
        except grpc.aio.AioRpcError as error:
            print("RPC failed:", error.code(), error.details())
            raise

if __name__ == "__main__":
    asyncio.run(main())
```

Expected: unary progress 40, then streaming progress 0, 50, 100. The streaming method simulates data per call; it is not a durable subscription. For a real job, reconnect using an application cursor or fetch authoritative current status.

## Deadlines, cancellation, and retries

`timeout=2` gives the call a time budget. Without an explicit deadline, callers can wait longer than intended. Propagate the remaining budget to downstream calls rather than giving every hop a fresh full timeout. Leave time for your own response handling.

A cancelled or expired RPC does not undo an already committed operation. Server work must cooperate with cancellation and clean up resources. For retriable mutations, use idempotency keys and a status lookup/reconciliation path.

Useful statuses include INVALID_ARGUMENT, NOT_FOUND, UNAUTHENTICATED, PERMISSION_DENIED, RESOURCE_EXHAUSTED, UNAVAILABLE, DEADLINE_EXCEEDED, and CANCELLED. These are gRPC statuses, not a one-for-one list of HTTP status codes. Map retry policy to the operation and failure, not just any non-success status.

gRPC supports configurable retry behavior and some transparent retries under defined conditions. Do not assume every failure is retried or safe; coordinate framework retries with application retries. Streaming recovery usually requires application-level state.

## Supporting techniques

| Need | Mechanism | Caveat |
|---|---|---|
| Secure identity | TLS/mTLS and application authorization | Encryption alone does not authorize a job lookup |
| Efficient repeated calls | Reuse channels/stubs | One long-lived connection may concentrate traffic depending on balancing |
| Find healthy services | Service discovery, gRPC-aware health and load balancing | A plain TCP check misses application failures |
| Understand latency | Interceptors, tracing metadata, per-method metrics | Do not log sensitive payloads indiscriminately |
| Control memory | Message-size limits and flow-control-aware processing | HTTP/2 flow control does not bound every application queue |
| Evolve contracts | Compatible proto changes and versioned deployment | Generated code can hide semantic incompatibility |

A load balancer must support the chosen gRPC/HTTP stack. L4 balancing selects connections, whereas L7 gRPC-aware balancing can route individual RPCs depending on implementation. Reuse is good, but understand how it interacts with distribution and failover.

## Quick recall and interview practice

**Remember:** define service and messages → generate code → implement servicer → call stub with a deadline. Reliability still requires deliberate design.

**Interview answer:** “I would use gRPC for typed internal calls and supported streaming patterns. I would reuse channels, propagate deadlines, authenticate and authorize calls, and design schema evolution and idempotency rather than assuming the framework supplies business reliability.”

1. How are gRPC, RPC, and Protobuf different?
2. Which streaming shape fits job progress?
3. What happens if the client deadline expires after the server saves a result?
4. Why can a single long-lived connection affect load distribution?
5. Does reconnecting automatically resume an interrupted stream?

References: [Python quick start](https://grpc.io/docs/languages/python/quickstart/), [deadlines](https://grpc.io/docs/guides/deadlines/), [retry behavior](https://grpc.io/docs/guides/retry/), [core concepts](https://grpc.io/docs/what-is-grpc/core-concepts/). Related: [Networking](09-network-foundations.md), [Retries](06-retries-backoff-jitter.md).
