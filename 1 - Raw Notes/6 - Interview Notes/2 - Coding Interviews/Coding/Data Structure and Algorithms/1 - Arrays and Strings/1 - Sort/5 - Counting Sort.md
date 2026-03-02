Date: 2026-02-26
Course: https://www.w3schools.com/dsa/dsa_algo_countingsort.php
Tags: [[W3Schools]] [[Arrary]] [[Sort]]

# Content

The Counting Sort algorithm sorts an array by counting the number of times each value occurs.

### **How it works:**
1. Create a new array for counting how many there are of the different values.
2. Go through the array that needs to be sorted.
3. For each value, count it by increasing the counting array at the corresponding index.
4. After counting the values, go through the counting array to create the sorted array.
5. For each count in the counting array, create the correct number of elements, with values that correspond to the counting array index.

```python
from typing import List

def counting_sort(nums: List) -> List:
	"""
	
	"""
	max_val = max(nums) # O(n)
	# if max = 8, needs the count has idx = 8. which includes 9 items
	count = [0] * (max_val + 1) 
	for i in range(len(nums)):
		count[nums[i]] += 1
	output = []
	for idx_is_num_val, val_is_num_idx in enumerate(count):
		output.extend([val_is_num_idx] * idx_is_num_val) 
	return output
```
# Note


# Reference

