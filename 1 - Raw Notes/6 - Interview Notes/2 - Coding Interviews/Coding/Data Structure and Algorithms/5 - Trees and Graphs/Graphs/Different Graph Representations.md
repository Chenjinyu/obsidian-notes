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

# the output: graph = [[1], [2], [0, 3], []], this is the exactally the adjanceny list graph
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
![400](assets/Graphs/file-20260402233434731.png)
## 2. Adjacency list
![200](assets/Different%20Graph%20Representations/file-20260404021943176.png)

the same graph can be represented by the adjacency list graph: 
```python
nodes = ['a', 'b', 'c', 'd', 'e', 'f'] 
#         0    1    2    3    4    5
adjancency_list = [[1], [2], [0, 3], []] # node's index

# OR 
adjancency_list_2 = {
    'a': ['b', 'c'],
    'b': ['d'],
    'c': ['e'],
    'd': [],
    'e': ['b'],
    'f': ['d']
}

are the adjacency list, adjancency_list uses index to present the node
# **The key insight:** the adjacency list only cares about **relationships between vertices** (who connects to who). The actual data/value sitting at each vertex is a separate concern — so it lives in a separate structure.
```

```python 
def dfs(graph, nodes, start):
	"""
	the nodes are the nodes list to present the node's info, eg value.
	since adjancency_list use the node value as the key and items in list, the traversal should use second one
	"""
    stack = [start]
    visited = set([start])

    while stack:
        node = stack.pop()
        print(nodes[node])  # ← use index to look up actual value
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

dfs(adj, nodes, 0)  # prints 'a', 'c', 'e', 'b', 'd'
```

```python
def dfs(graph, start):
	"""
	the traversal for adjancency_list
	"""
    stack = [start]
    visited = set([start])
    
    while stack:
        node = stack.pop() 
        print(node)  # process node
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
```

### 2.2 Adjacency List looks like
In the adjacency list representation, a graph is represented as an array of linked list. The index of the array represents a vertex and each element in its linked list represents the  vertices that form an edge with the vertex. 
the linked list just a list, 
#### 2.2.1. An undirected graphs and its adjacency list
![300](assets/Different%20Graph%20Representations/file-20260404025018005.png)


## 3. Adjacency Matrix

```python
adjacency_matrix = [
	[1,1,0],
	[1,1,0],
	[0,0,1]
]
```

# Note




# Reference

