---
sr-due: 2026-04-12
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-04-10
Course:
Tags: [[Union-Find(Disjoint Set Union, DSU)]] [[../../Coding/Data Structure and Algorithms/5 - Trees and Graphs/Graphs/Graphs|Graphs]]

# Content

The find and union function look are the same in the below Leetcode problem,
the only differences are two:
1. how to get the two nodes to check the union. 
	1. for 323, the items in sub list is the connection/edge. easy to get the two nodes
	2. for 200, its matrix, the two nodes are the next one in right or the lower one in down. it needs to have row and col loops to get the two nodes
2. for 2D array, need to flatten index
	```text
	# The formula
	index = r * cols + c
	
	Think of it as flattening the grid row by row
	grid (3×4):             flattened index:
	(0,0)(0,1)(0,2)(0,3)    0  1  2  3
	(1,0)(1,1)(1,2)(1,3) →  4  5  6  7
	(2,0)(2,1)(2,2)(2,3)    8  9  10 11
	
	because the parent = list(range(rows * cols))), aslo flatten the rows to 1D.
	```
	
```python
# parent lenght is how many the nodes, for matrix, it should be rows times cols.
parent = list(range(rows * cols))
# rank default vaule as 1 to every node
rank = [1] * rows * cols
def find(x):
	if parent[x] != x:
		parent[x] = find(parnet[x])
	return parent[x]

def union(a, b):
	root_a, root_b = find(a), find(b)

	if root_a == roo_b:
		# union itself, should not count.
		return 0 

	if rank[root_a] < rank[root_b]:
		parent[root_a] = root_b
		rank[root_b] += rank[root_a]
	else:
		parent[root_b] = root_a
		rank[root_a] += rank[root_b]
```

check out 
- [[../M - 0323. Number of Connected Components in an Undirected Graph|M - 0323. Number of Connected Components in an Undirected Graph]]
- [[../M - 0200. Number of Islands|M - 0200. Number of Islands]]



# Note


# Reference

