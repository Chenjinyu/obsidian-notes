Date: 2026-02-26
Course: https://www.w3schools.com/dsa/dsa_algo_binarysearch.php
Tags: [[W3Schools]] [[Arrary Sort]]

# Content

```
- The Binary Search algorithm searches through an array and returns the index of the value it searches for.
- Binary Search is much faster than Linear Search, but requires a sorted array to work.
- The Binary Search algorithm works by checking the value in the center of the array. If the target value is lower, the next value to check is in the center of the left half of the array. This way of searching means that the search area is always half of the previous search area, and 
- This is why the Binary Search algorithm is so fast.
```

```python
from typing import List

def binary_search(nums, k) -> int:
	"""
	Find out the idx if the value k in nums, 
	if does not find it, return -1
	"""
	n = len(n)
	sorted(nums) # in-place, O(n)
	mid = n // 2
	if nums[mid] > k:
		left = nums[0: mid]
	else:
		right = nums[mid: n]
			
	for idx in range(mid):
		if nums[idx] == k
			return idx
	
	return binary_search
```

# Note


# Reference

