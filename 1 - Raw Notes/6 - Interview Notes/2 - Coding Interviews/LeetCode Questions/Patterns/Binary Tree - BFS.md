### **BFS code implementations**
```python 
from collections import deque

def print_all_nodes(root):
    queue = deque([root])
    while queue:
	    # when the previous level finished, the queue will store current all nodes. 
        nodes_in_current_level = len(queue)
        # do some logic here for the current level

        for _ in range(nodes_in_current_level):
            node = queue.popleft()
            
            # do some logic here on the current node
            print(node.val)

            # put the next level onto the queue
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
                
```
![400](assets/Binary%20Trees%20-%20BFS/file-20260330014750835.png|100)

With an efficient queue, the dequeue and enqueue operations are O(1)O(1), which means that the time complexity of BFS is the same as DFS. Again, the main idea is that we visit each node only once, so the time complexity is O(n⋅k)O(n⋅k) where nn is the total number of nodes, and kk is the amount of work we do at each node, usually O(1)O(1). Let's look at some example problems.


# Reference
- [[Binary Tree - BFS]]
- [[../M - 0199. Binary Tree Right Side View|M - 0199. Binary Tree Right Side View]]
- 