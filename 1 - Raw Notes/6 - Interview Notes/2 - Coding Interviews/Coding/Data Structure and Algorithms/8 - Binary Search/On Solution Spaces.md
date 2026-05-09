---
sr-due: 2026-05-08
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-05-06
Course:
Tags: 

# Content

- [[../../../LeetCode Questions/M - 0875. Koko Eating Bananas|M - 0875. Koko Eating Bananas]]
- [[../../../LeetCode Questions/M - 1631. Path With Minimum Effort|M - 1631. Path With Minimum Effort]]
- [[../../../LeetCode Questions/M - 1870. Minimum Speed to Arrive on Time|M - 1870. Minimum Speed to Arrive on Time]]

All 3 examples we looked at in this article asked for a **<span style="color:red">minimum</span>**. In all solutions, we <span style="color:red">`return left`</span>.
If a problem is instead asking for a **maximum**, then `left` will not actually be the correct answer at the end. Instead, we should <span style="color:red">`return right`</span>.

# Why does `left` point to the answer when looking for a minimum, but `right` points to the answer when looking for a maximum?
## Explanation left-most is >=target, and right-most is >target

## LEFT-MOST
is to find FIRST position where a condition becomes TRUE
which not specfically:
```python
mid >= target
# it aslo can be
mid <= target # check the [[../../../LeetCode Questions/M - 1870. Minimum Speed to Arrive on Time|M - 1870. Minimum Speed to Arrive on Time]]
```

for left-most, it will get the first one which match the condition. 
```python
arr = [1,2,2,2,3]  
target = 2
arr[mid] >= target

# the boolean map: F T T T T
# the left-most get the first T index 1
```

## RIGHT-MOST
is to find the LAST position when the condition is TRUE
```python
arr = [1,2,2,2,3]  
target = 2
arr[mid] > target

# the boolean map: F F F F T
# the left-most get the first T index 1
```


# Note


# Reference

