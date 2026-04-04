---
sr-due: <% tp.date.now("YYYY-MM-DD") %>
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-04-02
Course:
Tags: [[Graphs]] [[DFS]] [[BFS]] [[Stack]] [[Queues]] [[Recursive]]

# Content

![](assets/Depth%20and%20Breath%20First%20Traversal/file-20260402234412648.png)

## Depth First Traversal: using Stack
it will pick up any node to start, and choose a direction to move on until there is no node in that direction, then it choose other random direction until cannot move on
![](assets/Depth%20and%20Breath%20First%20Traversal/file-20260402234532979.png)

#### 1. DFS - using Stack
```python
# depth first traversal pattern
# One important note: graphs need a `visited` set, trees do not.
# A tree is acyclic by definition, but a graph can have cycles — without `visited` you'd loop forever.
def dfs(graph, start):
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

#### 2. DFS - using Recursive
NOTE: <span style="color:red">Recursive DFS is standard and clean though, since the call stack naturally mirrors the depth-first nature of the traversal.</span>
```python
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(node)
    print(node)  # process node
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

> Also note that `visited.add()` happens **on insertion**, not on processing. If you add on processing instead, the same node can get pushed onto the stack/queue multiple times before it's visited, which wastes work or causes bugs in dense graphs.

## Breadth First Traversal: Using queue
it will pick up any node to start, and explore any possible nodes around it. 
![](assets/Depth%20and%20Breath%20First%20Traversal/file-20260402234709702.png)

#### 1. BFS - using Queue
```python
# breath first traversal pattern
# One important note: graphs need a `visited` set, trees do not.
# A tree is acyclic by definition, but a graph can have cycles — without `visited` you'd loop forever.
def bfs(graph, start):

    queue = deque([start])
    visited = set([start])
    
    while queue:
        node = queue.popleft()
        print(node)  # process node
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```
#### 2. BFS - using Recursive
NOTE: <span style="color:red">**BFS is naturally iterative** — forcing it into recursion is unnatural because the recursion just mimics the `while queue` loop. In practice, nobody writes recursive BFS.</span>
```python
def bfs(graph, queue=None, visited=None):
    if queue is None:
        queue = deque([start])
        visited = set([start])
    
    if not queue:
        return
    
    node = queue.popleft()
    print(node)  # process node
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)
            queue.append(neighbor)
    
    bfs(graph, queue, visited)  # recurse on remaining queue
```
> Also note that `visited.add()` happens **on insertion**, not on processing. If you add on processing instead, the same node can get pushed onto the stack/queue multiple times before it's visited, which wastes work or causes bugs in dense graphs.
# Note


# Reference

