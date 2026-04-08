---
sr-due: <% tp.date.now("YYYY-MM-DD") %>
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-04-07
Course:
Tags: 

# Content

99% of the time, a graph will not have a tree structure. But even then, the same logic still applies. 
Imagine whatever node you start from as a "root". Then, the neighbors of the root represent the next level, and the neighbors of those nodes represent the level after that.

BFS on a graph always visits nodes according to their distance from the **starting point**. This is the key idea behind BFS on graphs - **<span style="color:orange">every time you visit a node, you must have reached it in the minimum steps possible from wherever you started your BFS.</span>

> The above statement was always the case on binary trees, even if you did a DFS, because there is only one possible path to any node from the root. In a graph, there could be many paths from a given starting point to any other node. Using BFS will ensure that out of all possible paths, you take the shortest one.

# Note


# Reference

