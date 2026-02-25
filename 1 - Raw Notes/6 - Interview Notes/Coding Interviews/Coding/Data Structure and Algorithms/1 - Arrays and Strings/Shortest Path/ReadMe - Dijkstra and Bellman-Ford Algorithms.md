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

## How it works
```python

import heapq
from typing import List

graphs = {
	"A": [("B", 4), ("C", 5)],
	"B": [("A", 4), ("C", 5), ("D", 3)],
	"C": [("A", 5), ("B", 5), ("F", 3)],
	"D": [("B", 2), ("E", 8)],
	"F": [("C", 3), ("E", 2)]
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
- 
# Note


# Reference

