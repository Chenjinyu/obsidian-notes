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

## Continued discussion: adding a new field without losing old or new data

### Follow-up question — summarized

> If a producer adds a new field while Kafka still contains older messages, how should downstream readers handle both versions safely? Can we canary the new readers and eventually retire the old version?

JC proposed keeping the original field, adding a new `int64` field, and gradually replacing readers through a canary release. The additive approach is useful. The refinements are to upgrade readers before producers depend on the new field, keep both representations usable during the transition, and promote based on correct processing rather than waiting for older records to disappear.

### What “until every reader is upgraded” means

It refers to the **deployed reader applications**, not to draining older messages from Kafka. Editing a producer's `.proto` does not automatically update another service's generated code or deployed application.

For binary Protobuf, changing the same field from `int32` to `int64` while keeping its number can still permit parsing. Both readers preserve a value such as `60`. But `3,000,000,000` exceeds the signed `int32` maximum of `2,147,483,647`; an old decoder can truncate it without reporting a parse failure. The decoded number can therefore differ from the sent number. [2]

A coordinated rollout does not require simultaneous deployment. Keep outgoing values within the signed `int32` range, `-2,147,483,648` through `2,147,483,647`, until all relevant readers support the wider values. Regenerate code, update application variables and storage where needed, and test numeric equality as well as successful decoding.

Protobuf's general best practice is to avoid changing an existing field's type. Adding a new field or introducing a versioned contract is often easier to manage, especially when consumers deploy independently. [5]

### Example: retain the original field and add an optional replacement

This is an illustrative count event, separate from the original optional-progress interview exercise. Keep the existing field's number and business meaning; assign the replacement a fresh, never-used number. [2]

```proto
syntax = "proto3";

message JobCountEvent {
  int32 count = 1;               // Existing representation.
  optional int64 count_v2 = 2;   // New representation with explicit presence.
}
```

The replacement has the same units and meaning as the original count, but supports a wider numeric range. Adding a field makes the binary message parseable by old readers; it does not make their application logic understand the new field. [2]

An upgraded Python consumer uses the regenerated message class:

```python
def read_count(event: JobCountEvent) -> int:
    # Prefer the new representation whenever it was supplied.
    # Explicit zero is valid, so do not use "if event.count_v2".
    if event.HasField("count_v2"):
        return event.count_v2

    # Older Kafka records and older producers have only the legacy field.
    return event.count
```

`HasField` checks whether the optional field was supplied in the message, not which software version produced it. Validate the resulting count against the agreed business rules before persisting or acting on it. [3]

| Record shape | Old reader | Upgraded reader |
|---|---|---|
| Original `count = 60` only | Uses `60` | Falls back to `count` and uses `60` |
| Both fields contain `60` | Uses original `60`; ignores the new field | Prefers `count_v2` and uses `60` |
| Both fields explicitly assigned `0` | Original getter returns `0` | New field is present; uses `0` |
| New field contains `3,000,000,000`; original omitted | Original getter returns default `0`: incorrect for this event | Uses `3,000,000,000` |

The final row must **not** reach an application that still relies on the old field. New-field addition prevents a binary parsing failure; it does not guarantee correct business behavior for old readers.

### Production rollout: readers first, wider values last

| Phase | Reader behavior | Producer behavior | Condition for advancing |
|---|---|---|---|
| Prepare | Regenerate code; support new-field presence and legacy fallback | Continue legacy output | Tests cover old and new records and actual outcomes |
| Canary readers | Run a small number of upgraded consumers alongside old consumers | Keep legacy output, or write both fields with equal values within the old range | Canary receives representative records; results, errors, and lag are acceptable |
| Complete reader rollout | All relevant consumers support both representations | Keep values within the old range until readiness is verified | Verify every relevant deployment, consumer group, and parsing intermediary |
| Enable wider values | Read the new field; retain fallback for old records | Allow wider values in the new field; populate the old field only when representable | No application that needs these events still relies on the original field |

During dual writing, the producer contract requires both fields to represent the same value. Do not truncate or clamp a large number merely to populate the old field. Reject or defer wider values while old readers must still process those events. If those readers cannot migrate, use a separately controlled versioned contract or topic for incompatible events.

After wider values are enabled, an int32-only rollback cannot safely handle those records. Turning off a producer feature flag stops new wide values; it does not remove wide values already retained in Kafka or storage.

### How the canary works with Kafka

A canary can gradually replace old reader instances with the upgraded version. **Every upgraded instance supports both message shapes from the start.** The percentage describes deployment exposure; it does not mean new readers handle only new-format records.

With normal group-managed consumption, old and new instances can use the same consumer group. Kafka assigns each partition to one consumer in that group at a time and reassigns partitions as membership changes. Therefore, 5% of instances does not necessarily process 5% of records. A canary can receive no partitions, or partitions with very different traffic volumes. Verify actual assignments and exposure. Kafka does not route a record to a particular reader version based on whether `count_v2` is present. [6]

Promote the canary based on decoded values, persisted business outcomes, processing failures, consumer lag, throughput, and behavior during rebalances. A progression such as 5%, 25%, 50%, and 100% is illustrative rather than a precise Kafka message-routing guarantee.

Once upgraded readers successfully take over all partitions, retire the old reader instances. **Old messages may remain in Kafka:** the new readers still handle them through fallback. Reaching 100% in one consumer deployment does not prove that separate consumer groups or downstream applications have migrated.

### Existing Kafka records, offsets, and replay

Updating the schema or application does not rewrite records already stored in Kafka. The new consumer must be able to process the older representation throughout the retention and replay period, including backups or archives that may be restored later. Keep the legacy fallback until old records cannot be encountered, or migrate those records before removing support.

For the same processing application, preserve the consumer group identity and committed offsets across deployment; do not reset to the end of the topic to bypass the older records. Commit only through successfully and durably processed records, and make side effects safe to repeat. A crash or rebalance can cause records to be processed again after the last committed offset. [6]

These offset and retry practices address delivery and processing. Schema compatibility alone does not guarantee that no records are lost; retention, durable writes, failures, and replay also need appropriate handling.

### Validation plan

This is a proposed validation plan, not a claim that production or cross-language integration tests were executed.

- Exercise legacy-only, both-field, explicit-zero, and new-only records with old and new generated Python and Java readers.
- During the overlap period, confirm both fields agree and all values fit within the old range.
- Test the signed int32 boundaries, values immediately outside them, and a value such as `3,000,000,000`. Verify exact decoded and persisted values, not just parse success.
- Replay a representative older Kafka backlog with upgraded consumers. Confirm that absent `count_v2` uses the original field.
- Verify canary partition assignments, representative record exposure, lag, failures, and business results before promotion.
- Exercise restart, rebalance, retry, and rollback without skipping unprocessed records or duplicating business side effects.
- Check intermediaries that deserialize, reconstruct, or convert messages to JSON; these may lose unknown fields even when a binary Protobuf round trip would retain them. [2]

### Suggested English answer for this follow-up

> I would keep the existing field and add an optional int64 replacement with a fresh field number. I would deploy readers first so they prefer the new field when present and otherwise fall back to the original field. During a canary rollout, producers would keep both fields consistent and stay within the old numeric range. Kafka distributes partitions rather than exact traffic percentages, so I would verify actual canary exposure and business results. Once all relevant readers are upgraded, I would enable wider values. I would keep legacy fallback for retained or replayed messages and preserve offset and retry handling during deployment.


## Suggested English interview answer

> Wire compatibility concerns the serialized message: whether different versions can decode it, including any risk of losing information. Application semantics concerns what the decoded data means and how the application uses it. For example, both services might read the integer 1,000, but one interprets it as cents and the other as dollars. I would preserve field numbers and meanings, define missing-field behavior, and verify both decoding and business outcomes while old and new versions coexist.

## References and related notes

1. [Protobuf encoding](https://protobuf.dev/programming-guides/encoding/)
2. [Proto3: Updating a message type](https://protobuf.dev/programming-guides/proto3/#updating)
3. [Protobuf field presence](https://protobuf.dev/programming-guides/field_presence/)
4. [Introduction to gRPC](https://grpc.io/docs/what-is-grpc/introduction/)
5. [Protobuf best practices: changing field types](https://protobuf.dev/best-practices/dos-donts/#dont-change-the-type-of-a-field)
6. [KafkaConsumer: consumer groups, offsets, and processing](https://kafka.apache.org/44/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html)

Related: [Protocol Buffers](../../Backend%20Engineering%20and%20Distributed%20Systems/12-protocol-buffers.md) · [gRPC](../../Backend%20Engineering%20and%20Distributed%20Systems/11-grpc.md).
