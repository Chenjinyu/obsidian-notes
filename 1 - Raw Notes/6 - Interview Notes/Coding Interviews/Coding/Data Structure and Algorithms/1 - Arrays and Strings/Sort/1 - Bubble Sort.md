Date: 2026-02-26
Course: https://www.w3schools.com/dsa/dsa_algo_bubblesort.php
Tags: [[W3Schools]] [[Arrary Sort]]

# Content
Bubble Sort is an algorithm that sorts an array from the lowest value to the highest value.

```python
from typing import List

def bubble_sort_example(nums: List) -> List:
	"""
	Time Complexity: O(n^2), Space Complexity: O(1)
	"""
	for idx in range(len(nums)):
		cur_idx = idx
		while cur_idx < len(nums) - 1:
			if nums[cur_idx] > nums[cur_idx + 1]:
				nums[cur_idx], nums[cur_idx + 1] = nums[cur_idx + 1], nums[cur_idx]
			cur_idx += 1
	return nums
				
```

# Note


# Reference

