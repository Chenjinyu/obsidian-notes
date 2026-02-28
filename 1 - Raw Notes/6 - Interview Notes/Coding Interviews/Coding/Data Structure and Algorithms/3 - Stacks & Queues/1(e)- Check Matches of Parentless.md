Date: 2026-02-27
Course:
Tags: 

# Content

```python
## Check if the string is parentless
parentless = "[{}{([])}]{}{}"

def is_valid_parentless(s: str) -> bool:
	if len(s) <= 1:
		return False
	parentless_dict = {"(": ")", "{": "}", "[": "]"}
	stack = []
	for i in range(len(s)):
		if s[i] in parentless_dict.keys():
			stack.append(s[i])
		elif not stack or s[i] != parentless_dict[stack.pop()]:
			return False
	return len(stack) == 0 # eg. "(("
```

```python
from collections import deque



```
# Note


# Reference

