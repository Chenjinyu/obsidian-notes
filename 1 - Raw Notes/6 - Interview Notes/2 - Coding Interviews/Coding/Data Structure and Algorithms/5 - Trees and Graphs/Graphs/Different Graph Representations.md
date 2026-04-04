---
sr-due: <% tp.date.now("YYYY-MM-DD") %>
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-04-04
Course:
Tags: 

# Content

## 1. Array of edges
2D array: `edges = [[0, 1], [1, 2], [2, 0], [2, 3]]`
![200](assets/Different%20Graph%20Representations/file-20260404021943176.png)
the edges present the between `edges[i][0]` and `edges[i][1]` has a edge/arrow
means 0 -> 1, 1 ->2, 2 -> 0, and 2 -> 3
BUT it does represent the neighbors of any given node, Before starting the traversal, we need to pre-process the input so that we can easily find all neighbors.
There should use <span style="color:red">hashmap.</span>

```python
# example code for building graph from any array of edges
from collections import defaultdict
edges = [[0, 1], [1, 2], [2, 0], [2, 3]]
def build_graph(edges):
    graph = defaultdict(list)
    for x, y in edges:
        graph[x].append(y)
        # graph[y].append(x)
        # uncomment the above line if the graph is undirected
    
    return graph

# the output: graph = [[1], [2], [0, 3], []]
# the index is the node index in nodes list
```
for example 
```python
nodes = ['a', 'b', 'c', 'd', 'e', 'f'] 
#         0    1    2    3    4    5
```
and basically, when the node includes integer value, it will use index instead of char.
or if the node includes char, integer, string, set, etc. which are unique and immutable value, then can represent as the key, then the graph will look like:
```python
adjancency_list = {
    'a': ['b', 'c'],
    'b': ['d'],
    'c': ['e'],
    'd': [],
    'e': ['b'],
    'f': ['d']
}
```

## 2. Adjacency list
![200](assets/Different%20Graph%20Representations/file-20260404021943176.png)

the same graph can be represented by the adjacency list graph: 
```python
graph = [[1], [2], [0, 3], []]
```






# Note




# Reference

