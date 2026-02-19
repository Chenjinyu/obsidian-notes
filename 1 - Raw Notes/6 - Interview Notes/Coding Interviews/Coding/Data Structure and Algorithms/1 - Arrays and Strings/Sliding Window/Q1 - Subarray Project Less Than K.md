#### NOTE: python `/` and `//`.
```python
7 / 2 = 3.5
7 // 2 = 3

-7 / 2 = - 3.5
-7 // 2 = -4 (htting lower floor)
```

```text
Given an array of integers `nums` and an integer `k`, return _the number of contiguous subarrays where the product of all the elements in the subarray is strictly less than_ `k`.

**Example 1:**

**Input:** nums = [10,5,2,6], k = 100
**Output:** 8
**Explanation:** The 8 subarrays that have product less than 100 are:
[10], [5], [2], [6], [10, 5], [5, 2], [2, 6], [5, 2, 6]
Note that [10, 5, 2] is not included as the product of 100 is not strictly less than k.

**Example 2:**

**Input:** nums = [1,2,3], k = 0
**Output:** 0
```

### answer
```python
class Solution:
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        """ Since the length of subarray is the mount of combination subarraies which product less than K  """
        if len(nums) == 0 or k <= 1:
            return 0
        left = 0
        ans = 0
        product = 1
        for right in range(len(nums)):
            product *= nums[right]
            while product >= k:
                product //= nums[left]
                left += 1
                ans -= 1
            ans += right - left + 1 # because the right is keeping move to right, and it count the increment values. 
            
        return ans
```

### Takeaways
1. the right extends to the right always, and it cannot reset/backward, otherwise it's not the sliding window algorithm
2. when want to count using `right - left + 1`
	-> Answer: Almost always when counting subarrays/substrings.

### Pattern Recognition

| Problem Type                          | How to Count                               | Why                                                   |
| ------------------------------------- | ------------------------------------------ | ----------------------------------------------------- |
| **Count subarrays ending at `right`** | `right - left + 1`                         | Each position in `[left...right]` is a starting point |
| **Count total valid subarrays**       | `right - left + 1`                         | Same — accumulate as window expands                   |
| **Find longest subarray**             | `max_len = max(max_len, right - left + 1)` | Track max window size                                 |
| **Find if ANY valid subarray exists** | Just check if window is valid              | Boolean, no counting                                  |
