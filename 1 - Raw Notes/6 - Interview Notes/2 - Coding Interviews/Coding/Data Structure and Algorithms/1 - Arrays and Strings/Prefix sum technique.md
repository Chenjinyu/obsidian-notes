---
sr-due: 2026-05-01
sr-interval: 1
sr-ease: 2.5
---
Date: 2026-03-04
Course:
Tags: 

#review/3d
# Content

Prefix sum is a technique that can be used on arrays (of numbers, usually). 
The idea is to create an array 
```
prefix` where `prefix[i]` is the sum of all elements up to the index `i` (inclusive). 
```
For example, given `nums = [5, 2, 1, 6, 3, 8]`, we would have `prefix = [5, 7, 8, 14, 17, 25]`.


![](assets/Prefix%20sum%20technique/file-20260305010804782.png)

## Example Problem
```text
[2090. K Radius Subarray Averages](https://leetcode.com/problems/k-radius-subarray-averages/)
You are given a **0-indexed** array `nums` of `n` integers, and an integer `k`.
The **k-radius average** for a subarray of `nums` **centered** at some index `i` with the **radius** `k` is the average of **all** elements in `nums` between the indices `i - k` and `i + k` (**inclusive**). 
If there are less than `k` elements before **or** after the index `i`, then the **k-radius average** is `-1`.
Build and return _an array_ `avgs` _of length_ `n` _where_ `avgs[i]` _is the **k-radius average** for the subarray centered at index_ `i`.
The **average** of `x` elements is the sum of the `x` elements divided by `x`, using **integer division**. The integer division truncates toward zero, which means losing its fractional part.
- For example, the average of four elements `2`, `3`, `1`, and `5` is `(2 + 3 + 1 + 5) / 4 = 11 / 4 = 2.75`, which truncates to `2`.
  
**Input:** nums = [7,4,3,9,1,8,5,2,6], k = 3
**Output:** [-1,-1,-1,5,4,4,-1,-1,-1]
**Explanation:**
- avg[0], avg[1], and avg[2] are -1 because there are less than k elements **before** each index.
- The sum of the subarray centered at index 3 with radius 3 is: 7 + 4 + 3 + 9 + 1 + 8 + 5 = 37.
  Using **integer division**, avg[3] = 37 / 7 = 5.
- For the subarray centered at index 4, avg[4] = (4 + 3 + 9 + 1 + 8 + 5 + 2) / 7 = 4.
- For the subarray centered at index 5, avg[5] = (3 + 9 + 1 + 8 + 5 + 2 + 6) / 7 = 4.
- avg[6], avg[7], and avg[8] are -1 because there are less than k elements **after** each index.
```

## and Solution
```python
from typing import List

def get_averages(nums: List[int], k: int) -> List[int]:
	n = len(nums)
	ans = [-1] * n
	
	if 2 * k + 1 > n: return ans
	
	prefix = [0] * (n + 1)
	for i in range(n):
		prefix[i+1] = prefix[i] + nums[i]
		
	for j in range(k, n - k):
		window_sum = prefix[j + k + 1] - prefix[j-k]
		ans[j] = window_sum // (2 * k + 1)
	return ans
```

## Takeaways
1. [-1] * n wouldn't update other items in the list, but the [[]] * n will update all items
2. you can add one item as the default value to the list, like prefix, to allow the for loop is able to get the 0 at the first step
3. use the term of `window` as window_sum
# Note


# Reference

