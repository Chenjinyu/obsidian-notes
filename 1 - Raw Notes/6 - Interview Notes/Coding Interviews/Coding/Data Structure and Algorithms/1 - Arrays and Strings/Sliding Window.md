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

#### Check below script, which has O(n^2), because:
- the right is reset for each left. 
```python
# the code has logic error,just for reference.
for left in range(len(nums)):
    while right < len(nums) + 1:
        product *= nums[right]
        if product < k:
            ans += 1
        right += 1
    right = left + 1
```

# Note


# Reference

