---
sr-due: 2026-10-21
sr-interval: 1
sr-ease: 2.5
---

# HMAC, UTF-8, ASCII, and Raw Bytes — Authenticating Webhooks

## 1. What problem does HMAC solve?

Someone can send an HTTP POST to your webhook endpoint. How do you distinguish the expected sender from a forged request, and how do you detect a modified body?

**HMAC means Hash-based Message Authentication Code.** The sender and receiver share a secret key. The sender calculates an authentication tag from that key and the exact message bytes. The receiver calculates the tag again and compares it with the received tag.

If the tag matches, it provides evidence that a holder of the secret authenticated those bytes. HMAC does not distinguish two different parties who both know the same secret. It is a symmetric message authentication code, not a public/private-key digital signature providing non-repudiation. Webhook documentation often informally calls the tag a “signature.”

HMAC does not encrypt the message. HTTPS provides transport encryption. HMAC also does not prove the message is new, that its data is true, or that your business logic has not processed it already.

## Real-world use cases

| Real-world scenario | What needs protection or a shared byte format | Why HMAC or explicit encoding fits |
|---|---|---|
| Payment webhook verification | A store must detect forged or modified payment events. | The provider and receiver calculate an HMAC over the provider-defined bytes using a shared secret. |
| Repository webhook verification | A CI service receives a request claiming that code was pushed. | An HMAC can authenticate the payload before the service decides whether to start a build. |
| Partner warehouse integration | A partner submits shipment instructions through an API with a documented HMAC authentication scheme. | Both parties authenticate the agreed request representation, which may include method, path, timestamp, and body. |
| Expiring private download link | A backend issues a link whose resource ID and expiry must not be editable by its holder. | A server-verified HMAC can authenticate those fields without exposing the signing secret. This requires a carefully specified format and access policy. |
| Authenticated batch-file delivery | A partner sends a file and an authentication tag through an agreed integration. | Verifying the HMAC over the exact file bytes detects modification by someone without the shared key; it does not hide the file's contents. |
| International customer notifications | A webhook body contains Chinese names, accented addresses, or emoji. | UTF-8 defines how that text becomes bytes. The receiver verifies the original request bytes rather than reserializing parsed JSON. |
| Cross-language signed requests | A Python sender and a Java receiver must produce the same authentication tag. | Both implementations need identical encodings, field order, separators, and byte sequences. Different-looking code can interoperate only if the signed bytes agree. |

**Walk through an international order:** the sender serializes a JSON body containing `"customer": "王小明"` to UTF-8 bytes. If its documented signature scheme is `timestamp + "." + raw_body`, it encodes the decimal timestamp as ASCII, adds the literal byte `b"."`, and appends the body bytes. The receiver follows that same scheme using the received body. ASCII and UTF-8 produce the same bytes for decimal digits; using ASCII here expresses that the timestamp format only permits those characters. The period is a protocol-defined separator, not an HMAC requirement.

For webhook scenarios, a signed timestamp plus a freshness check can limit replay age, while an event ID and durable deduplication prevent repeat processing. Neither property comes from HMAC alone. Follow the actual provider's signing specification rather than imposing this illustrative format on every webhook.

**Interview practice:** explain which party knows the secret, exactly which bytes are authenticated, and why a valid tag neither encrypts the data nor proves that an event is new.

## 2. Text versus bytes — the questions JC asked

Python `str` represents text; `bytes` represents a sequence of byte values. Encoding defines how text becomes bytes. HMAC consumes bytes because cryptographic operations act on exact byte sequences.

**ASCII** has 128 codes: English letters, digits, punctuation, and controls. **UTF-8** represents Unicode code points with one to four bytes. A visible character can contain several code points, so “four bytes maximum per visible character” is not generally correct.

```python
assert "123".encode("ascii") == "123".encode("utf-8")
assert ".".encode("utf-8") == b"."
assert len("你".encode("utf-8")) == 3

text = '{"status":"completed"}'
body = text.encode("utf-8")
print(type(text), type(body))  # str, bytes
```

The timestamp contains digits, so ASCII and UTF-8 produce identical bytes for it. ASCII is a choice, not an HMAC restriction. UTF-8 supports the broader text that may occur in a JSON body.

The `b` prefix makes a literal bytes object. In `timestamp_bytes + b"." + body`, the dot creates an explicit boundary. Without framing, `b"12" + b"345"` and `b"123" + b"45"` both produce `b"12345"`. HMAC does not require a dot; both parties must agree on the precise format. Choose framing suitable for the allowed field contents.

## 3. Why sign the timestamp as well as the body?

If only the body is authenticated, an attacker could attach a fresh, unauthenticated timestamp to an old valid message. Authenticating both prevents such edits. The receiver checks a freshness window using a reasonably synchronized clock.

A valid request can still be replayed during that window. Deduplicate a stable event ID and make its effect idempotent. When a provider legitimately retries much later, it may sign each delivery with a fresh timestamp while retaining the event's original ID; verify the provider's actual protocol.

## 4. Runnable signing and verification module

Save as `webhook_security.py`. Only Python's standard library is needed. This is our illustrative protocol, not GitHub's or another provider's exact signature format.

```python
import hashlib
import hmac
import re
import time

def sign(secret: bytes, timestamp: str, body: bytes) -> str:
    message = timestamp.encode("ascii") + b"." + body
    return hmac.new(secret, message, hashlib.sha256).hexdigest()

def verify(secret, timestamp, body, signature, *, now=None, tolerance=300):
    if not isinstance(timestamp, str) or not isinstance(signature, str):
        return False
    if not re.fullmatch(r"[0-9]{1,12}", timestamp):
        return False
    if not re.fullmatch(r"[0-9a-f]{64}", signature):
        return False
    current_time = time.time() if now is None else now
    if abs(current_time - int(timestamp)) > tolerance:
        return False
    expected = sign(secret, timestamp, body)
    return hmac.compare_digest(expected, signature)

if __name__ == "__main__":
    secret = b"local-demo-only"
    body = b'{"event_id":"evt-123","status":"completed"}'
    timestamp = str(int(time.time()))
    signature = sign(secret, timestamp, body)
    assert verify(secret, timestamp, body, signature)
    assert not verify(secret, timestamp, body + b" ", signature)
    assert not verify(secret, timestamp, body, signature, now=int(timestamp) + 301)
    print("Valid, modified-body, and stale-delivery checks passed")
```

The strict tag format matches this demo's lowercase SHA-256 hex convention. Some providers prefix signatures, send multiple tags during rotation, or sign different fields. Adapt verification to the documented scheme.

## 5. Sending and receiving the exact bytes

```python
import json
import time
from webhook_security import sign

body = json.dumps(
    {"event_id": "evt-123", "message": "你好"},
    ensure_ascii=False, separators=(",", ":"),
).encode("utf-8")
timestamp = str(int(time.time()))
headers = {
    "Content-Type": "application/json",
    "X-Webhook-Timestamp": timestamp,
    "X-Webhook-Signature": sign(b"local-demo-only", timestamp, body),
}
# With an HTTPX client: client.post(url, content=body, headers=headers)
```

At the receiver, `await request.body()` is already bytes. Verify before parsing JSON. Never parse and reserialize as a substitute for reading the raw body. Semantically equal JSON can differ in whitespace, ordering, escapes, and encoding; HMAC authenticates those exact differences.

`hmac.compare_digest` avoids ordinary value-dependent short-circuit comparison behavior. It is one component of verification, not a replacement for secure key storage or correct signed-message construction.

## 6. Supporting mechanisms

| Requirement | Mechanism |
|---|---|
| Confidentiality in transit | HTTPS and certificate validation |
| Correct source | High-entropy per-provider or per-endpoint secret |
| Limit replay age | Authenticated timestamp and freshness check |
| Prevent repeated effects | Stable event ID and transactional idempotency |
| Rotate credentials | Key identifiers or a bounded overlap of accepted keys |
| Avoid resource abuse | Body-size limits before expensive processing |
| Investigate failures | Log event IDs/rejection categories, never secrets |

Provision secrets through a secret manager or secure deployment configuration. An environment variable is useful in local examples but is not a complete key lifecycle strategy. Authentication of the sending system is separate from authorization of the event's tenant, resource, and event type.

## 7. Interview answer and practice

“I would verify an HMAC over the provider's exact signed byte sequence, compare it securely, and check authenticated freshness information if the protocol supplies it. I would still deduplicate event IDs because an authentic request can be repeated.”

1. Why does HMAC need bytes instead of a Python string?
2. Why can both ASCII and UTF-8 encode the timestamp identically?
3. What does b"." add, and why is it not a cryptographic requirement?
4. Why can valid signatures still accompany duplicate requests?
5. What happens if a proxy changes whitespace in the body?
6. How does HMAC differ from encryption and a public-key signature?

References: [Python hmac](https://docs.python.org/3/library/hmac.html), [HMAC specification](https://www.rfc-editor.org/rfc/rfc2104.html), [Provider example: GitHub signature validation](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries). Next: [Webhooks](05-webhooks.md).
