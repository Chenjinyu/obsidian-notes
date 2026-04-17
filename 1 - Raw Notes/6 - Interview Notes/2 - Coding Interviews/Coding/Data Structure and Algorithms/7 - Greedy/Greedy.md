---
sr-due: <% tp.date.now("YYYY-MM-DD") %>
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-04-17
Course:
Tags: 

# Content

## Tabulation
is bottom up, fill to an array step by step form the start all the way to the final answer. 
If the order is clear, you can use the bottom up, 
for example: the climb stairs. 
Since we know the base cases, when stair == 1, it has 1 options
when the stair == 2, it has 2 options, 
1. from 0 jump to 1, and from 1 to 2, 
2. from 0 jump to 2 directly

```python
# one direction solution pattern
def climb_stairs(n):
	ways = []
	ways[1], ways[2] = 1, 2
	for i in range(3, n):
		ways[i] = ways[i - 1] + ways[i - 2]
	return ways[-1]
```

```python
# one direction solution pattern
def climb_stairs(n):
	# Call this solution as Constant Transition
	# becuase the problem only needs to know the accummuative answer, 
	# It's not necessary to store all answers in the list.
	prev_1, prev_2 = 1, 2
	for i in range(3, n):
		curr = prev_1 + prev_2
		prev_1 = prev_2
		prev_2 = curr
	return curr
```
## Memorization (Recursive)
The memorization is recursion with memory, 
is Top-Down when the order is unclear or hard to reason about, 
```python
# one direction solution pattern
def climb_stairs(n):
	memo = {}
	if n in memo: return memo[n]
	if n == 1: return 1
	if n == 2: return 2
	
	result = climb_stair(n - 1) + climb_stair(n - 2)
	# the result gets from the previous two status.
	# definitely, should be the n in the memo
	memo[n] = result 
	return result
```
# Note


# Reference

