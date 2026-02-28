Date: 2026-02-28
Course:
Tags: 

# Content

## The best solution I can understand

```python
class Solution:
    def isValid(self, code: str) -> bool:
        
        # Code must start with '<' and end with '>'
        if code[0] != '<' or code[-1] != '>':
            return False

        i, n = 0, len(code)
        stack = []  # tracks opened tags that need to be closed

        while i < n:
            if code[i] == '<':
                # ---- CDATA Section: <![CDATA[...]]> ----
                if i != 0 and code[i: i + 9] == '<![CDATA[':
                    # CDATA must be inside an open tag
                    if not stack:
                        return False

                    # Search for the closing ']]>'
                    j = i + 9
                    while j + 3 < n and code[j: j + 3] != ']]>':
                        j += 1

                    # If closing ']]>' not found, invalid
                    if code[j: j + 3] != ']]>':
                        return False

                    # Skip past the closing ']]>'
                    i = j + 3

                # ---- Tag Section: <TAG> or </TAG> ----
                else:
                    start = i  # remember where the tag started
                    is_closing = False
                    i += 1

                    # Unexpected end of string
                    if i >= n:
                        return False

                    # Check if it's a closing tag </TAG>
                    if code[i] == '/':
                        is_closing = True
                        i += 1

                    # Unexpected end of string after '/'
                    if i >= n:
                        return False

                    # Extract tag name (must be uppercase letters only)
                    tag = ''
                    while i < n and code[i] != '>':
                        if not code[i].isupper():
                            return False  # tag contains non-uppercase character
                        tag += code[i]
                        i += 1

                    # Tag name must exist, be <= 9 chars, and have a closing '>'
                    if i >= n or len(tag) == 0 or len(tag) > 9:
                        return False

                    if is_closing:
                        # Closing tag must match the most recent open tag
                        if not stack or stack[-1] != tag:
                            return False
                        stack.pop()
                    else:
                        # Opening tag must be inside another open tag (except the first one)
                        if start != 0 and not stack:
                            return False
                        stack.append(tag)

                    i += 1  # skip past '>'

            # ---- Text Content (non-tag characters) ----
            else:
                # Text content must be inside an open tag
                if not stack:
                    return False

                # Skip ahead until the next '<'
                while i < n and code[i] != '<':
                    i += 1

        # All opened tags must be closed
        return not stack
```

![](assets/3(h)%20-%20Tag%20Valiator/file-20260228155944832.png)%20-%20Tag%20Valiator/file-20260228155944832.png)

## The solution with regex

```python
import re

class Solution:
    def __init__(self):
        self.stack = []
        self.contains_tag = False

    def is_valid_tag_name(self, s, ending):
        if ending:
            if self.stack and self.stack[-1] == s:
                self.stack.pop()
            else:
                return False
        else:
            self.contains_tag = True
            self.stack.append(s)
        return True

    def isValid(self, code):
        regex = r'<[A-Z]{0,9}>([^<]*(<((\/?[A-Z]{1,9}>)|(!\[CDATA\[(.*?)]]>)))?)*'
        if not re.fullmatch(regex, code):
            return False

        i = 0
        while i < len(code):
            ending = False
            if not self.stack and self.contains_tag:
                return False
            if code[i] == '<':
                if code[i + 1] == '!':
                    i = code.index(']]>', i + 1)
                    i += 1
                    continue
                if code[i + 1] == '/':
                    i += 1
                    ending = True
                close_index = code.index('>', i + 1)
                if close_index < 0 or not self.is_valid_tag_name(code[i+1:close_index], ending):
                    return False
                i = close_index
            i += 1

        return len(self.stack) == 0
```
# Note


# Reference

