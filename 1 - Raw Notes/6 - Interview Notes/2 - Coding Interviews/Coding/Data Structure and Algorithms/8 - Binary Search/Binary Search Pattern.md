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

# Binary Search
Binary search is a search algorithm that runs in O(logn) in the worst case, where nn is the size of the search space


```python
def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            # do something
            return
        if arr[mid] > target:
            right = mid - 1
        else:
            left = mid + 1
    
    # target is not in arr, but left is at the insertion point
    return left
```

## Duplicate elements
If your input has duplicates, you can modify the binary search template to find either the first or the last position of a given element. If `target` appears multiple times, then the following template will find the left-most index:

### Left-Most Index

```python
def binary_search(arr, target):
    left = 0
    right = len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] >= target:
            right = mid
        else:
            left = mid + 1

    return left
```

### Right-Most Index
The following template will find the right-most **insertion point** (the index of the right-most element plus one):

```python
def binary_search(arr, target):
    left = 0
    right = len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] > target:
            right = mid
        else:
            left = mid + 1

    return left
```

### > Regarding both of the above templates, if the element you are searching for does not exist, then `left` will be at the index where the element should be inserted to maintain sorted order (just like in a normal binary search). Note that you can also use these templates on arrays without duplicate elements.


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

