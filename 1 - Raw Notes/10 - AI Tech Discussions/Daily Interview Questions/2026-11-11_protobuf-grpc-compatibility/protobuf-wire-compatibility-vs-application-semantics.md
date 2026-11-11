---
sr-due: 2026-11-11
sr-interval: 1
sr-ease: 2.5
created: "2026-11-11T13:13:11-06:00"
timezone: America/Chicago
source: voice-discussion
status: discussion-and-interview-feedback
tags:
  - interview
  - protobuf
  - grpc
---

# Protobuf and gRPC: Wire Compatibility vs Application Semantics

## Discussion question

> What do wire compatibility and application semantics mean? How do they differ, and why should we check both when evolving a gRPC API that uses Protobuf?

This question summarizes the initial clarification discussed on November 11, 2026. The interview scenario subsequently read aloud by JC, his answer, and the feedback are recorded in [Optional Progress: Partial Updates and Safe Migration](proto3-optional-progress-migration.md).

## The two checks

| Concept | Meaning | Question to ask |
|---|---|---|
| Wire compatibility — 傳輸格式相容性 | Whether different schema versions can exchange and decode the serialized representation, subject to the change's specific limitations. | Can the receiver parse these bytes, and could values or information be lost? |
| Application semantics — 資料的業務含義與處理規則 | The meaning the application assigns to decoded data and the behavior it performs. | Do both sides agree on units, defaults, rules, and the intended operation? |

**A successful parse alone does not prove that a change is safe.**

## Why is it called "wire"?

Developers use "on the wire" to mean the bytes transmitted between systems. The expression also applies over Wi-Fi; a physical cable is not required.

Consider a Python client calling a Java server:

1. Python code creates a Protobuf message.
2. Protobuf serializes it into bytes.
3. gRPC carries the message as part of the remote call.
4. Java's Protobuf code decodes the bytes.
5. The Java application interprets the values and performs its operation.

The **wire format** is the serialized representation between the applications. Protobuf's binary encoding identifies fields by their numbers and includes wire types that tell a parser how to read or skip their payloads. Field names and business units are not automatically transmitted as descriptive metadata. [1]

The term is **compatibility** (相容性). **Capability** means 能力.

## Where gRPC and different languages fit

gRPC provides remote service calls and uses Protobuf by default for message serialization. Generated client code makes calling a remote method convenient; generated message code handles serialization and parsing. [4]

A common format helps Python and Java interoperate. However, the distinction also matters when both services use Python: they can run different schema versions or apply different business rules.

For these message-evolution checks, backward compatibility means a newer reader can handle older messages; forward compatibility means an older reader can handle newer messages. Evaluate both directions when old and new versions coexist.

## Example: identical value, different meaning

Both versions use the same message definition:

```proto
syntax = "proto3";

message PaymentRequest {
  int64 amount = 1;
}
```

Here, `1` is the **field number**, not the payment amount. Application code can set `amount` to `1000`.

Suppose the original contract says `amount` represents US cents. A Python client sends `1000`, intending **USD 10.00**.

An updated Java server still decodes exactly `1000`, but its application logic now interprets the field as US dollars and charges **USD 1,000.00**.

| Check | Result |
|---|---|
| Field number remains `1` | Preserved |
| Declared type remains `int64` | Preserved |
| Decoded value remains `1000` | Preserved |
| Agreed unit remains cents | Broken |
| Intended charge remains USD 10.00 | Broken |

The wire representation did not change. The application contract changed.

This is an illustrative business failure: Protobuf encodes the integer, but does not independently decide what monetary unit that integer represents.

**Deserialization does not automatically strip meaning.** It reconstructs values according to the schema. Application code interprets those values using the agreed contract.

## "Wire-compatible" needs qualification

The Protobuf guide distinguishes several categories of binary schema changes. [2]

- **Wire-safe:** Adding a field with a fresh field number lets older binary readers skip the unknown field. The application still needs sensible behavior when the field is absent or ignored.
- **Conditionally wire-compatible:** Changing `int32` to `int64` permits parsing across versions, but an old `int32` reader can truncate an out-of-range value. Keep writing values within the old range until all relevant readers support the wider range.
- **Wire-unsafe:** Changing an existing field number breaks the association between the transmitted field and the expected field. It need not produce a parse error to break compatibility.

These rules concern **binary Protobuf**. ProtoJSON has different compatibility rules. Generated source APIs can also break independently of the binary representation.

## Presence and collection semantics

Presence is another place where representation and business meaning interact. [3]

With proto3 `optional int32 quantity = 2;`, code can distinguish an absent field from one explicitly set to zero.

A PATCH-style application might define:

- Absent quantity: keep the existing quantity.
- Explicit zero: replace the existing quantity with zero.

Those are application rules; `optional` supplies presence information, not that business policy.

A `repeated` field does not distinguish an omitted collection from an empty collection through presence tracking. An API that must distinguish "leave roles unchanged" from "clear all roles" needs an explicit update mechanism, such as a field mask.

## Questions and corrections from our discussion

| Question or initial understanding | Clarification |
|---|---|
| Why use the word "wire"? | It refers to the serialized bytes exchanged between systems. |
| Is this about Python communicating with Java? | That is one use case. Version compatibility matters even when both services use the same language. |
| Does application semantics mean the integer stays an integer and keeps the same value? | Preserving the type and value is insufficient. Both services must also agree on what the integer represents and how to act on it. |
| Does deserialization remove meaning? | It reconstructs values; the application interprets them according to the contract. |

JC correctly connected Protobuf with exchanging data across languages. The key refinement was distinguishing preservation of a value from preservation of its business meaning.

## Preserving both during deployment

The following is an application of these rules to the payment example:

1. Document units, currency, valid ranges, and missing-field behavior.
2. Keep existing field numbers and their agreed meanings stable.
3. Add a clearly named field or a versioned operation for a new representation.
4. Define how readers handle old messages and how writers handle older readers. Adding a field does not make older services understand it.
5. Deploy compatible readers before enabling writers to depend on new behavior.
6. Verify old-writer/new-reader and new-writer/old-reader combinations, checking business outcomes as well as parsing.
7. Account for persisted messages, retries, and rollback before retiring the old representation. Reserve deleted field numbers.

## Suggested English interview answer

> Wire compatibility concerns the serialized message: whether different versions can decode it, including any risk of losing information. Application semantics concerns what the decoded data means and how the application uses it. For example, both services might read the integer 1,000, but one interprets it as cents and the other as dollars. I would preserve field numbers and meanings, define missing-field behavior, and verify both decoding and business outcomes while old and new versions coexist.

## References and related notes

1. [Protobuf encoding](https://protobuf.dev/programming-guides/encoding/)
2. [Proto3: Updating a message type](https://protobuf.dev/programming-guides/proto3/#updating)
3. [Protobuf field presence](https://protobuf.dev/programming-guides/field_presence/)
4. [Introduction to gRPC](https://grpc.io/docs/what-is-grpc/introduction/)

Related: [Protocol Buffers](../../Backend%20Engineering%20and%20Distributed%20Systems/12-protocol-buffers.md) · [gRPC](../../Backend%20Engineering%20and%20Distributed%20Systems/11-grpc.md).
