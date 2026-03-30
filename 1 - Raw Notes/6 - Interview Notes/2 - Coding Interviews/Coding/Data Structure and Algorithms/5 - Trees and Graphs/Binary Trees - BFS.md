---
sr-due: 2026-03-30
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-03-30
Course:
Tags: 

# Content


![](assets/Binary%20Trees%20-%20Types/file-20260330013538803.png)
While DFS was implemented using a stack (recursion uses a stack under the hood), BFS is implemented iteratively with a queue. You _can_ implement BFS with recursion, but it wouldn't make sense as it's a lot more difficult without any benefit. As such, we will look only at iterative implementations in this course.

### **When to use BFS vs DFS?**
We mentioned earlier that in many problems, it doesn't matter if you choose preorder, inorder, or postorder DFS, the important thing is that you just visit all nodes. If you have a problem like this, then it doesn't matter if you use BFS either, because every "visit" to a node will store sufficient information irrespective of visit order.

Because of this, in terms of binary tree algorithm problems, it is very rare to find a problem that using DFS is "better" than using BFS. However, implementing DFS is usually quicker because it requires less code, and is easier to implement if using recursion, so for problems where BFS/DFS doesn't matter, most people end up using DFS.

On the flip side, there are quite a few problems where using BFS makes way more sense algorithmically than using DFS. Usually, this applies to any problem where we want to handle the nodes according to their level. We'll see this in the upcoming example and practice problems.

In an interview, you may be asked some trivia(琐事) regarding BFS vs DFS, such as their drawbacks. 

- The main disadvantage of DFS is that you could end up wasting a lot of time looking for a value. Let's say that you had a **huge** tree, and you were looking for a value that is stored in the root's right child. If you do DFS prioritizing left before right, then you will search the **entire** left subtree, which could be hundreds of thousands if not millions of operations. Meanwhile, the node is literally one operation away from the root. 
- The main disadvantage of BFS is that if the node you're searching for is near the bottom, then you will waste a lot of time searching through all the levels to reach the bottom.

In terms of space complexity, DFS uses space linear with the height of the tree (the maximum depth), whereas BFS uses space linear with the level that has the most nodes. In some cases, DFS will use less space, in other cases, BFS will use less.

For example, in a [perfect binary tree](https://en.wikipedia.org/wiki/Binary_tree#Types_of_binary_trees), DFS would use O(log⁡n) space (if its Unbalanced BST, the worse case is O(n)), whereas BFS would use O(n). The final level in a perfect binary tree has n22n​ nodes, but the tree only has a depth of log⁡nlogn.

However, if you have a lopsided tree (like a straight line), then BFS will have an O(1) space complexity while DFS will have O(n) (although, a lopsided tree is an edge case whereas a more full tree is the expectation).

### **BFS code implementations**
```python 
from collections import deque

def print_all_nodes(root):
    queue = deque([root])
    while queue:
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
# Note


# Reference

