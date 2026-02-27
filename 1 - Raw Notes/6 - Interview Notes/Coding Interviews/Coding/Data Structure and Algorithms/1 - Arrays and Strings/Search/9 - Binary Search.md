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
	n = len(nums)
	if n == 0:
		return False
	nums.sort() # in-place, O(n)
	mid = n // 2
	if nums[mid] == k:
		return True # then change idx mid to True
	if nums[mid] > k:
		# the idx will be changed after each split
		# so it cannot return correct idx.
		# but if want to return True or False
		# this solution is correct
		narrow_nums = nums[:mid] 
	else:
		narrow_nums = nums[mid + 1:]
	
	return binary_search(narrow_nums, k)
```


```python
def binary_search_is_better(nums, k) -> int:
	"""
	this one is better, 
	because, its not necessary to nums.sort() everytime
	"""
	nums.sort() # in-place, O(n)
	def search(nums):
		n = len(nums)
		if n == 0:
			return False
		mid = n // 2
		if nums[mid] == k:
			return True # then change idx mid to True
		if nums[mid] > k:
			return search(nums[:mid])
		else:
			return search(nums[mid + 1:])
		
	return search(nums)
```

### If want to return the matched Index, then using left and right to store the nums's index

and alos pass the left and right to recursive call
```python
def binary_search(nums, k) -> int:
    nums = sorted(nums)  # sort once before searching
    
    def search(left, right):
        if left > right:
            return -1          
        
        mid = (left + right) // 2
        
        if nums[mid] == k:
            return mid
        elif nums[mid] > k:
            return search(left, mid - 1)  
        else:
            return search(mid + 1, right)  
    
    return search(0, len(nums) - 1)
```
# Note


# Reference

