---
sr-due: 2026-04-10
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-04-02
Course:
Tags: [[Graphs]] [[DFS]] [[BFS]] [[Stack]] [[Queues]] [[Recursive]]

#review/daily 
# Content

![](assets/Depth%20and%20Breath%20First%20Traversal/file-20260402234412648.png)

## Depth First Traversal: using Stack
it will pick up any node to start, and choose a direction to move on until there is no node in that direction, then it choose other random direction until cannot move on
![](assets/Depth%20and%20Breath%20First%20Traversal/file-20260402234532979.png)

#### 0. How to use Set
```python
visited = set([start])  # wraps start in a list first, then makes a set
# or
visited = set()         # empty set, then add start separately
visited = {start}       # set literal, most Pythonic
```

`set(start)` without the list would be wrong if `start` is a string
```python
start = "abc"
set(start)    # → {'a', 'b', 'c'}  ← iterates characters! YES, the abc is iterable, same like [start] list is iterable
set([start])  # → {'abc'}          ← correct, treats whole string as one element
{start}       # → {'abc'}          ← correct

# when start = "a", then,
set(start), set([start]) are the same
# BUT, if the graph node, which is integer
# you cannot use
set(start), it will raise TypeError, because integer cannot iterate.
```


#### 1. DFS - using Stack
```python
# depth first traversal pattern
# One important note: graphs need a `visited` set, trees do not.
# A tree is acyclic by definition, but a graph can have cycles — without `visited` you'd loop forever.
def dfs(graph, start):
    stack = [start]
    visited = set([start]) # same to visited = {start}
    
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
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(start)
    print(start)  # process node
    
    for neighbor in graph[start]:
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
def bfs(graph, start, queue=None, visited=None):
    if queue is None:
        queue = deque([start]) # ← only use of start
        visited = set([start]) # ← only use of start
        
    # bool(deque([0])) # → True ← not empty 
    # bool(deque([])) # → False ← empty, "not queue" is True
    # the falsy / truthy based on deque size.
    if not queue: 
        return
    
    node = queue.popleft() # from here on, start is never referenced again
    print(node)  # process node
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)
            queue.append(neighbor)
    
    bfs(graph, start, queue, visited)  # recurse on remaining queue
```
> Also note that `visited.add()` happens **on insertion**, not on processing. If you add on processing instead, the same node can get pushed onto the stack/queue multiple times before it's visited, which wastes work or causes bugs in dense graphs.
# Note


# Reference

