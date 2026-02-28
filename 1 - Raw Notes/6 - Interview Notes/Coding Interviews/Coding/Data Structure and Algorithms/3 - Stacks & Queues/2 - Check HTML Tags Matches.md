Date: 2026-02-27
Course:
Tags: [[LeetCode]]

# Content
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


# Note


# Reference

