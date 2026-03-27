---
sr-due: 2026-03-28
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-03-27
Course:
Tags: 

# Content
This is a universal principle for tree DFS traversal:

## **Path-local data vs Global aggregator**

When doing DFS on a tree, your data falls into exactly two categories:
- **Path-local data** — values that belong to the current root-to-node path, must be carried inside the stack entry (or recursive parameter). Each path is independent and must not bleed into sibling paths.
  Examples: current min, current max, current sum, current path list

- **Global aggregator** — a single value that collects the final answer across all paths, lives outside the stack, only written to, never fed back into traversal.
  Examples: max difference, max sum, count of valid paths
---
The rule:
```
if the data influences HOW you traverse → path-local, carry it in the stack
if the data just COLLECTS results       → global aggregator, keep it outside
```
---

The bug pattern to watch for — feeding the global aggregator back into the stack entry:

```python
# WRONG — global answer pollutes path-local data
next_val = max(path_local, global_answer)
stack.append((node, next_val))  # sibling paths now see each other's results

# CORRECT — keep them separate
global_answer = max(global_answer, path_local)  # aggregate only
stack.append((node, path_local))                # carry only path-local
```

This applies universally to any DFS problem — recursive or iterative.

# Note


# Reference

