Date: 2026-03-04
Course:
Tags: 

## What each one stores

|Hash Table | `dict`|`set`|`map`|
|---|---|---|---|
|Stores|**key → value** pairs|**keys only** (no values)|**key → value** pairs|
|Duplicates|❌ No duplicate keys|❌ No duplicates at all|❌ No duplicate keys|
|Ordering|Insertion order (Python 3.7+)|❌ Unordered|✅ **Sorted by key**|
|Underlying structure|Hash table|Hash table|**Balanced BST** (Red-Black tree)|
|Python type|`dict`|`set`|No built-in — use `sortedcontainers.SortedDict`|

> **Key insight:** In Python, there is no built-in `map` type like Java/C++ has. Python's `dict` is the hash table. Java has both `HashMap` (hash table) and `TreeMap` (sorted map / BST).

---

## Time complexities side by side

|Operation|`dict` (hash table)|`set`|`map` (BST-based)|
|---|---|---|---|
|Search|O(1) avg|O(1) avg|O(log n)|
|Insert|O(1) amortized|O(1) amortized|O(log n)|
|Delete|O(1) avg|O(1) avg|O(log n)|
|Iteration in order|❌ insertion order only|❌ no order|✅ always sorted|
|Min / Max|O(n)|O(n)|O(log n)|
|Range query|O(n)|O(n)|O(log n)|

---

## When to use which
### Use `dict` when:
- You need to **map a key to a value**
- Lookup speed matters most
- Order doesn't need to be sorted
```python
# word frequency count
freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1

# caching / memoization
cache = {}
cache[input] = result
```

### Use `set` when:
- You only care about **existence** of a value, not mapping to anything
- You need **deduplication**
- You need fast **membership checks**
- You need **set operations** (union, intersection, difference)
```python
# deduplication
unique = set(my_list)

# membership check — O(1) vs list's O(n)
seen = set()
if item in seen: ...

# set operations
a = {1, 2, 3}
b = {2, 3, 4}
a & b   # intersection → {2, 3}
a | b   # union        → {1, 2, 3, 4}
a - b   # difference   → {1}
```

### Use `map` (sorted dict / TreeMap) when:
- You need key → value AND **sorted key order**
- You need **range queries** ("find all keys between 10 and 50")
- You need **min/max key** efficiently
- You need **floor/ceiling** of a key ("nearest key ≤ x")
```python
# Python — use sortedcontainers
from sortedcontainers import SortedDict
m = SortedDict()
m[5] = "five"
m[2] = "two"
m[8] = "eight"
print(m)          # SortedDict({2: 'two', 5: 'five', 8: 'eight'})
m.peekitem(0)     # min key → (2, 'two')
m.irange(2, 6)    # range query → keys 2, 5
```

---
## The decision flowchart
```
Do you need to store key → value pairs?
├── YES
│    Do you need sorted order or range queries?
│    ├── YES → use Map (SortedDict / TreeMap)
│    └── NO  → use dict (hash table)
└── NO — you only need to track existence/membership
     └── use set
```

---
## Common interview patterns

|Problem type|Use|
|---|---|
|Count frequency of elements|`dict`|
|Check if element was seen before|`set`|
|Remove duplicates from a list|`set`|
|Two Sum (find complement fast)|`dict` — store `{value: index}`|
|Find all unique characters|`set`|
|Find nearest/floor/ceiling key|`map` (SortedDict)|
|Sliding window with sorted order|`map`|
|Range queries on keys|`map`|
|Graph adjacency list|`dict` of `set`|

---

## Interview Cheat Sheet

|Concept|One-liner|
|---|---|
|`dict` vs `set`|dict maps key→value, set stores keys only|
|`dict` vs `map`|dict is unordered O(1), map is sorted O(log n)|
|When to pick `set` over `dict`|When you don't need a value, just existence|
|When to pick `map` over `dict`|When you need sorted keys, range queries, or min/max|
|Python's built-in map equivalent|No built-in — use `sortedcontainers.SortedDict`|
|Underlying structure of `set`|Hash table (same as dict, just no values)|
|Underlying structure of `map`|Balanced BST (Red-Black tree in Java/C++)|
|`in` operator on set/dict|O(1)|
|`in` operator on list|O(n) — avoid for membership checks|

# Note


# Reference

