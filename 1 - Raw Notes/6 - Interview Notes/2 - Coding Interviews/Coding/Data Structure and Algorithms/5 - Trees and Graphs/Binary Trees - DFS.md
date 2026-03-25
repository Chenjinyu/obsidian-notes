---
sr-due: <% tp.date.now("YYYY-MM-DD") %>
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-03-24
Course:
Tags: 

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
#### 1. **Preorder traversal**
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

#### 2. **Inorder traversal**
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

#### 3. **Postorder traversal**
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

#### for the three types of DFS, it always read the left and then read the right. only difference is when to read the node.

### Solving Problems with DFS

## Breadth-First Search (BFS)
# Note


# Reference
- [[../../../LeetCode Questions/E - 0104. Maximum Depth of Binary Tree|E - 0104. Maximum Depth of Binary Tree]]
- [[../../../LeetCode Questions/E - 0112. Path Sum|E - 0112. Path Sum]]

