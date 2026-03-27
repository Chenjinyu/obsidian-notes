---
sr-due: 2026-03-28
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-03-26
Course:
Tags: [[../../Coding/Data Structure and Algorithms/5 - Trees and Graphs/Binary Trees - DFS]] [[../../Coding/Data Structure and Algorithms/4 - Stacks & Queues/Stacks|Stacks]]

# 1. How to know the two nodes are in the same ancestor lineage?

The core question is: **in DFS, how do you know two nodes share the same ancestor lineage?**

The answer is — DFS naturally tracks ancestry through the **call stack** (recursive) or **explicit path** (iterative). The nodes currently "active" in the stack at any moment are exactly the ancestors of the current node.

Three common approaches:
**1. Carry the path explicitly (what we did earlier)**
```python
stack = [(node, path)]
```

Every node carries its full ancestor chain. You can compare paths directly.

**2. Recursive call stack — ancestors are implicitly "above" you**
```python
def dfs(node):
    # everything above this frame IS the ancestor chain
    dfs(node.left)
    dfs(node.right)
```

When you're inside `dfs(node)`, all parent calls are frozen on the call stack — they are the ancestors.

**3. Visited set / parent map — reconstruct ancestry later**
```python
parent = {}
# after DFS, walk up via parent pointers to find common ancestors
```

**BFS does NOT naturally preserve ancestry** — nodes at the same level have no relationship to each other in the queue, so ancestry tracking requires extra bookkeeping like a parent map.
So ironically, **DFS is the better tool when ancestry matters**, and BFS is better when level/distance matters.

# 2. To understand the steps each node in the stack

the tree
```text
          3
        /   \
       5     1
      / \   /  \
     6  2  0    8
       / \
      7   4 
```

Let's use the same stack-based DFS (append right first, then left — so left is popped first):
```
Initial: stack = [3]
```
**Step 1:** pop `3` → append right `1`, append left `5`
```
stack = [1, 5]
```
**Step 2:** pop `5` → append right `2`, append left `6`
```
stack = [1, 2, 6]
```
**Step 3:** pop `6` → leaf, nothing appended
```
stack = [1, 2]
```
**Step 4:** pop `2` → append right `4`, append left `7`
```
stack = [1, 4, 7]
```
**Step 5:** pop `7` → leaf, nothing appended
```
stack = [1, 4]
```
**Step 6:** pop `4` → leaf, nothing appended
```
stack = [1]
```
**Step 7:** pop `1` → append right `8`, append left `0`
```
stack = [8, 0]
```
**Step 8:** pop `0` → leaf, nothing appended
```
stack = [8]
```
**Step 9:** pop `8` → leaf, nothing appended
```
stack = []
```
**Visit order:** `3 → 5 → 6 → 2 → 7 → 4 → 1 → 0 → 8`
This is pre-order DFS (root → left → right). The trick is always **append right before left** so that left gets popped first.

# Note


# Reference

