Date: 2026-02-26
Course: https://www.w3schools.com/dsa/dsa_algo_selectionsort.php
Tags: [[W3Schools]] [[Arrary]] [[Sort]]

# Content

The Selection Sort algorithm finds the lowest value in an array and moves it to the front of the array.
The algorithm looks through the array again and again, moving the next lowest values to the front, until the array is sorted.

```python
from typing import List

def selection_sort_example(nums: List) -> List:
	"""
	Time Complexity: O(n²). 
	Space Complexity: O(1)
	"""
	for idx in range(len(nums)):
		min_val_idx = idx
		j_idx = idx + 1
		while j_idx < len(nums):
		    # find the min_val_idx in inner loop, swap with inner idx
			if nums[min_val_idx] > nums[j_idx]: # only j_idx less than min_val_idx, can assign j_idx to min_val_idx
				min_val_dix = j_idx
			j_idx += 1
		
		nums[idx], nums[min_val_dix] = nums[min_val_idx], nums[idx]
		
	return nums
```

### How selection sort works conceptually
```
[4, 3, 1, 2]

Pass 1: find min in [4,3,1,2] → min=1 at idx=2, swap with idx=0 → [1, 3, 4, 2]
Pass 2: find min in [3,4,2]   → min=2 at idx=3, swap with idx=1 → [1, 2, 4, 3]
Pass 3: find min in [4,3]     → min=3 at idx=3, swap with idx=2 → [1, 2, 3, 4]
Pass 4: one element left, done ✅
```
# Note


# Reference

