Date: 2026-02-09
Course:
Tags: 

# Content
## Why the sliding window is O(n)
Below of the time complexity is O(n), because the left does not reset for each right, it only moves forward overall. (**[**amortized analysis**](https://en.wikipedia.org/wiki/Amortized_analysis)**)
```python
# Time Complexity: O(n)
function fn(arr):
    left = 0
    for (int right = 0; right < arr.length; right++):
        Do some logic to "add" element at arr[right] to window

        while WINDOW_IS_INVALID:
            Do some logic to "remove" element at arr[left] from window
            left++

        Do some logic to update the answer
```
![](assets/Sliding%20Window/file-20260209005455197.png)
## A true sliding window needs to include:
- Both pointers only move forward, never reset.
- Each element is processed a constant number of time.
- Right pointer expands the window (add elements)
- Left pointer shrinks(收缩) the window when sum >= k (remove elements)
```python
def countSubarrays(nums, k):
    left = 0
    current_sum = 0
    count = 0
    # do you see the right and left alwasy move to right.
    for right in range(len(nums)):
        # Expand window: add right element
        current_sum += nums[right]
        # Shrink window: remove left elements while sum >= k
        # the point of the left needs to move one more step to right.
        # find out the point and then correct the current result before moving forward to right.
        while current_sum >= k and left <= right:
            current_sum -= nums[left]
            left += 1
        # Count all valid subarrays ending at right
        # [left...right], [left+1...right], ..., [right...right]
        count += (right - left + 1)
    
    return count
```
#### Check below script, which has O(n^2), because:
- the right is reset for each left, which is loop back to left + 1. (the above example, the right visits each element exactly once in the for loop, and left visits each element at most once in the while loop)
- re-checking many elements multi-times.
```python
# the code has logic error,just for reference.
for left in range(len(nums)):
    while right < len(nums) + 1:
	    arr_sum = sum(nums[left: right])
        if arr_sum < k:
            ans += 1
        right += 1
    right = left + 1
```

## Leetcode example
reference link: https://leetcode.com/problems/subarray-product-less-than-k/
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

**Constraints:**

- `1 <= nums.length <= 3 * 104`
- `1 <= nums[i] <= 1000`
- `0 <= k <= 106`
```

solution:
```python
class Solution:
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        """ Since the length of subarray is the mount of combination subarraies which product less than K  """
        if len(nums) == 0: return 0
        if k <= 1: return 0
        left = ans = 0
        product = 1
        for right in range(len(nums)):
            product *= nums[right]
            while product >= k:
                product //= nums[left]
                left += 1
            ans += right - left + 1
        return ans
```

Best practice here is provide the test cases including edge cases:
```python
#below is an example of count sub-array less than k
# Test cases (if required)
def test():
    # Basic
    assert countSubarrays([1, 2, 3], 7) == 6, "Basic case failed"
    # Edge cases
    assert countSubarrays([], 5) == 0, "Empty array failed"
    assert countSubarrays([1], 5) == 1, "Single element failed"
    assert countSubarrays([10], 5) == 0, "Single large element failed"
    
    # All valid/invalid
    assert countSubarrays([1, 1, 1], 10) == 6, "All valid failed"
    assert countSubarrays([10, 20], 5) == 0, "All invalid failed"
    
    print("All tests passed!")
```

### Maximum Average Subarray I - Easy



# Note


# Reference

