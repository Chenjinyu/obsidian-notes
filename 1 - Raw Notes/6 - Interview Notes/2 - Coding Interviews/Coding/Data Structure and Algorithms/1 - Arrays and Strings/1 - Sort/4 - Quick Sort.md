Date: 2026-02-26
Course: https://www.w3schools.com/dsa/dsa_algo_quicksort.php
Tags: [[W3Schools]] [[Arrary]] [[Sort]]

#pattern_binary_search

# Content

As the name suggests, Quicksort is one of the fastest sorting algorithms.

The Quicksort algorithm takes an array of values, chooses one of the values as the 'pivot' element, and moves the other values so that lower values are on the left of the pivot element, and higher values are on the right of it.

### **Quick Sort** is fastest with other sort algorithms on average in practice despite O(n²) worst case

```python
from typing import List

def quick_sort(nums: List) -> List:
	# BEST.        Average    Worse.   Space
	# O(n log n) O(n log n). O(n²).  O(log n)
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

