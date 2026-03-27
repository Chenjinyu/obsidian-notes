---
sr-due: 2026-03-28
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-03-27
Course:
Tags: [[../../../Coding/Data Structure and Algorithms/5 - Trees and Graphs/Binary Trees - DFS|Binary Trees - DFS]]

# Binary Tree DFS Traversal — Mental Checklist

## Core Idea

When doing DFS on a binary tree, whether iterative (stack) or recursive, every node visit follows the same 3-step thinking pattern.

---

## The 3-Step Checklist

### Step 1 — Handle current node's situation

What is the state of this node right now? Deal with edge cases before anything else.

- Is it `null`?
- Is it a leaf?
- Does it meet some special condition?

### Step 2 — Record / exit condition

Given the current node's state and the data carried from ancestors, should I record an answer?

- Update the global aggregator here
- This is where the actual problem logic lives

### Step 3 — Pass forward to children

What path-local data does each child need? Update based on current node, then push/recurse.

- Only path-local data goes into the stack entry or recursive parameter
- The global aggregator stays outside — never feed it back into the traversal

---

## Two Categories of Data

||Path-local data|Global aggregator|
|---|---|---|
|**What**|Values specific to current root-to-node path|The final answer collected across all paths|
|**Lives in**|Stack entry / recursive parameter|Outside the loop|
|**Direction**|Flows downward to children|Only written to, never fed back in|
|**Examples**|curr_min, curr_max, curr_sum, path list|max_diff, max_sum, count|

---

## The Bug Pattern to Avoid

Feeding the global aggregator back into path-local data — this causes sibling paths to bleed into each other:

```python
# WRONG — right subtree sees left subtree's result
next_val = max(path_local, global_answer)
stack.append((node, next_val))

# CORRECT — keep them separate
global_answer = max(global_answer, path_local)
stack.append((node, path_local))
```

---

## Template

```python
stack = [(root, initial_path_local_data)]
global_answer = initial_value

while stack:
    node, path_local = stack.pop()

    # Step 1 — situation
    if not node: continue

    # Step 2 — record condition
    global_answer = max(global_answer, compute(node, path_local))

    # Step 3 — pass forward
    next_path_local = update(path_local, node.val)
    stack.append((node.left, next_path_local))
    stack.append((node.right, next_path_local))

return global_answer
```

---

## Maps to Recursive Thinking Too

- **Step 1** → base case / guard clause
- **Step 2** → when to record the answer
- **Step 3** → what goes into the recursive call parameters

The checklist is the same regardless of whether you write iterative or recursive DFS.



# Note


# Reference

