Date: 2026-03-04
Course:
Tags: 

# Content

## Hash Set vs Hash Map

| Hash Map        | Hash Set               |                           |
| --------------- | ---------------------- | ------------------------- |
| **Stores**      | Key-value pairs        | Keys only (no values)     |
| **Purpose**     | Look up a value by key | Check if something exists |
| **Python type** | `dict`                 | `set`                     |
| **Duplicates**  | No duplicate keys      | No duplicate elements     |
| **Null/None**   | ✅                      | ✅                         |
### Yes — Python's `set` IS a Hash Set
Under the hood, `set` is implemented as a hash table where only keys exist — there are no associated values. Same hashing mechanism, same O(1) average operations.

```python
# Hash Map — dict
d = {"a": 1, "b": 2}
d["a"]          # get the VALUE → 1

# Hash Set — set
s = {"a", "b"}
"a" in s        # just check existence → True, no value
```

### Time Complexity (both are the same)

|Operation|Average|Worst|
|---|---|---|
|**Insert**|O(1)|O(n)|
|**Delete**|O(1)|O(n)|
|**Search**|O(1)|O(n)|
|**Iteration**|O(n)|O(n)|

### What Hash Set is Good At
```python
# 1. Deduplication
nums = [1, 2, 2, 3, 3, 3]
unique = set(nums)          # {1, 2, 3}

# 2. O(1) membership check  (vs O(n) for list)
seen = set()
seen.add("a")
"a" in seen                 # ✅ O(1)
"a" in ["a", "b", "c"]     # ❌ O(n)

# 3. Set operations
a = {1, 2, 3}
b = {2, 3, 4}
a & b   # intersection → {2, 3}
a | b   # union        → {1, 2, 3, 4}
a - b   # difference   → {1}
```

---
### Choosing Between Them
- Need to **store and retrieve a value** by key → `dict` (Hash Map)
- Need to **check existence** or **eliminate duplicates** → `set` (Hash Set)
A simple way to think about it: a `set` is just a `dict` where you threw away the values.

# Note


# Reference

