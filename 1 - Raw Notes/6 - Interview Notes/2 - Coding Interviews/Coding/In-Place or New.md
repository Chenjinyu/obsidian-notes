Date: 2026-02-27
Course:
Tags: [[Python]]

This is a **very good Python question**, and you're right to be suspicious here.  
Let's make this **systematic and precise**, not hand-wavy.

---
# 1️⃣ Big rule first (memorize this)

> **In Python, whether something changes in-place is a property of the _object type_, not the syntax.**

This means:
- `object.method()` **may** mutate
- `object.method()` **may** return a new object
- You **cannot tell** just by seeing `obj.method()`
You must know the method.

---
# 2️⃣ Common Python objects that **mutate in-place**
Here's the full comparison — every function from your document paired with its standalone equivalent:
## List Operations

| In-place method    | Standalone equivalent            | Difference                                                               |
| ------------------ | -------------------------------- | ------------------------------------------------------------------------ |
| `lst.append(x)`    | `lst + [x]`                      | `+` returns new list `O(n)` space; `.append()` is `O(1)` space           |
| `lst.extend(iter)` | `lst + list(iter)`               | `+` returns new list `O(n)` space; `.extend()` is `O(1)` space           |
| `lst.insert(i, x)` | `lst[:i] + [x] + lst[i:]`        | slicing returns new list `O(n)` space                                    |
| `lst.remove(x)`    | `[v for v in lst if v != x]`     | comprehension removes **all** x, `.remove()` removes **first** x only    |
| `lst.pop()`        | `lst[-1]` (just read, no remove) | no real equivalent that both reads + removes in one step                 |
| `lst.reverse()`    | `reversed(lst)` / `lst[::-1]`    | see detailed table above                                                 |
| `lst.sort()`       | `sorted(lst)`                    | see detailed table above                                                 |
| `lst.clear()`      | `lst = []`                       | rebind creates new list object; `.clear()` keeps same object, empties it |
### Complexity comparison

| In-place           | Time         | Space  | Standalone            | Time         | Space    |
| ------------------ | ------------ | ------ | --------------------- | ------------ | -------- |
| `lst.append(x)`    | `O(1)`       | `O(1)` | `lst + [x]`           | `O(n)`       | `O(n)`   |
| `lst.extend(iter)` | `O(k)`       | `O(1)` | `lst + list(iter)`    | `O(n+k)`     | `O(n+k)` |
| `lst.insert(i, x)` | `O(n)`       | `O(1)` | `lst[:i]+[x]+lst[i:]` | `O(n)`       | `O(n)`   |
| `lst.remove(x)`    | `O(n)`       | `O(1)` | list comprehension    | `O(n)`       | `O(n)`   |
| `lst.pop()`        | `O(1)`       | `O(1)` | `lst[-1]` (read only) | `O(1)`       | `O(1)`   |
| `lst.reverse()`    | `O(n)`       | `O(1)` | `lst[::-1]`           | `O(n)`       | `O(n)`   |
| `lst.reverse()`    | `O(n)`       | `O(1)` | `reversed(lst)`       | `O(1)`*      | `O(1)`   |
| `lst.sort()`       | `O(n log n)` | `O(n)` | `sorted(lst)`         | `O(n log n)` | `O(n)`   |
| `lst.clear()`      | `O(n)`       | `O(1)` | `lst = []`            | `O(1)`       | `O(1)`** |
* lazy iterator, `O(n)` to fully consume ** old list still exists in memory until GC collects it
## Dict Operations

|In-place method|Standalone equivalent|Difference|
|---|---|---|
|`d.update({k:v})`|`{**d, k: v}`|unpacking returns new dict `O(n)` space|
|`d.pop(k)`|`d[k]` then `del d[k]`|two steps vs one atomic operation|
|`d.popitem()`|no clean equivalent|would need `next(iter(d.items()))` + `del`|
|`d.clear()`|`d = {}`|rebind creates new dict; `.clear()` keeps same object|
|`d.setdefault(k,v)`|`d[k] if k in d else v`|`.setdefault()` also **writes** v if missing; ternary just reads|
|`del d[k]`|`{k2:v for k2,v in d.items() if k2 != k}`|comprehension returns new dict|
### Complexity comparison

|In-place|Time|Space|Standalone|Time|Space|
|---|---|---|---|---|---|
|`d.update({k:v})`|`O(k)`|`O(1)`|`{**d, **other}`|`O(n+k)`|`O(n+k)`|
|`d.pop(k)`|`O(1)`|`O(1)`|read + `del`|`O(1)`|`O(1)`|
|`d.popitem()`|`O(1)`|`O(1)`|`iter` + `del`|`O(1)`|`O(1)`|
|`d.clear()`|`O(n)`|`O(1)`|`d = {}`|`O(1)`|`O(1)`*|
|`d.setdefault(k,v)`|`O(1)`|`O(1)`|ternary (read only)|`O(1)`|`O(1)`|
|`del d[k]`|`O(1)`|`O(1)`|dict comprehension|`O(n)`|`O(n)`|
|`d.copy()`|❌ not in-place|—|`dict(d)` / `{**d}`|`O(n)`|`O(n)`|
* old dict object lingers until GC
## Set Operations

|In-place method|Standalone equivalent|Difference|
|---|---|---|
|`s.add(x)`|`s \| {x}`|`\|` returns new set `O(n)` space|
|`s.remove(x)`|`s - {x}`|`-` returns new set; `.remove()` raises `KeyError` if missing|
|`s.discard(x)`|`s - {x}`|`-` returns new set; `.discard()` silently ignores if missing|
|`s.pop()`|no equivalent|removes arbitrary element, no standalone equivalent|
|`s.clear()`|`s = set()`|rebind vs empty same object|
|`s.update(other)`|`s \| other`|`\|` returns new set|
|`s.intersection_update(other)`|`s & other`|`&` returns new set|
|`s.difference_update(other)`|`s - other`|`-` returns new set|
### Complexity comparison

|In-place|Time|Space|Standalone|Time|Space|
|---|---|---|---|---|---|
|`s.add(x)`|`O(1)`|`O(1)`|`s \| {x}`|`O(n)`|`O(n)`|
|`s.remove(x)`|`O(1)`|`O(1)`|`s - {x}`|`O(n)`|`O(n)`|
|`s.discard(x)`|`O(1)`|`O(1)`|`s - {x}`|`O(n)`|`O(n)`|
|`s.clear()`|`O(n)`|`O(1)`|`s = set()`|`O(1)`|`O(1)`*|
|`s.update(other)`|`O(k)`|`O(1)`|`s \| other`|`O(n+k)`|`O(n+k)`|
|`s.intersection_update(other)`|`O(min(n,k))`|`O(1)`|`s & other`|`O(min(n,k))`|`O(n)`|
|`s.difference_update(other)`|`O(k)`|`O(1)`|`s - other`|`O(n)`|`O(n)`|
* old set object lingers until GC

## Heapq Operations
`heapq` has no in-place vs standalone split — it's a module, not a method. But the relevant comparisons are:

|heapq operation|Standalone equivalent|Difference|
|---|---|---|
|`heapq.heapify(lst)`|`sorted(lst)`|`sorted` gives sorted list `O(n log n)`; `heapify` only guarantees heap property `O(n)`|
|`heapq.heappush(h, x)`|`h.append(x); h.sort()`|sort is `O(n log n)`; push is `O(log n)`|
|`heapq.heappop(h)`|`min(h)` then `remove`|`min+remove` is `O(n)`; `heappop` is `O(log n)`|
|`heapq.nlargest(k, iter)`|`sorted(iter)[-k:]`|both `O(n log n)` but `nlargest` is `O(n log k)` — faster for small k|
|`heapq.nsmallest(k, iter)`|`sorted(iter)[:k]`|same — `O(n log k)` vs `O(n log n)`|
### Complexity comparison

|heapq|Time|Space|Standalone|Time|Space|
|---|---|---|---|---|---|
|`heapq.heapify(lst)`|`O(n)`|`O(1)`|`sorted(lst)`|`O(n log n)`|`O(n)`|
|`heapq.heappush(h,x)`|`O(log n)`|`O(1)`|`append+sort`|`O(n log n)`|`O(n)`|
|`heapq.heappop(h)`|`O(log n)`|`O(1)`|`min+remove`|`O(n)`|`O(1)`|
|`heapq.nlargest(k,iter)`|`O(n log k)`|`O(k)`|`sorted()[-k:]`|`O(n log n)`|`O(n)`|
|`heapq.nsmallest(k,iter)`|`O(n log k)`|`O(k)`|`sorted()[:k]`|`O(n log n)`|`O(n)`|
## The Universal Pattern

```
In-place method     → O(1) extra space, mutates original
Standalone function → O(n) extra space, returns new object, original safe
```

The one exception worth memorizing: **`reversed()` and `iter()`-based equivalents are `O(1)` space** because they're lazy iterators, not materialized collections.

---
## 🔹 `bytearray`

- Mutable bytes
- Almost all methods mutate in-place

---
# 3️⃣ Objects that are **immutable** (never change in-place)
These **cannot** be mutated:
- `int`
- `float`
- `bool`
- `str`
- `tuple`
- `frozenset`
### Example
```python
s = "abc"
s.replace("a", "x")  # returns new string
# s is still "abc"
```

---
# 4️⃣ Methods that look mutating but are NOT
These **return new objects**:

| Expression       | In-place? | Time       | Space |
| ---------------- | --------- | ---------- | ----- |
| `sorted(nums)`   | ❌         | O(n log n) | O(n)  |
| `nums + [1]`     | ❌         | O(n)       | O(n)  |
| `str.replace()`  | ❌         | O(n)       | O(n)  |
| `str.lower()`    | ❌         | O(n)       | O(n)  |
| `dict.copy()`    | ❌         | O(n)       | O(n)  |
| `list.copy()`    | ❌         | O(n)       | O(n)  |
| `set.union()`    | ❌         | O(n+k)     | O(n+k)|

---
# 5️⃣ Very important: `+=` depends on the type

```python
# list
a = [1, 2]
a += [3]   # IN-PLACE

# tuple
b = (1, 2)
b += (3,)  # NEW tuple
```

Same syntax, different behavior.

---

# 6️⃣ So… does `object.func()` normally change in-place?
### ❌ No. There is **NO general rule**.
You must know:
1. The **type**
2. The **specific method**

However, there is a **strong convention** in Python:
> If a method **mutates in-place**, it usually returns `None`.

That's a design choice to prevent bugs like:

```python
nums = nums.sort()  # WRONG → nums becomes None
```

---
# 7️⃣ How to think about this safely (best practice)
### Rule of thumb:
- If you need the result → assume **new object**
- If method returns `None` → it mutated in-place

### Safe patterns
```python
nums = sorted(nums)   # safe
nums.sort()           # safe
```

---

# 8️⃣ Interview-level summary (say this)

> "In Python, mutability depends on the object type.  
> Lists, dicts, and sets have methods that mutate in-place and usually return `None`.  
> Immutable types like strings and tuples always return new objects."

That answer is **clean, correct, and senior-level**.

# Note


# Reference