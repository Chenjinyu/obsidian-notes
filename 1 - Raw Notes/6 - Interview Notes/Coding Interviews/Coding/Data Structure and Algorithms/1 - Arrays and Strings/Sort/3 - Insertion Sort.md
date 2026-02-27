Date: 2026-02-26
Course: https://www.w3schools.com/dsa/dsa_algo_insertionsort.php
Tags: [[W3Schools]] [[Arrary Sort]]

# Content

The Insertion Sort algorithm uses one part of the array to hold the sorted values, and the other part of the array to hold values that are not sorted yet.

```python
from typing import List

def insert_sort(nums: List) -> List:
	n = len(nums)
	
	for i in range(1, n):
		
		for j in range(i, -1, -1):
			if nums[j] > nums[j + 1]:
				nums[j], nums[j + 1] = nums[j + 1], nums[j]
	return nums
	
```

# Note


# Reference

