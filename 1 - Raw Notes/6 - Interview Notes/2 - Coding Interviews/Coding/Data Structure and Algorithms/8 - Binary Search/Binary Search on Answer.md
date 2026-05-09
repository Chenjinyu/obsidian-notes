---
sr-due: 2026-05-10
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-05-09
Course:
Tags: 

# Content

“Binary Search on Answer” does **not** usually mean:
```python
find exact target in array
```
Instead, it means:
> search the space of possible answers  
> to find the optimal feasible one

Usually:
- smallest possible valid answer
- largest possible valid answer
    
For example in LeetCode 410:
You are NOT searching for an already-known answer.
You are asking:
```python
What is the smallest possible maximum subarray sum?
```
You test candidate answers like:
```python
15
18
20
```

and check:
```python
Can this answer work?
```

So the core idea is:
```python
Binary Search on Answer
=
Binary Search on Feasibility
```
You binary search over:
```python
candidate answers
```
not over indices.

You also correctly noticed another important thing:
It often becomes:
```python
find smallest valid answer
```
or:
```python
find largest valid answer
```
rather than exact matching.
That is why these problems often look like:
```python
FFFFTTTT
```
or:
```python
TTTTFFFF
```
instead of:
```python
find exact equality
```

For example:
## Smallest valid answer
- Koko minimum eating speed
- smallest divisor
- minimum ship capacity
- split array largest sum

Pattern:
```python
find first True
```

## Largest valid answer
Examples:
- maximum minimum distance
- maximize sweetness
- aggressive cows
Pattern:
```python
find last True
```

So your refined understanding is strong now:
> Binary Search on Answer means using binary search over the range of possible optimal answers, usually to find the smallest or largest feasible solution.

That is the correct mental model interviewers expect.

# Note


# Reference

