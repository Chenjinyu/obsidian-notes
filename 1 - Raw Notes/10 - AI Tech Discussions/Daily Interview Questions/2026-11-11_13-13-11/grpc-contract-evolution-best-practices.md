---
sr-due: 2026-11-11
sr-interval: 1
sr-ease: 2.5
created: "2026-11-11T13:38:27-06:00"
timezone: America/Chicago
source: voice-discussion
status: discussion-notes
tags:
  - grpc
  - protobuf
  - api-contract
  - schema-evolution
---

# gRPC Contracts: How Microservices Collaborate on Changes

## JC's question — summarized

If developers agree on a Protobuf contract before implementing internal microservices, why can data meaning still break? How should teams collaborate when one service needs to change a field and other services cannot upgrade immediately?

JC correctly identified the need for an agreed service contract. The refinement is that schema agreement, generated code, business meaning, and deployment compatibility are related responsibilities, and each deployed version must honor its supported contract.

## Agree on the complete contract

| Part | What teams agree on |
|---|---|
| Schema | RPC methods, request/response messages, field numbers, types, presence, and cardinality. |
| Business behavior | Units, valid values, meaning of omission and zero, update behavior, and relevant error cases. |
| Evolution | Which old/new versions coexist, deployment order, fallback or legacy behavior, and retirement criteria. |

The `.proto` file describes the structural interface. Comments and API documentation describe behavior; implementation and tests enforce it. A shared schema does not independently enforce every business rule. Google's compatibility guidance explicitly separates source, wire, and semantic compatibility. [1]

gRPC is commonly used between internal microservices and can also serve other clients. A remote call crosses a process/service boundary; the processes need not be on different physical machines. For a call from Service A to Service B, A is the client and B is the server for that call. [4]

## What happens when the contract changes?

Changing a shared `.proto` file does not change already-running clients. Each service continues using its generated message and RPC code until its build and deployment adopt the new contract.

I would keep the schemas in a shared repository or publish versioned schema/generated-code packages, assign an owner, and require review from affected consuming teams. Each service pins a supported contract release and compatible tooling. Different compatible contract versions may coexist; deployment does not require every service to adopt the latest release simultaneously.

This is a proposed team workflow, not functionality automatically supplied by gRPC.

## A practical rollout

1. **Review the change with consumers.** Identify who sends and receives the affected field, including retry queues, stored messages, and intermediaries. Agree on missing/default behavior and whether the change preserves existing meaning.
2. **Prefer additive evolution.** Introduce a fresh field number for a genuinely new field. Keep deployed field numbers stable and never reuse them. Reserve numbers and usually names after retiring deleted fields. Avoid changing types, cardinality, or meaning casually. [2]
3. **Publish and test the contract.** Generate the relevant Python and Java code and run compatibility checks. Verify application outcomes using old/new readers and writers, not just successful compilation or parsing.
4. **Expand receiver support first.** For a request change, deploy the receiving server so it supports old requests and the new contract before enabling callers to depend on it. For response changes that require new interpretation, upgrade the receiving clients before relying on that interpretation.
5. **Enable new senders gradually.** Use deployment controls and routing so new behavior reaches compatible receivers. Preserve legacy semantics for unchanged callers. Do not infer caller version from field presence.
6. **Retire deliberately.** Observe remaining legacy usage and allow for rollback and historical/retried messages before removing old support.

Steps 1, 3–6 are a rollout recommendation derived from the compatibility risks, rather than a universal order for every possible schema change. Simple additive fields may not require every reader to upgrade; new required behavior needs explicit support.

Protobuf's best-practice guide warns against assuming clients and servers update together, including when either side may roll back. [2]

## Apply this to the optional-progress interview

The intended new behavior is: omitted progress preserves the stored value; explicitly present zero resets it.

Adding `optional` at the same field number is binary-compatible, but old generated clients still omit zero during normal serialization. An updated server cannot reconstruct whether that old caller omitted progress or assigned zero. [5]

I would keep the legacy RPC's documented behavior and add a separate partial-update RPC or versioned contract for upgraded callers. Another design is an explicit update mask: include `progress` to update it, including a default zero; exclude it to preserve it. The handler must implement those rules, and mask omission must have a documented policy. Adding a mask to the schema does not make old clients send one. [3]

Validate against a stored value such as `80`: under the new contract, omission leaves `80`, explicit zero produces `0`, and explicit `60` produces `60`. Repeat across the Python/Java version combinations and any parse-and-reserialize intermediaries. This is a validation recommendation, not a report of executed integration tests.

## Does Protobuf guarantee exactly the same data and meaning?

Protobuf supplies defined encoding and decoding rules. An old reader may ignore a newly added field, so it may not expose everything a new sender supplied. Compatible parsing also does not establish an unchanged business meaning. Preserve that meaning through the contract, implementation, and cross-version tests. [1, 5]

## References and related notes

1. [Google AIP-180: Backwards compatibility](https://google.aip.dev/180)
2. [Protobuf best practices](https://protobuf.dev/best-practices/dos-donts/)
3. [FieldMask update semantics](https://protobuf.dev/reference/protobuf/google.protobuf/#field-mask)
4. [Introduction to gRPC](https://grpc.io/docs/what-is-grpc/introduction/)
5. [Protobuf field presence and change compatibility](https://protobuf.dev/programming-guides/field_presence/)

Related: [Optional Progress Migration](proto3-optional-progress-migration.md) · [Wire Compatibility vs Application Semantics](protobuf-wire-compatibility-vs-application-semantics.md).
