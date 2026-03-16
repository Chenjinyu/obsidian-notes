---
sr-due: 2026-03-18
sr-interval: 15
sr-ease: 2.5
---
Creation Date: 2026-03-15
Course:
Tags: [[../../../../3 - Zettelkasten/A - Templates/LeetCode]] [[Stack]]

# Problem



# Step 1 - Understand the problem (10 mins)
- What are the input and output
- What are the edge cases? create your own examples
- What constraints matter?

1. Allow duplicate?
2. Allow Negative numbers?
3. Allow Empty List

## Can you find out the exit condition? 
## What is the solution pattern? and why
# Step 2 - Try Brute Force First to help you understand the structure of the problems
```python

```

# Step 3 - Think about Optimization
```python
html = """
<html>
    <head>Test</head>
    <body>
        <p>test content</p>
        <ol>
            <li>Option 1</li>
            <li>Option 2</li>
            <li>Option 3</li>
        </ol>
    </body>
</html>
"""
import re
def is_valid_html(html: str) -> bool:
	# using regex
    tag_pattern = re.compile(r'<(/?\w+)[^>]*>')
    stack = []
    for matches in tag_pattern.finditer(html):
        tag = matches.group(1)
        if not tag.startswith('/'):
            # opening tag
            stack.append(tag)
        else:
            if not stack or stack.pop() != tag[1:]: # not stack to make sure stack.pop() has value
                return False
    return not stack # the stack should include nothing, if all tags are matached

print(is_valid_html(html))
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
