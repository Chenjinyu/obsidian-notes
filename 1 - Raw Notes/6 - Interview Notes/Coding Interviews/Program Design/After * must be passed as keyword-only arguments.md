Date: 2026-01-11
Course:
Tags: 

# Content

Great question — this `*` is **subtle but extremely powerful**, especially for **API design**.

---

## What does `*` mean in function parameters?

In Python, `*` means:

> **All parameters after `*` must be passed as keyword-only arguments.**

So in your example:

```python
class LLMFactory(Protocol):
    def __call__(
        self,
        provider: str,
        *,
        timeout: int = 30
    ) -> "LLMService":
        ...
```

### This enforces:

* `provider` → positional **or** keyword
* `timeout` → **keyword-only**

---

## What calls are allowed?

### ✅ Valid calls

```python
factory("openai")
factory("openai", timeout=10)
factory(provider="openai", timeout=10)
```

### ❌ Invalid calls

```python
factory("openai", 10)  # ❌ positional timeout not allowed
```

---

## Why this is a big deal (real API design value)

### 1️⃣ Prevents fragile APIs

Without `*`:

```python
def __call__(self, provider: str, timeout: int = 30):
    ...
```

This allows:

```python
factory("openai", 10)
```

If you later add a new parameter:

```python
def __call__(self, provider, retries=3, timeout=30):
```

🔥 **Breaking change** — positional arguments shift.

With `*`, **future-safe APIs**:

```python
def __call__(self, provider: str, *, timeout: int = 30, retries: int = 3):
```

No breaking changes.

---

### 2️⃣ Self-documenting APIs

```python
factory("openai", timeout=10)
```

vs

```python
factory("openai", 10)  # what is 10?
```

Keyword-only arguments improve:

* Readability
* Maintainability
* Code reviews

---

### 3️⃣ Encourages correct usage

When APIs get complex:

* Configuration should be explicit
* Options should not be positional

This is exactly why:

* FastAPI
* boto3
* SQLAlchemy

use keyword-only parameters heavily.

---

### 4️⃣ Better type-checking & IDE support

With `*`:

* IDEs suggest keyword names
* Fewer accidental mistakes
* Better autocomplete

---

## Why this matters even more in `Protocol`

Remember:

> `Protocol` defines **contracts**, not implementations.

So:

* You want **stable contracts**
* You want **backward compatibility**
* You want **extensible APIs**

Keyword-only args are **one of the best tools** for that.

---

## Real-world analogy

Think of `*` as:

> “Configuration parameters must be named.”

Just like JSON configs:

```json
{
  "timeout": 30,
  "retries": 3
}
```

You don’t pass configs by position.

---

## When should you use `*`?

### ✅ Use `*` when:

* Designing public APIs
* Using Protocols
* Expect future extension
* Parameters are optional / configuration

### ❌ Avoid `*` when:

* Tiny internal helpers
* Performance-critical inner loops
* Obvious mathematical functions

---

## TL;DR

* `*` makes parameters **keyword-only**
* Prevents breaking changes
* Improves readability
* Ideal for Protocol / API design
* Makes your API future-proof

---

If you want next:

* `*` vs `**kwargs`
* Keyword-only args in dataclasses
* How FastAPI uses `*` implicitly
* Designing stable APIs in Python

Just say the word.


# Note


# Reference

