Date: 2026-02-26
Course: https://www.w3schools.com/dsa/dsa_algo_selectionsort.php
Tags: [[W3Schools]] [[Arrary Sort]]

# Content

The Selection Sort algorithm finds the lowest value in an array and moves it to the front of the array.
The algorithm looks through the array again and again, moving the next lowest values to the front, until the array is sorted.

```python
from typing import List

def selection_sort_example(nums: List) -> List:
	
	for idx in range(len(nums)):
		min_val_idx = idx
		j_idx = idx + 1
		while j < len(nums) - 1:
			if nums[min_val_idx] <
```

# Note


# Reference

