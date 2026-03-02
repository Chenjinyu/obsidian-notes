Date: 2026-03-01
Course:
Tags: 

# Tim Sort

## **How it works:**

```
1. Split array into small chunks called "runs" (usually size 32)
2. Sort each run using Insertion Sort (fast for small arrays)
3. Merge the sorted runs together using Merge Sort
```

## Why this is smart:

- Insertion Sort is fast for **small** arrays
- Merge Sort is fast for **combining** sorted chunks
- Tim Sort gets the best of both worlds

### Complexity
Time Complexity:
- Best: O(n)
- Average: O(n log n)
- Worse: O(n ^ 2)
Space Complexity:
- O(n)

## Example
```python

RUN = 4  # chunk size (in real Tim Sort this is 32)

def insertion_sort(nums, left, right):
    for i in range(left + 1, right + 1):
        key = nums[i]
        j = i - 1
        # shift elements right until correct position found
        while j >= left and nums[j] > key:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = key

def merge(nums, left, mid, right):
    left_part = nums[left:mid + 1]   # copy left half
    right_part = nums[mid + 1:right + 1]  # copy right half

    i = j = 0
    k = left

    # merge two halves back into nums
    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            nums[k] = left_part[i]
            i += 1
        else:
            nums[k] = right_part[j]
            j += 1
        k += 1

    # append remaining elements
    while i < len(left_part):
        nums[k] = left_part[i]
        i += 1
        k += 1
    while j < len(right_part):
        nums[k] = right_part[j]
        j += 1
        k += 1

def tim_sort(nums):
    n = len(nums)

    # Step 1: sort each small run using insertion sort
    for start in range(0, n, RUN):
        end = min(start + RUN - 1, n - 1)
        insertion_sort(nums, start, end)

    # Step 2: merge runs together, doubling size each time
    size = RUN
    while size < n:
        for left in range(0, n, size * 2):
            mid = min(left + size - 1, n - 1)
            right = min(left + size * 2 - 1, n - 1)
            if mid < right:
                merge(nums, left, mid, right)
        size *= 2  # double the merge size each pass

    return nums

# Test
nums = [38, 27, 43, 3, 9, 82, 10, 1]
print(tim_sort(nums))  # [1, 3, 9, 10, 27, 38, 43, 82]
```

**Visualized:**
```
Original:  [38, 27, 43, 3,  9, 82, 10,  1]

Step 1 — insertion sort each run of size 4:
Run 1:     [27, 38, 43, 3] → [3, 27, 38, 43]  (oops, 3 belongs here after sort)
           Actually: [38,27,43,3] → [3,27,38,43] ✅
Run 2:     [9, 82, 10, 1]  → [1, 9, 10, 82]  ✅

Step 2 — merge sorted runs:
Merge:     [3,27,38,43] + [1,9,10,82] → [1,3,9,10,27,38,43,82] ✅
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

