---
sr-due: <% tp.date.now("YYYY-MM-DD") %>
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-03-15
Course:
Tags: 

#interview_review

# Content

`deque` can work as both — but for stack, a plain `list` is preferred.

**`deque` as a queue (recommended ✅)**
```python
queue = deque()
queue.append(1)     # enqueue to right
queue.popleft()     # dequeue from left  O(1)
```
Use `deque` for queue because `list.pop(0)` is O(n) but `deque.popleft()` is O(1).

---
**`deque` as a stack (works but not recommended)**
```python
stack = deque()
stack.append(1)     # push to right
stack.pop()         # pop from right  O(1)
```

This works, but plain `list` is simpler and equally efficient for stack:

```python
stack = []
stack.append(1)     # push
stack.pop()         # pop  O(1)
```

---
**Summary:**

|Structure|Best tool|Why|
|---|---|---|
|Stack|`list`|`append`/`pop` both O(1), simpler|
|Queue|`deque`|`popleft()` is O(1) vs list's O(n)|
|Both ends|`deque`|`appendleft`/`popleft`/`append`/`pop` all O(1)|

---

The reason `deque` exists is specifically to fix the O(n) weakness of `list.pop(0)`. For stack operations (only touching the right end), `list` is already O(1) so there is no reason to switch.

# Note


# Reference

