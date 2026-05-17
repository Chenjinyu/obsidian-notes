---
sr-due: 2026-05-16
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-04-16
Course:
Tags: [[../../../../../../3 - Zettelkasten/B - Tags/Binary Search]] 

## Reference LeetCode Problem
- [[../../../LeetCode Questions/M - 0658. Find K Closest Elements|M - 0658. Find K Closest Elements]]

# Binary Search


## The MOST Important thing to understand is:
- Binary Search is NOT about "Finding Target"
- Binary Search is about finding a BOUNDARY.

### left-most = first valid position
### right-most = last valid position.


eg
```python
arr = [1,3,7,9,12,20]  
target = 9

# for left-most index pattern, we want to find the first elem >= target, find index.

# for right-most index pattern, we want to find the first elem which is larget than target. first elem > target. find index 4
```

Binary search is a search algorithm that runs in O(logn) in the worst case, where nn is the size of the search space

### Find out the match within closed interval. [left, right] both ends included.
```python
def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            # do something
            return
        if arr[mid] > target:
            right = mid - 1
        else:
            left = mid + 1
    
    # target is not in arr, but left is at the insertion point
    return left
```

## Duplicate elements
If your input has duplicates, you can modify the binary search template to find either the first or the last position of a given element. If `target` appears multiple times, then the following template will find the left-most index:

### Left-Most Index - when asking the minimum, so getting the left index as possible as it can.

#### Half-open interval, `[left, right)`, right is not included. But right = len(arr) is allowed, because its exclusive

the leftmost position where arr[i] >=target
that position might be:
- inside the array
- OR at the very end (insertion point)
Example:
```python
arr = [1,2,3,4]  
target = 10

# Answer should be:
4 # insert at the end
# So:  👉 you MUST allow `left` to reach `len(arr)`
# if using right = len(arr) - 1, you'd never return 4, you'd cap out at 3.

```

#### Why right = mid (not `mid - 1`)
Because `mid` might still be the answer
```python
if arr[mid] >= target:
    right = mid   # keep mid
   
# You’re shrinking: 
# [left, right) → [left, mid)
```

####  pattern for left most index, the only different with right most index is the >= target
```python
def binary_search(arr, target):
    left = 0
    right = len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] >= target: # here is the find the first elem whic >= target
            right = mid
        else:
            left = mid + 1

    return left
```

check [[../../../LeetCode Questions/E - 0035. Search Insert Position|E - 0035. Search Insert Position]], during the processing to find the left most index, also to check if the elem exists in nums.
below the pattern is able to find out the matched target index, also is able to return the position to insert by returning the left index.
```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums)
        while left < right:
            mid = (left + right) // 2

            if nums[mid]==target: return mid
            elif nums[mid] > target: right = mid
            else: left = mid + 1

        return left
```

### Right-Most Index - when asking maximum, so getting the right index as possible as it can.
The following template will find the right-most **insertion point** (the index of the right-most element plus one):
if the if condition in the while loop, why it cannot `>= target`, check [[../../../LeetCode Questions/E M - 2389. Longest Subsequence With Limited Sum|E M - 2389. Longest Subsequence With Limited Sum]]
```python
def binary_search(arr, target):
    left = 0
    right = len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] > target:
            right = mid
        else:
	        # why left is mid + 1, becuase here condition is: arr[mid] <= target. + 1 means the next elem may equals target. so, it incldues all.
            left = mid + 1 

    return left
```

### > Regarding both of the above templates, if the element you are searching for does not exist, then `left` will be at the index where the element should be inserted to maintain sorted order (just like in a normal binary search). Note that you can also use these templates on arrays without duplicate elements.


## Key signals to recognize binary search

|Signal|Example|
|---|---|
|Sorted array|`arr = [1, 3, 5, 7, 9]`|
|"Find minimum/maximum that satisfies X"|minimize max distance|
|Has `mid = (left + right) // 2`|always present|
|Search space halves each iteration|left or right moves to mid|
## Common mistakes

```python
# infinite loop when left + 1 == right
mid = (left + right) // 2  # always floors, so mid == left
right = mid                 # right never changes → infinite loop
# fix: ensure one branch always shrinks the space
```

```python
# overflow (not an issue in Python, but good habit)
mid = left + (right - left) // 2  # safer in Java/C++
```

# Note


# Reference

