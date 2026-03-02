Date: 2026-03-02
Course:
Tags: 

# Heap Sort

## **How it works:**
```
1. Build a "max heap" from the array
   → max heap means: every parent is larger than its children
2. Repeatedly extract the largest element (root) and place it at the end
```

## First understand a **heap** structure:
```
Array:  [38, 27, 43, 3, 9]

As a tree:
        38          ← index 0 (root, always largest in max heap)
       /   \
     27     43      ← index 1, 2
    /  \
   3    9           ← index 3, 4

Parent of index i  → (i-1) // 2
Left child of i   → 2*i + 1
Right child of i  → 2*i + 2


```

### Complexity
Time Complexity:
- Best: O(n log n)
- Average: O(n log n)
- Worse: O(n log n)
Space Complexity:
- O(1)

## Example
```python

def heapify(nums, n, i):
    """
    Ensure subtree rooted at index i satisfies max heap property.
    n = current heap size
    """
    largest = i          # assume root is largest
    left = 2 * i + 1     # left child index
    right = 2 * i + 2    # right child index

    # check if left child is larger than root
    if left < n and nums[left] > nums[largest]:
        largest = left

    # check if right child is larger than current largest
    if right < n and nums[right] > nums[largest]:
        largest = right

    # if root is not largest, swap and continue heapifying
    if largest != i:
        nums[i], nums[largest] = nums[largest], nums[i]
        heapify(nums, n, largest)  # fix the affected subtree

def heap_sort(nums):
    n = len(nums)

    # Step 1: build max heap (start from last non-leaf node)
    for i in range(n // 2 - 1, -1, -1):
        heapify(nums, n, i)

    # Step 2: extract largest element one by one
    for i in range(n - 1, 0, -1):
        nums[0], nums[i] = nums[i], nums[0]  # move root (largest) to end
        heapify(nums, i, 0)                  # fix heap for remaining elements

    return nums

# Test
nums = [38, 27, 43, 3, 9, 82, 10]
print(heap_sort(nums))  # [3, 9, 10, 27, 38, 43, 82]
```

**Visualized:**
```
Original: [38, 27, 43, 3, 9, 82, 10]

Step 1 — build max heap:
        82
       /   \
     27     43
    /  \   /  \
   3    9 38  10
→ array: [82, 27, 43, 3, 9, 38, 10]

Step 2 — extract max repeatedly:
swap 82 with last → [10, 27, 43, 3, 9, 38, | 82]
heapify           → [43, 27, 38, 3, 9, 10, | 82]
swap 43 with last → [10, 27, 38, 3, 9, | 43, 82]
heapify           → [38, 27, 10, 3, 9, | 43, 82]
... continues until sorted ...
final: [3, 9, 10, 27, 38, 43, 82] ✅

```

**Key differences between Tim Sort and Heap Sort:**

| | Tim Sort | Heap Sort |
|--|---------|-----------|
| Strategy | divide and merge | build heap, extract max |
| Space | O(n) extra space | O(1) in-place |
| Stable | ✅ equal elements keep order | ❌ may reorder equal elements |
| Best case | O(n) nearly sorted data | O(n log n) always |
| Real world | Python's default sort | priority queues, scheduling |
| Key idea | combines insertion + merge sort | uses heap tree structure |
# Note


# Reference

