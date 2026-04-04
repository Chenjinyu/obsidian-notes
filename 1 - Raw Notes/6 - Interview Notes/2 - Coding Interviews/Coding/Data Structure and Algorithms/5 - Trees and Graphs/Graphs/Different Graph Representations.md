---
sr-due: 2026-04-05
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-04-04
Course:
Tags: [[Graphs]]

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

### 2.2 Adjacency List Graph Representation(画像)
In the adjacency list representation, a graph is represented as an array of linked list. The index of the array represents a vertex and each element in its linked list represents the  vertices that form an edge with the vertex. 
The "linked list" because conceptually each neighbor list can grow dynamically — but <span style="color: orange">the **idea** is the same whether you use a linked list or a dynamic array.</span>
#### 2.2.1. An undirected graph and its adjacency list
![300](assets/Different%20Graph%20Representations/file-20260404025018005.png)

#### 2.2.2. An directed and weighted graph and its adjacency list
![300](assets/Different%20Graph%20Representations/file-20260404025410768.png)
## 3. Adjacency Matrix
In the adjacency matrix representation, a graph is represented in the form of a two-dimensional array. The size of the array is **V x V**, where V is the set of vertices.
```python
adjacency_matrix = [
	[1,1,0],
	[1,1,0],
	[0,0,1]
]
```
### 3.1. Adjacency Matrix Graph Representation(画像)
#### 3.1.1. An undirected graph an the adjacency matrix
![300](assets/Different%20Graph%20Representations/file-20260404025557884.png)
#### 3.1.2. An directed and weighted graph an the adjacency matrix
![300](assets/Different%20Graph%20Representations/file-20260404025648961.png)
NOTE: the adjacency matrix does not have to be symmetric, since the weighted

#### 3.2. Adjacency Matrix Graph Traversal
OPTION 1: Use adjacency matrix directly un DFS
just change how you find neighbors - instead of `graph[mode]`, you can scan the row:
```python
def dfs_matrix(matrix, start):
    n = len(matrix)
    stack = [start]
    visited = set([start])

    while stack:
        node = stack.pop() # the node is the row's index.
        print(node)
		
		# the neighbor is the index of row[n]
        for neighbor in range(n): # scan the entire row, the neighbor is the index of row[n]
            if matrix[node][neighbor] == 1 and neighbor not in visited:
                visited.add(neighbor) # the neighbor is the index of row[n], which is the node, there is asking: have we visited this node/vertex before?, 
                stack.append(neighbor)
                
matrix = [
    [0, 1, 1, 0], # a
    [0, 0, 1, 1], # b 
    [0, 1, 0, 1], # c 
    [0, 1, 1, 1], # d
]
dfs_matrix(matrix, 0) # start from vertex a 
dfs_matrix(matrix, 2) # start from vertex c


when pop 0(index of row), it will visit the neighbor which index 1(b) and index 2(c).
when pop 2 (append b and c, so c will be pop first), the neighbor which index 1(b) has been visited.

below is the walk through

initial: stack = [0], visited = {0}
pop 0 → scan row [0, 1, 1, 0]
    neighbor=0 → matrix[0][0]=0 → skip
    neighbor=1 → matrix[0][1]=1 → visited={0,1}, stack=[1]
    neighbor=2 → matrix[0][2]=1 → visited={0,1,2}, stack=[1,2]
    neighbor=3 → matrix[0][3]=0 → skip

pop 2 → scan row [0, 1, 0, 1]
    neighbor=0 → matrix[2][0]=0 → skip
    neighbor=1 → matrix[2][1]=1 → already in visited → skip
    neighbor=2 → matrix[2][2]=0 → skip
    neighbor=3 → matrix[2][3]=1 → visited={0,1,2,3}, stack=[1,3]

pop 3 → scan row [0, 1, 1, 1]
    neighbor=1 → already visited → skip
    neighbor=2 → already visited → skip
    neighbor=3 → matrix[3][3]=1 → already visited → skip

pop 1 → scan row [0, 0, 1, 1]
    neighbor=2 → already visited → skip
    neighbor=3 → already visited → skip

```
**The short answer:** for LeetCode, if the input is already an adjacency matrix, just traverse it directly — converting first is unnecessary overhead unless you have a strong reason.
OPTION 2: Convert to adjacency list first, then use original DFS
```python
matrix = [
    [0, 1, 1, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
]

n = len(matrix) # the len of rows, not matter if its symmetric or not.
adj = [[] for _ in range(n)]
for u in range(n):
    for v in range(n):
        if matrix[u][v] == 1:
            adj[u].append(v)

dfs(adj, 0)  # your original dfs works now
```

# Note




# Reference

