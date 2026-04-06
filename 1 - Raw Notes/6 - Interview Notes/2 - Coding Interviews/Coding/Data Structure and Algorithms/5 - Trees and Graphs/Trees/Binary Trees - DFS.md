---
sr-due: 2026-04-11
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-03-24
Course:
Tags: [[Binary Trees - DFS]]


# Reviews Knowledges Points
```text
04/04/2026
you need manually traversal the tree nodes with the three DFS traversal methods.
```

```text
04/05/2026
In order to improve the memory, 
1. you need to manually get the pre-order, in-order and post-order's nodes to list
2. write down the pre-order, in-order and post-order solution patterns.
```
# Review dates
- 04/04/2026
- 04/05/2026
# Traverse binary trees
Tree traversal is how we access the elements of a tree, and thus is mandatory for solving tree problems.
We start at the `root` and traverse by using the child pointers `.left` and `.right`. When traversing linked lists, we usually do it iteratively. With binary trees, we usually do it recursively.

There are two main types of tree traversals. The first is called depth-first search (DFS). For binary trees specifically, there are 3 ways to perform DFS - preorder, inorder, and postorder (don't worry though, the type you choose rarely matters). The other main type of traversal is called breadth-first search (BFS). Let's start by looking at DFS.

# Depth-first Search(DFS)
>the depth of a node is its distance from the root.

In a DFS, we prioritize depth by traversing as far down the tree as possible in one direction (until reaching a leaf node) before considering the other direction

Because we need to backtrack up the tree after reaching the end of a branch, DFS is typically implemented using recursion, although it is also sometimes done iteratively using a stack. Here is a simple example of recursive DFS to visit every node:
```python
def dfs(node):
    if node == None:
        return

    dfs(node.left)
    dfs(node.right)
    return
```

The good news is that the structure for performing a DFS is very similar across all problems. It goes as follows:

1. Handle the base case(s). Usually, an empty tree (`node = null`) is a base case.
2. Do some logic for the current node
3. Recursively call on the current node's children
4. Return the answer

> As we will see in a moment, steps 2 and 3 may happen in different orders.

## Three types of DFS.
### 1. 1. **Preorder Recursive Traversal**
```python
def preorder_dfs(node):
    if not node:
        return

    print(node.val) # read current node value first
    preorder_dfs(node.left)
    preorder_dfs(node.right)
    return
    
# node -> left -> right
# Pre -> before children
```
### 1. 2. **Preorder Stack Traversal**
```python
# 1. Preorder — node → left → right
# Push right first, then left (LIFO means left gets processed first)
# read node and then all the left nodes, jump up to each node's right to read
def preorder_iterative(root):
    if not root: return
    stack = [root]
    while stack:
        node = stack.pop()
        print(node.val)              # process node first
        if node.right: stack.append(node.right)
        if node.left:  stack.append(node.left)
```

### 1.3. Example of Tree nodes traversal with preorder
```
              9
             / \
            6   10
           / \    \
          5   7   14
         /       /  \
        4       13  15
       / \      /     \
      1   3    12     16 
# Pre-Order: LIST = 9, 6, 5, 4, 1, 3, 7, 10, 14, 13, 12, 15, 16
# read the left node all the down after reading the node
# for example, from the node 14, the order should be 14, 13, 12 -> then to 15, 16. after read 13, then is the left node of node 13.      
```


### 2.1. **Inorder Recursive Traversal**
```python
def inorder_dfs(node):
    if not node:
        return

    inorder_dfs(node.left)
    print(node.val) # read the node only after traversa all left nodes.
    inorder_dfs(node.right)
    return
    
# left -> node -> right
# In -> in the middle of children
```

<span style="color:red; font-size:16px">Remember, the two of Inorder and postorder are more difficult. </span>
### **2. 2. Inorder Stack Traversal**
<span style="color:red">In-order is the odd one out, it's the only one that cannot be done with a simple push/pop loop.
because you need to defer processing until the entire left subtree is exhausted</span>
```python
# 2. Inorder — left → node → right
# Can't process on push — must walk left first, then process on pop

def inorder_dfs(root):
    stack = []
    curr = root
    while stack or curr:
        if curr:
            stack.append(curr)
            curr = curr.left         # keep walking left all the way down, util curr = curr.left is None
        else: # else branch process node and node.right after if curr
            curr = stack.pop()
            print(curr.val)          # process node after all left exhausted
            # there is no stack.append(curr.right)
            # because the append will do in if curr:, and the curr is the curr.right, just from right here.
            curr = curr.right
```
### 2.3. Example of Tree nodes traversal with In-Order
```
              9
             / \
            6   10
           / \    \
          5   7   14
         /       /  \
        4       13  15
       / \      /     \
      1   3    12     16     
# Read all left nodes all the way down, then read the node, then read the right subtree.
# LIST = 1, 4, 3, 5, 6, 7, 9, 10, 12, 13, 14, 15, 16
```

### 3.1. **Postorder Recursive Traversal**
```python
def postorder_dfs(node):
    if not node:
        return

    postorder_dfs(node.left)
    postorder_dfs(node.right)
    print(node.val) # read the node only after traversa left and right
    return

# left -> right -> node
# Post -> after children
```
### 3.2. **Postorder Stack Traversal**
#### 3.2.1. Method 1 (visited flag, my solution for [[../../../../LeetCode Questions/E M - 0543. Diameter of Binary Tree|E M - 0543. Diameter of Binary Tree]])
```python
def postorder_dfs(root):
	# tuple (node, visited) is the standard pattern for iterative post-order whenever
	# you need to process a node after its chilren.
	stack = [(root, False)] # 
	while stack:
	    node, visited = stack.pop()
	    if visited:
	        # process current node HERE
	        # children are already done at this point
	        print(node.val) # whatever computation you need.
	    else:
	        stack.append((node, True))    # revisit current later
	        if node.right: stack.append((node.right, False))
	        if node.left:  stack.append((node.left, False))
```

#### 3.2.2. Method 2
<span style="color:red">below traversal just reverses the pre-order</span>
NOTE: This is a **trick** — it doesn't actually process children before parent, it just **reorders the output** at the end. It works for printing but is **useless** when you need to use children's computed values at the parent.
```python
# 3. Postorder — left → right → node
# Trick: reverse of (node → right → left), which is just preorder with right/left swapped

def preorder_reverse_to_postorder_dfs(root):
    if not root: return
    stack = [root]
    result = []
    while stack:
        node = stack.pop()
        result.append(node.val)      # collect in reverse postorder
        if node.left:  stack.append(node.left)
        if node.right: stack.append(node.right)
    
    print(result[::-1])              # reverse at the end → left → right → node
```

### 3.3. Example of Tree nodes traversal with Post-Order
```
              9
             / \
            6   10
           / \    \
          5   7   14
         /       /  \
        4       13  15
       / \      /     \
      1   3    12     16 
      
# Post order read all left nodes all the way down before read right node.      
# LIST = 1, 3, 4, 5, 7, 6, 12, 13, 16, 15, 14, 10, 9
# the Post order also read all right nodes all the way down before read the parent node. 
# but in any left node which has left node, will be read first, and all the way down
# like from the 10, 
```


#### for the three types of DFS, it always read the left and then read the right. only difference is when to read the node.

### Solving Problems with DFS

## Breadth-First Search (BFS)
# Note


# Reference
- [[../../../../LeetCode Questions/E - 0104. Maximum Depth of Binary Tree|E - 0104. Maximum Depth of Binary Tree]]
- [[../../../../LeetCode Questions/E - 0112. Path Sum|E - 0112. Path Sum]]
- [[../../../../LeetCode Questions/M - 1448. Count Good Nodes in Binary Tree|M - 1448. Count Good Nodes in Binary Tree]]
- [[../../../../LeetCode Questions/E - 0100. Same Tree]]

