Date: 2026-02-26
Course: https://www.w3schools.com/dsa/dsa_algo_bubblesort.php
Tags: [[W3Schools]] [[Arrary]] [[Sort]]

# Content
Bubble Sort is an algorithm that sorts an array from the lowest value to the highest value.

```python
from typing import List

def bubble_sort_example(nums: List) -> List:
	"""
	Time Complexity: O(n^2), Space Complexity: O(1)
	Works, but not efficient.
	The solution is not standard bubble sort, closer to selection/insertion sort style
	"""
	for idx in range(len(nums)):
		cur_idx = idx
		while cur_idx < len(nums) - 1:
			if nums[cur_idx] > nums[cur_idx + 1]:
				nums[cur_idx], nums[cur_idx + 1] = nums[cur_idx + 1], nums[cur_idx]
			cur_idx += 1
	return nums
				
```

### Efficient(Optimized) Bubble Sort Example
```python
from typing import List
"""
Standard Bubble Sort
- Largest bubbles to end
- Shrinks each time
"""
def bubble_sort_efficient(nums: List) -> List:
	"""
	Best case O(n), worse case O(n ^ 2), space: O(1)
	"""
	n = len(nums)
	
	for idx in range(n):
		swapped = False # optimization: detect if array is already sorted
		
		# Shrinking the range
		for j_idx in range(0, n - idx - 1):
			if nums[j_idx] > nums[j_idx + 1]:
				nums[j_idx], nums[j_idx + 1] = nums[j_idx + 1], nums[j_idx]
				swapped = True
		
		# such like, the nums already are sorted, then, 
		# in the inner loop, it's not able to set swapped = True
		if swapped: # already sorted, exit early.
			break
			
	return nums
```

#### Steps for example:

##### Pass 1 (i=0): scan 0 → 3, largest bubbles to end

```
[4, 3, 1, 2]
 j=0: 4 > 3 → swap  →  [3, 4, 1, 2]
 j=1: 4 > 1 → swap  →  [3, 1, 4, 2]
 j=2: 4 > 2 → swap  →  [3, 1, 2, 4]  ✅ 4 is locked at end
```
##### Pass 2 (i=1): scan 0 → 2, ignore last 1
```
[3, 1, 2, 4]
 j=0: 3 > 1 → swap  →  [1, 3, 2, 4]
 j=1: 3 > 2 → swap  →  [1, 2, 3, 4]  ✅ 3 is locked
```

##### Pass 3 (i=2): scan 0 → 1, ignore last 2
```
[1, 2, 3, 4]
 j=0: 1 > 2 → no swap
 swapped = False → EARLY EXIT ✅
```

#### Why the inner loop shrinks each pass

````python
for j in range(n - 1 - i):
```
```
i=0 → range(3) → j checks: 0,1,2   (full scan)
i=1 → range(2) → j checks: 0,1     (skip last 1)
i=2 → range(1) → j checks: 0       (skip last 2)
```

Each pass you already know the last `i` elements are in their final position, so no need to check them again.

---

### Full picture
```
Start:  [4, 3, 1, 2]
Pass 1: [3, 1, 2, 4]  ← 4 locked
Pass 2: [1, 2, 3, 4]  ← 3 locked
Pass 3: early exit    ← already sorted
Result: [1, 2, 3, 4]  ✅
````
# Note


# Reference

