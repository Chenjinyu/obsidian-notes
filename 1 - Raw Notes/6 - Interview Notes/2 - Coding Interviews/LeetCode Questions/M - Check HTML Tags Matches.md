---
sr-due: 2026-05-30
sr-interval: 3
sr-ease: 2.5
---
Creation Date: 2026-03-15
Course:
Tags: [[../../../../3 - Zettelkasten/A - Templates/LeetCode Template]] [[Stack]] [[../Coding/Regress Expression|Regress Expression]]

#review/15d 
# Reviews Knowledges Points
- regex 
- stack
```text
03/29/2026
r'<(/?\w+)[^>]*>',  # (/?\w+), i use it to get the tag name
<div class="div">
     ~~~~~~~~~~~ excluded by [^>]* 
     
`r` means the raw string in python. it tells python do not treat backslashes \ as escape characters, etc.
so `r'\n'` means two characters: \ and n.


`[^>]*` means: match any character except `>`, zero or more times.
So given:
<div class="div">
The regex `<(/?\w+)[^>]*>` matches like this:
```

| Part      | Matches                                       |
| --------- | --------------------------------------------- |
| `<`       | `<`                                           |
| `(/?\w+)` | `div` — captured in group 1                   |
| `[^>]*`   | `class="div"` — consumed but **not captured** |
| `>`       | `>`                                           |
|           |                                               |

```
`[^>]*` greedily eats everything between the tag name and the closing `>`, including spaces, quotes, attribute names and values — it just throws them away.
```

# Review Dates
- 03/20/2026
- 03/29/2026

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
	# using regex, * means zero or more characters that are not `>`
	# <div class="foo">
	#      ^^^^^^^^^^^ matched by [^>]*, not include >,but any others.
    tag_pattern = re.compile(r'<(/?\w+)[^>]*>') # r'<(?P<tag>/?\w+)[^>]*>' to name the group as tag.
    stack = []
    for matches in tag_pattern.finditer(html):
        tag = matches.group(1) # matches.group('tag') 
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
