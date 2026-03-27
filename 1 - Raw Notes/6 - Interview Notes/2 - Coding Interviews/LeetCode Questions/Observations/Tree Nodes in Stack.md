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

# 2. Tree Nodes in Stack

# Note


# Reference

