Date: 2026-02-24
Course:
Tags: [[DSA]] [[Shortest Path]] 

# Content

To solve the shortest path problem means to check the edges inside the Graph 
until we find a path where we can move from one vertex to another using the lowest possible combined weight along the edges

The sum of weights along the edges that make up a path is called a path cost or a path weight

Algorithms that find the shortest paths, like [Dijkstra's algorithm](https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php) or [the Bellman-Ford algorithm](https://www.w3schools.com/dsa/dsa_algo_graphs_bellmanford.php), find the shortest paths from one start vertex to all other vertices.

To begin with, the algorithms set the distance from the start vertex to all vertices to be infinitely long. And as the algorithms run, edges between the vertices are checked over and over, and shorter paths might be found many times until the shortest paths are found at the end.

Every time an edge is checked and it leads to a shorter distance to a vertex being found and updated, it is called a **relaxation**, or **relaxing** an edge.

## Dijkstra
- Only can visit once.
- It's greedy and 
# Note


# Reference

