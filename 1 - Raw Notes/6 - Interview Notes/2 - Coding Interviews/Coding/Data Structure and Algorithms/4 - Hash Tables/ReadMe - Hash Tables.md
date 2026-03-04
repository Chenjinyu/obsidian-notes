Date: 2026-03-03
Course: https://www.w3schools.com/dsa/dsa_theory_hashtables.php
Tags: [[DSA]]

# Hash Tables — Interview Study Notes

## Overview

A **hash table** (called `dict` in Python) maps **keys to values** using a **hash function**. It is one of the most commonly tested data structures in interviews because of its O(1) average-case lookup.

---

## Q1: How does a hash table work internally?

1. You provide a **key** (e.g. `"name"`)
2. A **hash function** converts the key into an **integer index**
3. The value is stored in an **array (bucket)** at that index
4. On lookup, the same hash function recomputes the index → direct access

```
key "name"  →  hash("name")  →  index 4  →  buckets[4] = "Alice"
key "age"   →  hash("age")   →  index 7  →  buckets[7] = 30
```

---

## Q2: What are the time complexities?

### Average Case (what you say in most interviews)

|Operation|Time Complexity|Notes|
|---|---|---|
|Search (lookup by key)|O(1)|Hash function gives direct index|
|Insert|O(1) amortized|Occasional rehashing like list reallocation|
|Delete|O(1)|Hash to index, remove entry|
|Iteration|O(n)|Must visit all buckets|

### Worst Case (when collisions are bad)

|Operation|Time Complexity|Notes|
|---|---|---|
|Search|O(n)|All keys hash to same bucket|
|Insert|O(n)|Same reason|
|Delete|O(n)|Same reason|

> **Interview tip:** Always say **"O(1) average case"** — not just O(1). If the interviewer asks why it can degrade, explain **collisions**.

---

## Q3: What is a collision and how is it handled?

A **collision** happens when two different keys produce the **same hash index**.

```
hash("cat") → index 3
hash("act") → index 3   ← collision!
```

### Two main strategies:

**1. Chaining (most common)** Each bucket holds a **linked list** of all key-value pairs that hash to that index.

```
buckets[3] → [("cat", 1)] → [("act", 2)] → None
```

- Lookup: hash to bucket, then scan the list → O(1) average, O(n) worst
- Python's `dict` uses a variation of this approach

**2. Open Addressing** If a bucket is occupied, probe for the **next available slot**.

- Linear probing: check index+1, index+2, ...
- Quadratic probing: check index+1², index+2², ...
- Less memory overhead than chaining but more complex

---

## Q4: What is rehashing?

Similar to list reallocation — when the hash table gets too full, it:

1. Allocates a **larger array** (typically 2x)
2. **Re-hashes every existing key** into the new array
3. That single operation costs **O(n)**

The ratio of filled slots to total slots is called the **load factor**. Python's `dict` rehashes when load factor exceeds ~**0.67 (2/3)**.

```
Load factor = number of entries / number of buckets
```

- Low load factor → fewer collisions, more wasted memory
- High load factor → more collisions, better memory usage

Just like list `append`, insert is **O(1) amortized** because rehashing is rare and the cost spreads across many insertions.

---

## Q5: What makes a good hash function?

|Property|Why it matters|
|---|---|
|**Deterministic**|Same key must always produce same index|
|**Uniform distribution**|Spread keys evenly to minimize collisions|
|**Fast to compute**|Should be O(1) itself|
|**Avalanche effect**|Small key change → very different hash|

Python's built-in `hash()` handles this for standard types (str, int, tuple).

---

## Q6: What types can be used as keys?

In Python, only **hashable** (immutable) types can be dictionary keys.

|Type|Hashable?|Notes|
|---|---|---|
|`int`, `float`|✅ Yes|Immutable|
|`str`|✅ Yes|Immutable|
|`tuple`|✅ Yes|Only if all elements are hashable|
|`list`|❌ No|Mutable — hash would change if list changes|
|`dict`|❌ No|Mutable|
|`set`|❌ No|Mutable (use `frozenset` instead)|

> **Interview tip:** If asked "why can't a list be a dict key?" — say: "Lists are mutable. If the list changed after being used as a key, the hash would be different and you'd never find it again. Python enforces immutability to keep hashing reliable."

---

## Q7: Full Implementation — Hash Table from scratch

```python
class HashTable:
    def __init__(self, size=16):
        self._size = size
        self._buckets = [[] for _ in range(self._size)]  # chaining with lists
        self._count = 0

    def _hash(self, key):
        return hash(key) % self._size   # map to valid index

    def insert(self, key, val):
        index = self._hash(key)
        bucket = self._buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, val)  # update existing key
                return
        bucket.append((key, val))       # new key
        self._count += 1

    def search(self, key):
        index = self._hash(key)
        bucket = self._buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(f"Key '{key}' not found")

    def delete(self, key):
        index = self._hash(key)
        bucket = self._buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._count -= 1
                return
        raise KeyError(f"Key '{key}' not found")

    def __len__(self):
        return self._count

    def __contains__(self, key):
        index = self._hash(key)
        return any(k == key for k, v in self._buckets[index])
```

---

## Q8: Hash Table vs other data structures

|Operation|Hash Table (avg)|Sorted Array|Linked List|BST (balanced)|
|---|---|---|---|---|
|Search|O(1)|O(log n)|O(n)|O(log n)|
|Insert|O(1) amortized|O(n)|O(1) at head|O(log n)|
|Delete|O(1)|O(n)|O(n)|O(log n)|
|Ordered iteration|❌ No|✅ Yes|Depends|✅ Yes|

> Hash tables win on speed but **sacrifice ordering**. If you need sorted data, use a BST or sorted array instead.

---

## Q9: Python `dict` specifics worth knowing

- Python `dict` maintains **insertion order** since Python 3.7
- Average O(1) for get, set, delete via `[]` operator
- `key in dict` is O(1) — much faster than `key in list` which is O(n)
- `dict.get(key, default)` — safe lookup without raising `KeyError`

```python
d = {}
d["name"] = "Alice"     # insert  O(1)
d["name"]               # search  O(1)
del d["name"]           # delete  O(1)
"name" in d             # search  O(1)
d.get("age", 0)         # safe search with default
```

---

## Design Decision: When to use a hash table?

|Use case|Why hash table fits|
|---|---|
|Frequency counting|`counts[item] += 1` in O(1)|
|Fast lookup by key|No need to scan — direct index|
|Deduplication|`seen = set()` — set is a hash table without values|
|Caching / memoization|Store computed results by input key|
|Two Sum / pairing problems|Store complement in O(1) lookup|

---

## Interview Cheat Sheet

|Concept|One-liner|
|---|---|
|Hash table order|No guaranteed order (except Python 3.7+ dict preserves insertion order)|
|Search average|O(1)|
|Search worst case|O(n) — all keys collide|
|Insert|O(1) amortized — rehashing like list reallocation|
|Delete|O(1) average|
|Collision|Two keys hash to the same index|
|Chaining|Each bucket holds a linked list of colliding pairs|
|Load factor|filled slots / total buckets — triggers rehash when too high|
|Python rehash threshold|~0.67 load factor|
|Hashable types|Immutable only — str, int, tuple (no list, dict, set)|
|`key in dict`|O(1) — use dict/set over list for membership checks|
|`key in list`|O(n) — scans every element|



# Note


# Reference

