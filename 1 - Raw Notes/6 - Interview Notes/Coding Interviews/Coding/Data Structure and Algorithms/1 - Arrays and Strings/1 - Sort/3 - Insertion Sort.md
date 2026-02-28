Date: 2026-02-26
Course: https://www.w3schools.com/dsa/dsa_algo_insertionsort.php
Tags: [[W3Schools]] [[Arrary]] [[Sort]]

# Content

The Insertion Sort algorithm uses one part of the array to hold the sorted values, and the other part of the array to hold values that are not sorted yet.

```python
from typing import List

def insertion_sort(nums: List) -> List:
	n = len(nums)
	
	for i in range(1, n):
		
		for j in range(i, 0, -1): # does not incldue 0, so 1 - 1 = 0, not out of index
			if nums[j] < nums[j - 1]:
				nums[j], nums[j - 1] = nums[j - 1], nums[j]
			else:
				break # no need to continue, coz the sub-list[O: j-1] already sorted
	return nums
	
```

### Explain why else: break is a smart optimization
```
i=3: insert 2 into [1, 3, 4]
j=3: 2 < 4 → swap  →  [1, 3, 2, 4]
j=2: 2 < 3 → swap  →  [1, 2, 3, 4]
j=1: 2 < 1 → False → BREAK ✅  no need to check further
```
# Note


# Reference

