Date: 2026-02-24
Course:
Tags: [[DSA]] [[Shortest Path]] 

# Content

To solve the shortest path problem means to check the edges inside the Graph 
until we find a path where we can move from one vertex to another using the lowest possible combined weight along the edges

The sum of weights along the edges that make up a path is called a path cost or a path weight

Algorithms that find the shortest paths, like [Dijkstra's algorithm](https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php) or [the Bellman-Ford algorithm](https://www.w3schools.com/dsa/dsa_algo_graphs_bellmanford.php), find the shortest paths from one start vertex to all other vertices(顶点的复数).

To begin with, the algorithms set the distance from the start vertex to all vertices to be infinitely long. And as the algorithms run, edges between the vertices are checked over and over, and shorter paths might be found many times until the shortest paths are found at the end.

Every time an edge is checked and it leads to a shorter distance to a vertex being found and updated, it is called a **relaxation**, or **relaxing** an edge.

## Dijkstra
### Dijkstra's algorithm is often considered to be the most straightforward algorithm for sloving the shortest path problem.
- is used for resolving single-source shortest path for directed or undirected paths, (Single-source means that one vertex is chosen to be the start, and the algorithm finds the shortest path from that started vertex to all other vertices)
- does not work for graph with negative edges/weights
- it needs to know which vertex is the source.
- It needs a way to mark vertices as visited
- It needs an overview of the current shortest distance to each vertex as it works its way through the graph, 
- and updating these distances when a shorter distance is found.
### Time Complexity: O((V+E) log V)
### Simple Example 
```python

import heapq
from typing import List

graphs = {
	"A": [("B", 4), ("C", 5)],
	"B": [("A", 4), ("C", 5), ("D", 3)],
	"C": [("A", 5), ("B", 5), ("F", 3)],
	"D": [("B", 2), ("E", 8)],
	"F": [("C", 3), ("E", 2), ("G": 1)],
	"G": []
}
# TO find the cloest paths
def dijkstra_simple_example(graph, start, end) -> List:
	# is a list, but it will push to heapq and order it with min order queue
	# current_time, current_city, and the path
	pq = [(0, start, [start])]
	# assign inf to all vertices
	shortest_cost = {city: float("inf") for city in graphs}
	shortest_cost[start] = 0
	visted = set()
	
	while pq:
		cur_time, cur_city, path = heapq.heappop(pq)
		
		if cur_city == end:
			return path
		if cur_city in visted:
			continue
		
		visted.add(cur_city)
		
		for neighbor, cost_time in graphs[cur_city]:
			new_time = cur_time + cost_time
			if new_time < shortest_cost[neighbor]:
				shortest_cost[neighbor] = new_time # relaxing neighbor vertex with new vaule
				# everytime push the smaller value to heapq, 
				# since all vertices are assign postive inf, so all vertices will be pushed to heapq, and vist them once.
				heapq.heappush(pq, (new_time, neighbor, path + [neighbor]))

```
### NOTE: The Term of Relaxing
Since the original value is inf, then we can relax it with lower value, the processing we call it as relaxing.

## Bellman-Ford
- it loops through all edges V-1 times
- can start at any vertex
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
    for i in range(len(graph) - 1):
        for from_node, to_node, cost in edges:
            new_cost = shortest_cost[from_node] + cost
            if new_cost < shortest_cost[to_node]:
                shortest_cost[to_node] = new_cost        # relaxation
                predecessor[to_node] = from_node         # track the path

    # Step 3: rebuild path using predecessor
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = predecessor[cur]
    path.reverse()

    return path, shortest_cost[end]


path, cost = bellman_ford(graphs, "A", "E")
print(f"Path: {path}")   # Path: ['A', 'B', 'D', 'E']
print(f"Cost: {cost}")   # Cost: 9
```

---

## Why V-1 times?

In the worst case, the shortest path visits every vertex once, meaning it has at most `V-1` edges. Each round of relaxation is guaranteed to "lock in" at least one more vertex correctly.
```
Round 1:  A gets finalized  (distance 0)
Round 2:  B gets finalized  (A → B = 4)
Round 3:  D gets finalized  (A → B → D = 1)
Round 4:  E gets finalized  (A → B → D → E = 9)
```

# Note


# Reference

