---
sr-due: 2026-11-11
sr-interval: 1
sr-ease: 2.5
created: "2026-11-11T13:20:15-06:00"
updated: "2026-11-11T13:31:33-06:00"
timezone: America/Chicago
source: voice-interview
status: answer-and-feedback-recorded
tags:
  - interview
  - protobuf
  - grpc
  - schema-evolution
---

# Proto3 Optional Progress: Partial Updates and Safe Migration

## Interview question

The following preserves the scenario from JC's spoken reading, with wording normalized for readability. The original field number was not clear in the transcript; keep that same number during the proposed change.

> A gRPC job server uses proto3 and binary Protobuf. Existing Python and Java clients were generated from a schema with an implicit-presence `int32 progress` field. The team wants partial updates: omitting progress should leave it unchanged, while explicitly setting progress to zero should reset it to zero. They propose changing the field to `optional int32 progress`, but cannot upgrade all clients at once. Is that schema change alone sufficient to support the intended behavior safely? Explain what the server can observe from old and new clients and how you would validate a safe migration.

## JC's answer — summarized, not a verbatim quotation

- The schema change alone is not sufficient; the intended business behavior needs consideration.
- Proposed `reserved` as a way to preserve or leave progress unchanged.
- Suggested checking whether progress exists before reading or updating it.
- Suggested presence or absence could distinguish old versus new clients or servers.
- Worried that the meaning of zero would be ambiguous and concluded there might be no safe migration.

## Feedback

The high-level conclusion is correct: **binary compatibility does not by itself establish safe partial-update behavior**. Checking presence is relevant, but the explanation needs these corrections:

1. **Use `optional` for presence tracking.** `reserved` blocks reuse of field numbers or names; it does not preserve a job's stored progress. Reserving the active progress field number while also declaring it is invalid.
2. **Check whether this request supplied a value.** Both schema versions define progress. The useful check is request presence, not whether the schema contains a field with that name.
3. **Old clients lose the omitted-versus-zero distinction during serialization.** Their normal generated serializers omit zero. A new reader cannot reconstruct an intent that was not encoded.
4. **Presence does not identify the caller's version.** Both old and new clients can send a nonzero progress value, and both can omit progress.
5. **There is a safe migration strategy.** Preserve legacy behavior and introduce an explicit new update contract. The same change cannot make unchanged old clients express the new zero-reset distinction.

## What an updated server observes

Assume direct binary serialization using the normal generated client code, with no intermediary rewriting the message. The updated server was regenerated with `optional` at the original field number.

| Client schema | Client action | Progress encoded? | New server presence | Accessor value |
|---|---|---|---|---|
| Old implicit | Omit progress | No | Absent | `0` |
| Old implicit | Assign `0` | No | Absent | `0` |
| Old implicit | Assign `60` | Yes | Present | `60` |
| New optional | Omit progress | No | Absent | `0` |
| New optional | Assign `0` | Yes | Present | `0` |
| New optional | Assign `60` | Yes | Present | `60` |

The first two rows are indistinguishable to the new server. Under the new partial-update policy, both leave stored progress unchanged, so an unchanged old client cannot request a reset to zero through this field alone. Whether applying that policy to legacy traffic breaks existing behavior depends on the old API contract. [1]

An updated Python receiver can use `request.HasField("progress")`; Java uses `request.hasProgress()`. Reading the accessor alone is insufficient: an absent optional integer still reads as zero. [2]

## Correct new-contract application logic

This illustrative Python fragment assumes an updated message class and the new partial-update contract:

```python
if request.HasField("progress"):
    job.progress = request.progress
# Otherwise, leave job.progress unchanged.
```

Apply the API's domain validation before persisting a supplied value. Checking presence does not validate its allowed range.

This logic supports absent versus explicit zero from upgraded clients. It does not repair the ambiguity in old-client messages.

## What an old receiver observes

A receiver still using implicit presence reads zero for either absence or an explicitly encoded zero. Its ordinary generated API cannot distinguish them. Updating business code alone does not give an old message class optional presence tracking.

If an old-schema intermediary parses a new client's explicit-zero message and reserializes it, zero is omitted on output. The next optional-aware receiver then observes absence. Raw byte forwarding does not introduce this particular parse-and-reserialize loss. [1]

## A safe migration I would propose

**Recommendation:** keep the legacy RPC's established semantics, and add a separate partial-update RPC or versioned contract. The following plan is a design recommendation for this scenario:

1. Document the current legacy behavior for omitted and zero progress; do not silently reinterpret existing calls.
2. Add a new partial-update RPC with an explicit-presence request. Keep the existing field number stable if evolving the same message; never reserve an active number.
3. Implement the new handler's policy: absent means preserve; present means set, including zero. Regenerate message code and validate domain constraints.
4. Deploy servers supporting the new contract before enabling clients to call it. Route new-contract traffic only to compatible servers.
5. Upgrade Python and Java clients gradually. Their use of the new RPC makes the contract explicit; presence is not a version detector.
6. Observe outcomes and preserve rollback behavior. Retire the legacy path only after usage and stored/retried traffic allow it.

An alternative is an explicit `FieldMask` on a clearly defined upgraded update contract. Including `progress` in the mask means update it even when the scalar reads zero; excluding it means leave it unchanged. Define or require the mask explicitly. An unchanged old client will not start sending a mask merely because the schema gained one. [3]

## How I would validate the migration

This is a **validation plan**, not a claim that cross-language integration tests were executed.

- Test old and new generated Python and Java clients against old and new server versions.
- Exercise omitted progress, explicitly assigned zero, and a nonzero value. Check serialized field presence as well as the decoded accessor.
- Begin with a stored progress such as `80`. Under the new contract, omission must keep `80`, explicit zero must produce `0`, and a supplied `60` must produce `60`.
- Verify legacy calls still produce the old documented behavior, including the ambiguous omitted/zero case.
- Verify that unsupported new RPCs are not treated as successful updates on old servers.
- Exercise any proxy, queue consumer, or other component that parses and reserializes the same request. Include explicit-zero round trips.
- Cover retries, rollback, and domain-invalid values, checking persisted results rather than parse success alone.

## Suggested English interview answer

> No. Keeping the field number and changing the field to optional is binary-compatible, but the schema change alone does not provide safe partial-update behavior for every client. Old proto3 clients serialize an omitted progress and an explicitly assigned zero identically, so the server cannot recover that distinction. New optional clients can express both cases. I would regenerate server code, use presence checks for the new update logic, preserve the legacy contract, and introduce an explicit partial-update RPC or update mask. I would validate omitted, zero, and nonzero updates across client and server versions, including intermediaries.

## Communication feedback

Lead with the conclusion, then explain **old clients**, **new clients**, **server logic**, and **migration validation** in that order.

Useful wording: "The server checks whether progress was explicitly provided in this request." This is clearer than "the server checks whether the progress field exists," which could refer to the schema.

## Continued explanation: client/server roles and integer validation

### JC's revised understanding — summarized

After reviewing the definitions, JC identified `optional` as the relevant presence mechanism and emphasized that the communicating services need an agreed contract. He proposed checking progress with `HasField`, but still associated presence with detecting an old or new client. He also asked whether the server must verify that deserialized progress remains an integer and how to name the two communicating services.

### Naming the participants

For a particular RPC, **the caller is the gRPC client, and the service handling the call is the gRPC server**. Both participants may be backend microservices. [5]

A clear way to describe the example is: "Service A acts as the gRPC client and sends an update request to Service B, the gRPC server."

Client and server describe roles in that call. The same service can handle incoming calls as a server and initiate downstream calls as a client. In this interview scenario, the update client supplies progress, and the job server checks its presence in the incoming request.

### What the presence check establishes

With the updated optional-aware receiver:

- `HasField("progress")` false means progress was absent from this parsed request. Reading the accessor still returns the default integer zero.
- Presence true with value zero means an explicitly encoded zero arrived.
- The new partial-update contract defines the first case as preserve and the second as reset.

This does **not** establish whether the caller used old or new generated code. Either client version may omit progress. Moreover, an old implicit-presence client explicitly assigning zero still omits that field during normal serialization. Presence identifies an encoded field, not the caller's software version. [1, 2]

### What to validate after parsing

For an agreed schema, the generated API exposes the declared integer value; checking `isinstance` again is not the main migration safeguard. Validate whether a value was supplied and whether it obeys the application's rules. For example, **if** progress is defined as a percentage, validate the agreed range such as 0–100. A value of 150 can be a valid Protobuf integer while violating that business rule. [2]

To establish cross-version correctness, verify actual decoded values and persisted update outcomes. Checking only that the value is an integer cannot reveal lost presence or a changed business meaning.

## References and related notes

1. [Field presence: semantic differences and change compatibility](https://protobuf.dev/programming-guides/field_presence/)
2. [Python generated code: explicit and implicit field presence](https://protobuf.dev/reference/python/python-generated/#fields)
3. [FieldMask update semantics](https://protobuf.dev/reference/protobuf/google.protobuf/#field-mask)
4. [Proto3 guide: optional and reserved fields](https://protobuf.dev/programming-guides/proto3/)
5. [Introduction to gRPC](https://grpc.io/docs/what-is-grpc/introduction/)

Related: [Wire Compatibility vs Application Semantics](protobuf-wire-compatibility-vs-application-semantics.md).
