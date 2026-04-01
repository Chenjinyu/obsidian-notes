---
sr-due: <% tp.date.now("YYYY-MM-DD") %>
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-03-24
Course:
Tags: [[Binary Trees - DFS]]

# Content

## Traverse binary trees
Tree traversal is how we access the elements of a tree, and thus is mandatory for solving tree problems.
We start at the `root` and traverse by using the child pointers `.left` and `.right`. When traversing linked lists, we usually do it iteratively. With binary trees, we usually do it recursively.

There are two main types of tree traversals. The first is called depth-first search (DFS). For binary trees specifically, there are 3 ways to perform DFS - preorder, inorder, and postorder (don't worry though, the type you choose rarely matters). The other main type of traversal is called breadth-first search (BFS). Let's start by looking at DFS.

## Depth-first Search(DFS)
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

### three types of DFS.
#### 1. 1. **Preorder Recursive Traversal**
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
#### 1. 2. **Preorder Stack Traversal**
```python
# 1. Preorder — node → left → right
# Push right first, then left (LIFO means left gets processed first)

def preorder_iterative(root):
    if not root: return
    stack = [root]
    while stack:
        node = stack.pop()
        print(node.val)              # process node first
        if node.right: stack.append(node.right)
        if node.left:  stack.append(node.left)
```

#### 1.3. Example of Tree nodes traversal with preorder
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
      
      
# LIST = 9, 6, 5, 4, 1, 3, 7, 10, 14, 13, 12, 15, 16
# read the left node all the down after reading the node
# for example, from the node 14, the order should be 14, 13, 12 -> then to 15, 16. after read 13, then is the left node of node 13.      
```


#### 2.1. **Inorder Recursive Traversal**
```python
def inorder_dfs(node):
    if not node:
        return

    inorder_dfs(node.left)
    print(node.val) # read the node only after traversa all left nodes.
    inorder_dfs(node.right)
    return
    
# left -> node -> rigth
# In -> in the middle of children
```

<span style="color:red; font-size:16px">Remember, the two of Inorder and postorder are more difficult. </span>
#### **2. 2. Inorder Stack Traversal**
<span style="color:red">In-order is the odd one out, it's the only one that cannot be done with a simple push/pop loop.
because you need to defer processing until the entire left subtree is exhausted</span>
```python
# 2. Inorder — left → node → right
# Can't process on push — must walk left first, then process on pop

def inorder_iterative(root):
    stack = []
    curr = root
    while stack or curr:
        if curr:
            stack.append(curr)
            curr = curr.left         # keep walking left
        else:
            curr = stack.pop()
            print(curr.val)          # process node after all left exhausted
            curr = curr.right
```

#### 2.3. Example of Tree nodes traversal with In-Order
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
      
# In order read all left nodes all the way down before read node.      
# LIST = 1, 4, 
```


#### 3.1. **Postorder Recursive Traversal**
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
#### 3.2. **Postorder Stack Traversal**
<span style="color:red">below traversal just reverses the pre-order</span>
```python
# 3. Postorder — left → right → node
# Trick: reverse of (node → right → left), which is just preorder with right/left swapped

def postorder_iterative(root):
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
#### for the three types of DFS, it always read the left and then read the right. only difference is when to read the node.

### Solving Problems with DFS

## Breadth-First Search (BFS)
# Note


# Reference
- [[../../../LeetCode Questions/E - 0104. Maximum Depth of Binary Tree|E - 0104. Maximum Depth of Binary Tree]]
- [[../../../LeetCode Questions/E - 0112. Path Sum|E - 0112. Path Sum]]
- [[../../../LeetCode Questions/M - 1448. Count Good Nodes in Binary Tree|M - 1448. Count Good Nodes in Binary Tree]]
- [[E - 0100. Same Tree]]

