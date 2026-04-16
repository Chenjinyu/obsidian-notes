---
sr-due: 2026-04-25
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-04-16
Course:
Tags: [[Binary Search]] 

## Reference LeetCode Problem
- [[../../../LeetCode Questions/M - 0658. Find K Closest Elements|M - 0658. Find K Closest Elements]]
# Content
## Binary Search Patterns

### 1️⃣ Classic — find exact target
```python
left, right = 0, len(arr) - 1

while left <= right:
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        left = mid + 1
    else:
        right = mid - 1

return -1
```
### 2️⃣ Find leftmost (first occurrence)
```python
left, right = 0, len(arr)  # note: right = len(arr)

while left < right:         # note: strict 
    mid = (left + right) // 2
    if arr[mid] < target:
        left = mid + 1
    else:
        right = mid         # don't do mid - 1

return left
```

### 3️⃣ Find rightmost (last occurrence)
```python
left, right = 0, len(arr)

while left < right:
    mid = (left + right) // 2
    if arr[mid] <= target:
        left = mid + 1      # note: <=
    else:
        right = mid

return left - 1
```

### 4️⃣ Binary search on answer (search space is a range, not array)
```python
left, right = min_possible, max_possible

while left < right:
    mid = (left + right) // 2
    if feasible(mid):       # some condition function
        right = mid
    else:
        left = mid + 1

return left
```

> Used when you're not searching an array but a **value range** — e.g. "minimum capacity", "minimum days", "kth smallest".

## Key signals to recognize binary search

|Signal|Example|
|---|---|
|Sorted array|`arr = [1, 3, 5, 7, 9]`|
|"Find minimum/maximum that satisfies X"|minimize max distance|
|Has `mid = (left + right) // 2`|always present|
|Search space halves each iteration|left or right moves to mid|
## Common mistakes

```python
# infinite loop when left + 1 == right
mid = (left + right) // 2  # always floors, so mid == left
right = mid                 # right never changes → infinite loop
# fix: ensure one branch always shrinks the space
```

```python
# overflow (not an issue in Python, but good habit)
mid = left + (right - left) // 2  # safer in Java/C++
```

# Note


# Reference

