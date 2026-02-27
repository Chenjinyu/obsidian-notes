Date: 2026-02-27
Course:
Tags: [[Python]]

This is a **very good Python question**, and you’re right to be suspicious here.  
Let’s make this **systematic and precise**, not hand-wavy.

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
## 🔹 `list` (VERY IMPORTANT)

| Method              | In-place? | Return        |
| ------------------- | --------- | ------------- |
| `list.append(x)`    | ✅         | `None`        |
| `list.extend(iter)` | ✅         | `None`        |
| `list.insert(i, x)` | ✅         | `None`        |
| `list.remove(x)`    | ✅         | `None`        |
| `list.pop()`        | ✅         | element       |
| `list.clear()`      | ✅         | `None`        |
| `list.reverse()`    | ✅         | `None`        |
| `list.sort()`       | ✅         | `None`        |
| `+=`                | ✅         | modifies list |

❗ Key signal:
> **Most mutating list methods return `None`**

### Example
```python
nums = [3, 1, 2]
nums.sort()
# nums is now [1, 2, 3]
```

---
## 🔹 `dict`

|Method|In-place?|
|---|---|
|`dict.clear()`|✅|
|`dict.pop(k)`|✅|
|`dict.popitem()`|✅|
|`dict.update({...})`|✅|
|`dict.setdefault(k, v)`|✅|
|`del dict[k]`|✅|
### Example

```python
d = {"a": 1}
d.update({"b": 2})
```
---
## 🔹 `set`

|Method|In-place?|
|---|---|
|`set.add(x)`|✅|
|`set.remove(x)`|✅|
|`set.discard(x)`|✅|
|`set.pop()`|✅|
|`set.clear()`|✅|
|`set.update(...)`|✅|
|`set.intersection_update(...)`|✅|
|`set.difference_update(...)`|✅|

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

|Expression|In-place?|
|---|---|
|`sorted(nums)`|❌|
|`nums + [1]`|❌|
|`str.replace()`|❌|
|`str.lower()`|❌|
|`dict.copy()`|❌|
|`list.copy()`|❌|
|`set.union()`|❌|

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

That’s a design choice to prevent bugs like:

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

> “In Python, mutability depends on the object type.  
> Lists, dicts, and sets have methods that mutate in-place and usually return `None`.  
> Immutable types like strings and tuples always return new objects.”

That answer is **clean, correct, and senior-level**.

# Note


# Reference

