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
- Left pointer shrinks the window when sum >= k (remove elements)
```python
def countSubarrays(nums, k):
    left = 0
    current_sum = 0
    count = 0
    for right in range(len(nums)):
        # Expand window: add right element
        current_sum += nums[right]
        # Shrink window: remove left elements while sum >= k
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
        if product < k:
            ans += 1
        right += 1
    right = left + 1
```

# Note


# Reference

