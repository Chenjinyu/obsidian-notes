---
sr-due: 2026-04-12
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-04-10
Course:
Tags: 

# Content

```python
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

