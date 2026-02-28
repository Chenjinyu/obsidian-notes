Date: 2026-02-26
Course: https://www.w3schools.com/dsa/dsa_algo_quicksort.php
Tags: [[W3Schools]] [[Arrary]] [[Sort]]

# Content

As the name suggests, Quicksort is one of the fastest sorting algorithms.

The Quicksort algorithm takes an array of values, chooses one of the values as the 'pivot' element, and moves the other values so that lower values are on the left of the pivot element, and higher values are on the right of it.

```python
from typing import List

def quick_sort(nums: List) -> List:
	n = len(n)
	if n <= 1: return nums
	mid = n // 2
	# the pivot can be any item in nums
	pivot = nums[mid]
	left = [x for x in nums if x < pivot]
	right = [x for x in nums if x > pivot]
	return quick_sort(left) + [pivot] + quick_sort(right)
```
# Note


# Reference

