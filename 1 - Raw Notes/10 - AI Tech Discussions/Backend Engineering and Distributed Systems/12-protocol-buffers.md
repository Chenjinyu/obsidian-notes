---
sr-due: <% tp.date.now("YYYY-MM-DD", 3) %>
sr-interval: 1
sr-ease: 2.5
---

# Protocol Buffers — Typed Messages and Compatible Schema Evolution

## Definition

**Protocol Buffers, or Protobuf, is a language-neutral schema and serialization system.** You describe structured messages in a `.proto` file, generate classes for your programming language, and serialize instances to a compact binary representation.

Think of a shared form definition: both services agree what field number 1 means, how field 2 is typed, and which values are allowed. Generated code provides convenient accessors; the wire format uses field numbers rather than sending full field names for each value.

Protobuf is not a transport, encryption scheme, database, or complete business validator. It can be used in files, queues, logs, or gRPC. gRPC commonly uses it for messages and service definitions, but the ideas are distinct.

## Real-world use cases

| Real-world scenario | What Protobuf represents | Why it fits |
|---|---|---|
| Typed internal gRPC API | Inventory requests, job results, and service method contracts. | Generated classes and stable schemas let services written in different languages exchange agreed message types. |
| IoT telemetry | Device IDs, measurement values, timestamps, and battery readings. | A binary schema can reduce repeated field-name overhead across many structured messages; measure actual payload size for the workload. |
| Order events in an event log | Events such as order accepted or shipment created. | Producers and consumers can share an explicit schema and evolve it compatibly, with a strategy for identifying message types and schema versions. |
| Offline mobile synchronization | A client stores structured changes locally and later uploads them. | The same serialization can be used in local files and transport payloads; conflict resolution remains an application concern. |
| Game service messages | Structured player actions, match state, or inventory updates. | Typed compact messages can be useful across clients and servers, independently of the chosen transport. |
| Long-term measurement archives | Stored records are read by later versions of analytics software. | Stable field numbers and compatibility rules support reading older data, provided the necessary schema definitions are retained. |
| Batch exchange between languages | A Python pipeline writes records consumed by a Java service. | Generated implementations share a wire format rather than maintaining unrelated custom parsers. |

**Walk through an evolving sensor message:** version one includes a device ID and temperature. A later version adds an optional battery field with a new field number. Older readers can ignore the unknown field; newer readers must handle its absence in old messages. If temperature is later removed, reserve its old field number instead of reusing it for an unrelated measurement.

Protobuf answers “how are these structured values represented as bytes?” A broker, HTTP API, gRPC call, or file system still moves or stores those bytes. It is not general-purpose compression, and smaller size than JSON is workload-dependent.

**Interview practice:** explain how an old consumer and a new producer can coexist, then describe a schema change that would break that compatibility.

## Why use it instead of JSON?

| Need | Protobuf helps by... | Trade-off |
|---|---|---|
| Many languages | Generating typed message classes | Requires code-generation and compatible runtimes |
| Compact messages | Encoding typed fields with numeric tags | Binary payloads are less convenient to inspect manually |
| Evolving services | Supporting carefully designed additive changes | Incompatible schema changes can still corrupt meaning |
| Shared contract | Checking types and structure | Application constraints still need validation |

Do not promise that Protobuf is always faster or smaller for every workload. Measure representative messages, CPU cost, compression, and network size. Avoid treating deterministic serialization as a universal canonical byte representation for signatures or hashes.

## The schema used by our gRPC guide

Save this as `jobs.proto`. The examples deliberately use proto3; newer Protobuf editions exist, but are not required for learning these fundamentals.

```proto
syntax = "proto3";
package learning;

enum State {
  STATE_UNSPECIFIED = 0;
  QUEUED = 1;
  RUNNING = 2;
  COMPLETED = 3;
}

message JobRequest {
  string job_id = 1;
}

message JobStatus {
  string job_id = 1;
  State state = 2;
  optional int32 progress = 3;
  reserved 4;
  reserved "old_detail";
  repeated string tags = 5;
}

service Jobs {
  rpc GetJob(JobRequest) returns (JobStatus);
  rpc WatchJob(JobRequest) returns (stream JobStatus);
}
```

The numbers are permanent field identities, not positions that should be renumbered when reorganizing a file. `repeated` is a list. The zero enum value provides an explicit unspecified default. `optional` lets this example distinguish absent progress from explicit zero.

## Generate Python code and run a round trip

Install `grpcio` and `grpcio-tools`, then run in the directory containing `jobs.proto`:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. jobs.proto
```

This produces `jobs_pb2.py` (messages) and `jobs_pb2_grpc.py` (gRPC stubs/servicer interfaces). The Protobuf-only round trip below uses only `jobs_pb2.py`; gRPC code is generated here for the next guide. Keep generated code and runtime versions compatible; do not hand-edit generated modules.

Save as `protobuf_demo.py`:

```python
from google.protobuf.json_format import MessageToDict
import jobs_pb2 as pb

original = pb.JobStatus(job_id="job-123", state=pb.RUNNING, tags=["batch"])
assert not original.HasField("progress")
original.progress = 0
assert original.HasField("progress")

encoded = original.SerializeToString()
decoded = pb.JobStatus.FromString(encoded)
assert decoded == original
print("Binary bytes:", encoded)
print("Readable view:", MessageToDict(decoded, preserving_proto_field_name=True))

# A field's type does not enforce all business rules.
decoded.progress = 150  # Valid int32, invalid percentage for our application.
assert not 0 <= decoded.progress <= 100
```

Expected: binary bytes, a readable dictionary, and assertions passing. Without explicit presence, a scalar default can be indistinguishable from omission through the usual generated API. Do not call HasField indiscriminately on implicit-presence scalar fields.

## Schema evolution: what interviews focus on

1. Add fields with new numbers; old readers can generally ignore unknown binary fields.
2. Never reuse a deleted field number. Reserve its number and usually its name to prevent accidental reuse, including text/JSON considerations.
3. Do not casually change a field's type, cardinality, or meaning. Some changes are wire-compatible yet unsafe for application semantics.
4. Unknown fields may survive binary parse/reserialize, but conversions through JSON or hand-built objects can lose information. Design migrations across the actual pipeline.
5. Add enum values carefully: older business logic may not know what to do with them.
6. Roll out compatible readers before writers depend on new behavior; retain backward compatibility for queued or stored historical data.

Binary compatibility and ProtoJSON compatibility are different. Renaming a field while retaining its number may preserve binary meaning but change JSON names and generated source APIs. A schema registry can track event schemas and compatibility rules; it is not inherently required by Protobuf or automatically provided by a broker.

## Supporting technologies and implementation details

Use code generation in CI, contract/compatibility checks, pinned compatible build tools, and explicit domain validation. Limit message size and nesting where appropriate. Log a safe readable representation rather than dumping sensitive raw bytes.

A raw stream of concatenated serialized messages needs framing: protobuf messages are not generally self-delimiting at the top level. gRPC supplies its own message framing; the network guide shows why boundaries matter.

For HMAC or signatures, authenticate the exact transmitted bytes or a well-specified canonical representation. Parsing and reserializing is not a general substitute. Encryption still requires TLS or an appropriate payload-encryption scheme.

## Quick recall and practice

**Remember:** schema → generated classes → message bytes. Field numbers are identities. Compatible parsing does not guarantee compatible business meaning.

**Interview answer:** “I would use Protobuf for a shared typed contract and efficient serialization. I would make additive changes, reserve deleted field numbers, validate domain constraints separately, and test compatibility across deployed versions.”

1. Does Protobuf send data over the network by itself?
2. Why is explicit zero different from missing progress?
3. Why should a removed field number never be reused?
4. Can a valid Protobuf message contain an invalid business value?
5. Does converting a binary message to JSON preserve all compatibility behavior?

References: [Proto3 guide](https://protobuf.dev/programming-guides/proto3/), [field presence](https://protobuf.dev/programming-guides/field_presence/), [serialization is not canonical](https://protobuf.dev/programming-guides/serialization-not-canonical/). Related: [gRPC](11-grpc.md), [HMAC](07-hmac-and-encoding.md).
