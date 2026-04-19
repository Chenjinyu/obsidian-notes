---
sr-due: <% tp.date.now("YYYY-MM-DD", 3) %>
sr-interval: 1
sr-ease: 2.5
---

Creation Date: 2026-04-19
Course:
Tags: [[../../../../3 - Zettelkasten/A - Templates/LeetCode Template]]

#review/daily #review/3d 

# Reviews Knowledges Points

# Review dates

# Problem

The **median** is the middle value in an ordered integer list. If the size of the list is even, there is no middle value. So the median is the mean of the two middle values.
- For examples, if `arr = [2,3,4]`, the median is `3`.
- For examples, if `arr = [1,2,3,4]`, the median is `(2 + 3) / 2 = 2.5`.

You are given an integer array `nums` and an integer `k`. There is a sliding window of size `k` which is moving from the very left of the array to the very right. You can only see the `k` numbers in the window. Each time the sliding window moves right by one position.
Return _the median array for each window in the original array_. Answers within `10-5` of the actual value will be accepted.

**Example 1:**
**Input:** nums = [1,3,-1,-3,5,3,6,7], k = 3
**Output:** [1.00000,-1.00000,-1.00000,3.00000,5.00000,6.00000]
**Explanation:** 
Window position                Median
---------------                -----
[**1  3  -1**] -3  5  3  6  7        1
 1 [**3  -1  -3**] 5  3  6  7       -1
 1  3 [**-1  -3  5**] 3  6  7       -1
 1  3  -1 [**-3  5  3**] 6  7        3
 1  3  -1  -3 [**5  3  6**] 7        5
 1  3  -1  -3  5 [**3  6  7**]       6

**Example 2:**
**Input:** nums = [1,2,3,4,2,3,1,4,2], k = 3
**Output:** [2.00000,3.00000,3.00000,3.00000,2.00000,3.00000,2.00000]

**Constraints:**
- `1 <= k <= nums.length <= 105`
- `-231 <= nums[i] <= 231 - 1`

# Step 1 - Understand the problem (10 mins)
- What are the input and output
- What are the edge cases? create your own examples
- What constraints matter?

1. Allow duplicate?
2. Allow Negative numbers?
3. Allow Empty List

## How do you think about this problem?
## Can you find out the exit condition? 
## What is the solution pattern? and why

# Step 2 - Try Brute Force First to help you understand the structure of the problems
```python

```

# Step 3 - Think about Optimization
```python

```

# Step 4 - If stuck > 20 mins, Study the solution
1. Why does the algorithm work?
2. What pattern is this problem?
3. What problem type does it belong to?

# Step 5 - Re implement from scratch. 
```python

```

# Takeaways

# Reference
