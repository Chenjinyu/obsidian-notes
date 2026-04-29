---
sr-due: 2026-04-28
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-02-24
Course: https://www.w3schools.com/dsa/dsa_theory_graphs.php
Tags: [[DSA]] [[Shortest Path]]  [[Heaps]] [[Graphs]]
#review/daily #review/3d 
# Content

To solve the shortest path problem means to check the edges inside the Graph 
until we find a path where we can move from one vertex to another using the lowest possible combined weight along the edges

The sum of weights along the edges that make up a path is called a path cost or a path weight

Algorithms that find the shortest paths, like [Dijkstra's algorithm](https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php) or [the Bellman-Ford algorithm](https://www.w3schools.com/dsa/dsa_algo_graphs_bellmanford.php), find the shortest paths from one start vertex to all other vertices(顶点的复数).

To begin with, the algorithms set the distance from the start vertex to all vertices to be infinitely long. And as the algorithms run, edges between the vertices are checked over and over, and shorter paths might be found many times until the shortest paths are found at the end.

Every time an edge is checked and it leads to a shorter distance to a vertex being found and updated, it is called a **relaxation**, or **relaxing** an edge.

## Dijkstra
### Dijkstra's algorithm is often considered to be the most straightforward algorithm for solving the shortest path problem.
- is used for resolving single-source shortest path for directed or undirected paths, <span style="color:red">(Single-source means that one vertex is chosen to be the start, and the algorithm finds the shortest path from that started vertex to all other vertices)</span>
- does not work for graph with negative edges/weights
- it needs to know which vertex is the source.
- It needs a way to mark vertices as visited
- It needs an overview of the current shortest distance to each vertex as it works its way through the graph, 
- and updating these distances when a shorter distance is found.


Dijkstra's Algorithm on undirected graphs
![400](assets/Shortest%20Path%20Algorithms%20-%20Dijkstra%20and%20Bellman-Ford/file-20260404185631636.png)
Dijkstra's Algorithm on directed graphs
![400](assets/Shortest%20Path%20Algorithms%20-%20Dijkstra%20and%20Bellman-Ford/file-20260404185758661.png)

#### **Undirected** — add both directions:
```python
graph = {
    'a': [('b', 4), ('c', 5)],
    'b': [('a', 4), ('c', 5)],  # ← reverse edges added
    'c': [('a', 5), ('b', 5)],
}
```
#### **Directed** — add only one direction:
```python
graph = {
    'a': [('b', 4), ('c', 5)],
    'b': [('c', 5)],             # ← no reverse edge back to 'a'
    'c': [],
}
```
The Dijkstra function itself stays **identical** — it just follows whatever neighbors are in `graph[node]`.
#### **The same principle applies to all graph traversal algorithms:**

|Algorithm|Directed|Undirected|
|---|---|---|
|DFS|same code|same code|
|BFS|same code|same code|
|Dijkstra|same code|same code|

The graph representation absorbs the directed/undirected distinction — the traversal logic never needs to know.

## Code Example

### Time Complexity: O((V+E) log V)
the sum of the number of Vertex + the number of edges and then times log Vertex


Both example 1 and example 2 work correctly. <br/>
Example 1's visited approach is slightly cleaner to read <br/>
the example 1 uses the path to store all visited paths to the path list<br/>
the example 2 uses the dictionary prev_dict to store prev_dict[neighbor] = node, and after while loop, iterative all nodes to get the path into list<br/>
Overall: correct solutions, just trade off being extra space cost of carrying path in heap versus reconstructing with prev dict.
### Simple Example 1 - I prefer this solution
```python

import heapq
from typing import List

graphs = {
	"A": [("B", 4), ("C", 5)],
	"B": [("A", 4), ("C", 5), ("D", 3)],
	"C": [("A", 5), ("B", 5), ("F", 3)],
	"D": [("B", 3), ("E", 8)],
	"F": [("C", 3), ("E", 2), ("G", 1)],
	"G": []
}
# TO find the closest paths
def dijkstra_simple_example(graph, start, end) -> List:
	# is a list, but it will push to heapq and order it with min order queue
	# current_time, current_city, and the path
	pq = [(0, start, [start])]
	# assign inf to all vertices
	shortest_cost = {city: float("inf") for city in graph}
	shortest_cost[start] = 0
	visted = set()
	
	while pq:
		# heappop costs O(log V) to reorder the heap, this happens at most V times(once per vertex), then total under while is V * log V
		cur_time, cur_city, path = heapq.heappop(pq) 
		
		if cur_city == end:
			return path # <- here is the return when find the end.
		if cur_city in visted: # skip if we already found a better path to this node.
			continue
		
		visted.add(cur_city)
		
		for neighbor, cost_time in graph[cur_city]: # E total across all vertices
			new_time = cur_time + cost_time
			if new_time < shortest_cost[neighbor]:
				shortest_cost[neighbor] = new_time # relaxing neighbor vertex with new vaule
				# everytime push the smaller value to heapq, 
				# since all vertices are assign postive inf, so all vertices will be pushed to heapq, and vist them once.
				heapq.heappush(pq, (new_time, neighbor, path + [neighbor])) # log V per push to reorder the heap
	
	return [] # ← end not reachable

```

### Simple Example 2: solution from Claude
```python
import heapq

def dijkstra(graph, start, end):
    # min heap: (cost, node)
    heap = [(0, start)]
    # track shortest distance to each node
    dist = {start: 0}
    # track the path: which node did we come from
    prev = {start: None}

    while heap:
        cost, node = heapq.heappop(heap)
        # early exit — found shortest path to end
        if node == end:
            break
        # skip if we already found a better path to this node
        if cost > dist[node]:
            continue
        for neighbor, weight in graph[node]:
            new_cost = cost + weight
            if neighbor not in dist or new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                prev[neighbor] = node
                heapq.heappush(heap, (new_cost, neighbor))

    # reconstruct path by walking back through prev
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()

    return dist[end], path
    
# adjacency list: graph[u] = [(v, weight), ...]
graph = {
    'a': [('b', 1), ('c', 4)],
    'b': [('c', 2), ('d', 6)],
    'c': [('d', 3)],
    'd': []
}

cost, path = dijkstra(graph, 'a', 'd')
print(cost)   # 6
print(path)   # ['a', 'b', 'c', 'd']
```
### NOTE: The Term of Relaxing
Since the original value is inf, then we can relax it with lower value, the processing we call it as relaxing.

## Bellman-Ford
- it loops through all edges V-1 times
- can start at any vertex
### Time Complexity: O(V+E)
the number of Vertex + the number of edges
### Simple Example 
```python

graphs = {
    "A": [("B", 4), ("C", 5)],
    "B": [("A", 4), ("C", 5), ("D", -3)],  # negative edge here
    "C": [("A", 5), ("B", 5), ("F", 3)],
    "D": [("B", 2), ("E", 8)],
    "E": [],
    "F": [("C", 3), ("E", 2)]
}

def bellman_ford(graph, start, end):
    # graph edges as list of (from, to, cost)
    edges = []
    for node, neighbors in graph.items():
        for neighbor, cost in neighbors:
            edges.append((node, neighbor, cost))

    # Step 1: assign inf to all vertices
    shortest_cost = {city: float("inf") for city in graph}
    shortest_cost[start] = 0
    predecessor = {city: None for city in graph}

    # Step 2: relax all edges V-1 times
    for i in range(len(graph) - 1): # brute force every round
        for from_node, to_node, cost in edges:
	        # when the from_node has not been reached yet, the shortest_cost[from_node] is inf
	        # until reach out the start, which has cost is 0
	        # in bellman-ford algorithm, blindly relaxes all edges every round regardless of order.
            new_cost = shortest_cost[from_node] + cost 
            if new_cost < shortest_cost[to_node]:
                shortest_cost[to_node] = new_cost        # relaxation
                predecessor[to_node] = from_node         # track the path, use to_node, so that can get the from_node from the predeerror to_node keys

    # Step 3: rebuild path using predecessor
    path = []
    cur = end
    while cur is not None: # the None assigned by predecessor = {city: None for city in graph}, so that the while loop can be stopped
        path.append(cur)
        cur = predecessor[cur]
    path.reverse()

    return path, shortest_cost[end]


path, cost = bellman_ford(graphs, "A", "E")
print(f"Path: {path}")   # Path: ['A', 'B', 'D', 'E']
print(f"Cost: {cost}")   # Cost: 9

# explanation: 
predecessor = { "A": None,   ← start node, no one came before it
                "B": "A",
                "D": "B",
                "E": "D" }

Reconstruction: E → D → B → A → None (stop)
Reversed:       A → B → D → E  ✅
```

## Why V-1 times?
In the worst case, the shortest path visits every vertex once, meaning it has at most `V-1` edges. Each round of relaxation is guaranteed to "lock in" at least one more vertex correctly.
```
Round 1:  A gets finalized  (distance 0)
Round 2:  B gets finalized  (A → B = 4)
Round 3:  D gets finalized  (A → B → D = 1)
Round 4:  E gets finalized  (A → B → D → E = 9)
```

## Bellman-Ford doesn't naturally fit a heap/queue
because its strategy is fundamentally different — it just **loops through all edges V-1 times**. No priority ordering needed.
However, there is a queue-based optimization called **SPFA (Shortest Path Faster Algorithm)** — it's essentially Bellman-Ford but with a queue to only process vertices whose cost actually changed, instead of blindly relaxing all edges every round.

## SPFA (Shortest Path Faster Algorithm)

### Time Complexity: O(V+E)
SPFA is often faster than Bellman-Ford in practice, but its worst case is the same O(V×E).

```python
from collections import deque

def spfa(graph, start, end):
    shortest_cost = {city: float("inf") for city in graph}
    shortest_cost[start] = 0
    predecessor = {city: None for city in graph}

    queue = deque([start])
    in_queue = set([start])  # avoid duplicates in queue

    while queue:
        cur = queue.popleft()  # regular queue (FIFO)
        in_queue.remove(cur)

        for neighbor, cost in graph[cur]:
            new_cost = shortest_cost[cur] + cost
            if new_cost < shortest_cost[neighbor]:  # relaxation
                shortest_cost[neighbor] = new_cost
                predecessor[neighbor] = cur

                if neighbor not in in_queue:  # only enqueue if not already waiting
                    queue.append(neighbor)
                    in_queue.add(neighbor)

    # rebuild path
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = predecessor[cur]
    path.reverse()

    return path, shortest_cost[end]
```

### The Core Difference in Strategy
```
Bellman-Ford:  relax ALL edges, every round, V-1 times
               → wasteful, processes edges that haven't changed

SPFA:          only re-process a vertex if its cost just improved
               → skip the wasted work using a queue
```
Think of it this way — if vertex D's cost didn't change, there's no point re-relaxing D's neighbors. SPFA uses the queue to track only the "active" vertices worth exploring.

SPFA is often faster than Bellman-Ford in practice, but its worst case is the same O(V×E). Dijkstra with a heap is still the fastest when there are no negative edges.
# Note


# Reference

