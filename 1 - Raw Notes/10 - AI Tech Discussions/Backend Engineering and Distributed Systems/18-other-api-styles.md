---
sr-due: 2026-10-21
sr-interval: 1
sr-ease: 2.5
---

# Other API Styles — GraphQL, SOAP, and Choosing an Interface

## Start by separating categories

REST, RPC, GraphQL, SOAP, messaging, SSE, and WebSocket are not all alternatives at the same layer. REST is an architectural style; RPC organizes calls around operations; GraphQL defines a query language and execution model; SOAP defines an XML-based messaging framework. HTTP can transport several of them. SSE and WebSocket handle continuing message delivery; queues and logs decouple asynchronous work.

A company can expose GraphQL to a web application, call internal gRPC services, publish Kafka events, and use SSE for notifications. Choose each boundary based on its consumers and requirements.

## Real-world use cases

GraphQL and SOAP solve different integration needs. These are illustrative product requirements, not claims that every company in an industry uses a particular API style.

| API style | Real-world scenario | What happens and why it fits |
|---|---|---|
| GraphQL | Mobile home screen | A client requests a profile summary, recent orders, and notification count through one schema, selecting the fields that screen needs. |
| GraphQL | E-commerce product page | A client selects product variants, prices, reviews, and seller details while another client requests a smaller view from the same schema. |
| GraphQL | Internal support portal | An agent views related customer, subscription, and ticket information through an API that composes backend data. Resolver authorization and query cost remain essential. |
| GraphQL | Several evolving frontends | Web and mobile clients request different views as their screens evolve, reducing the need for a separate endpoint shape for every screen. |
| SOAP | Insurance partner integration | A partner exposes policy or claim operations through a WSDL contract; the application exchanges the required SOAP XML messages. |
| SOAP | Airline or travel-system integration | An existing provider requires contract-defined reservation operations and SOAP fault handling. Using its supported interface is the integration requirement. |
| SOAP | Existing financial enterprise service | A system exposes customer or account operations through a SOAP service contract. The client follows the required schema and any specified security standards. |
| SOAP | Carrier or logistics integration | A carrier's existing SOAP API provides shipment creation or tracking operations. Generated clients can help with the published contract. |

**Walk through a GraphQL product page:** the client asks for a product's title, selected variants, and a limited set of reviews. Resolvers obtain the underlying data, possibly from several services. A single client request can still trigger many backend reads, so selection flexibility does not automatically mean lower server cost. Batch repeated lookups, paginate collections, enforce authorization, and bound query complexity.

**Walk through a SOAP carrier integration:** obtain the carrier's service contract, build the required shipment request, and handle its defined response or fault. If a timeout occurs after sending the request, use the provider's operation identifier or status lookup to avoid creating a duplicate shipment. SOAP's envelope and schema do not remove the unknown-outcome problem.

**Interview practice:** explain why frontend data-selection flexibility may favor GraphQL, while compatibility with an existing partner contract may require SOAP. Neither choice replaces queues, event delivery, or workflow recovery elsewhere in the product.

## GraphQL: clients select fields from a schema

**GraphQL** lets clients request particular fields from a typed schema. The server validates the query and executes resolver functions that retrieve those fields. A query reads data; a mutation represents a write operation; a subscription provides ongoing results through a transport chosen by the implementation.

It is useful when web/mobile clients need different shapes of related data, or a client-facing layer aggregates multiple services. It can reduce unwanted fields and repeated client round trips. It does not automatically reduce backend queries or guarantee a faster system.

### Runnable Python GraphQL example

Install `graphql-core`, save as `graphql_demo.py`, and run it. This executes the query locally to isolate the schema/resolver concepts; it does not expose an HTTP server.

```python
from graphql import build_schema, graphql_sync

schema = build_schema("""
    type Job { id: ID!, status: String!, progress: Int! }
    type Query { job(id: ID!): Job }
""")
jobs = {"job-123": {"id": "job-123", "status": "running", "progress": 42}}

def resolve_job(source, info, id):
    # A network service must authorize info.context's caller before lookup.
    return jobs.get(id)

schema.get_type("Query").fields["job"].resolve = resolve_job
query = "query FindJob($id: ID!) { job(id: $id) { status progress } }"
result = graphql_sync(schema, query, variable_values={"id": "job-123"})
assert result.errors is None
print(result.data)  # id is not requested and is absent from the result.

invalid = graphql_sync(schema, '{ job(id: "job-123") { missingField } }')
assert invalid.errors
print("Unknown field rejected by validation")
```

To expose it over HTTP, add an authenticated HTTP adapter accepting the query and variables, configure body/query limits, call the executor, and serialize data plus errors according to the chosen GraphQL-over-HTTP contract. Do not turn this learning resolver into an unauthenticated public data endpoint.

### Supporting techniques and pitfalls

- **N+1 queries:** resolving a list of jobs and then each owner separately can create one query for the list plus N owner queries. Batch and cache lookups within a request using a DataLoader-like mechanism; avoid cross-user cache leakage.
- **Query cost/depth limits:** flexible nested queries can be expensive even if their HTTP body is small. Bound depth, complexity, pagination, execution time, and concurrency.
- **Authorization:** check resource/field access in appropriate resolvers or a shared policy layer. Hiding a field in the UI does not secure it.
- **Caching:** response shape and variables affect keys. Persisted queries and well-defined cache identities can help, but HTTP caching requires deliberate design.
- **Partial results:** data and errors can coexist. A non-null field error can propagate to its parent; inspect the GraphQL result, not just HTTP status.
- **Mutations:** serial execution of top-level mutation fields in one operation is not a database transaction or global lock. Use authoritative transactional logic and idempotency as needed.
- **Subscriptions:** often use WebSocket or SSE-based transports, but GraphQL itself does not make updates durable or replayable.

## SOAP: XML messages with formal contracts

**SOAP is an XML-based messaging framework.** A SOAP message has an Envelope, optional Header, and Body; failures can be represented as Faults. It is often associated with WSDL service descriptions and XML Schema types in enterprise integrations. HTTP is common, but SOAP is not conceptually restricted to one transport.

SOAP is worth understanding when integrating with an established partner, bank, or enterprise service whose contract uses it. It can support an ecosystem of standards such as WS-Security, but merely writing an XML envelope does not implement signing, encryption, or reliable messaging.

### Python: construct and inspect a SOAP 1.2 envelope

Save as `soap_demo.py`; standard library only. This demonstrates message structure, not a complete SOAP client or WSDL implementation. Only locally generated XML is parsed in this example.

```python
import xml.etree.ElementTree as ET

SOAP = "http://www.w3.org/2003/05/soap-envelope"
JOBS = "urn:learning:jobs"
ET.register_namespace("soap", SOAP)
ET.register_namespace("j", JOBS)

envelope = ET.Element(f"{{{SOAP}}}Envelope")
body = ET.SubElement(envelope, f"{{{SOAP}}}Body")
operation = ET.SubElement(body, f"{{{JOBS}}}GetJob")
ET.SubElement(operation, f"{{{JOBS}}}jobId").text = "job-123"
wire = ET.tostring(envelope, encoding="utf-8", xml_declaration=True)
print(wire.decode())

parsed = ET.fromstring(wire)
job_id = parsed.find(f"{{{SOAP}}}Body/{{{JOBS}}}GetJob/{{{JOBS}}}jobId")
assert job_id is not None and job_id.text == "job-123"
```

For a real provider, use the exact WSDL, namespaces, SOAP version, endpoint, bindings, and security requirements. SOAP 1.2 commonly uses `application/soap+xml`; SOAP 1.1 uses different conventions including the SOAPAction header in its HTTP binding. Do not mix versions by copying an envelope from an unrelated example.

Handle SOAP Faults as well as HTTP/network errors. Untrusted XML needs hardened parser settings, limits, and protection against entity/resource-exhaustion attacks. A schema-valid XML document can still request an unauthorized action.

## A comparison for choosing, not ranking

| Interface | Good starting fit | Main responsibility you still own |
|---|---|---|
| REST-style HTTP | Broad client compatibility and resource-oriented APIs | Resource design, authorization, pagination, concurrency |
| JSON RPC-style API | Named operations with simple serialization | Explicit errors, contracts, deadlines, idempotency |
| gRPC | Typed internal calls and supported streaming | Compatible schema rollout, deadlines, transport support |
| GraphQL | Different clients need flexible related data | Resolver authorization, batching, query cost |
| SOAP | Existing contract-driven enterprise integration | Exact bindings, XML/security rules, faults |
| Asynchronous messaging | Decoupled long-running or event-driven work | Delivery/effect guarantees, ordering, recovery |

Avoid “GraphQL replaces every REST API” or “SOAP is always obsolete.” Existing client contracts, operational experience, latency, tooling, and organizational requirements matter. A new system does not need every style just because the team knows them.

## Quick recall and interview practice

**Remember:** query shape, operation contract, transport, and delivery guarantees are separate choices.

**Interview answer:** “I would select the interface from the consumers' needs. GraphQL can give clients flexible views but needs query-cost and resolver controls. SOAP is appropriate when the integration contract requires its messaging and security conventions. Neither removes ordinary distributed-system failure handling.”

1. Why can GraphQL reduce client round trips while increasing backend queries?
2. What is a resolver, and where should authorization happen?
3. Do GraphQL mutations make several database writes transactional?
4. What is the difference between a SOAP Fault and an HTTP transport failure?
5. Why does a SOAP envelope alone not implement WS-Security?

References: [GraphQL learning guide](https://graphql.org/learn/), [GraphQL-core execution](https://graphql-core-3.readthedocs.io/en/latest/usage/queries.html), [SOAP 1.2](https://www.w3.org/TR/soap12-part1/). Related: [REST](01-rest-apis.md), [RPC](10-rpc.md), [gRPC](11-grpc.md).
