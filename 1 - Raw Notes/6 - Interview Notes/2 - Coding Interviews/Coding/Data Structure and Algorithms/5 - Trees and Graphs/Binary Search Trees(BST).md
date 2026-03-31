---
sr-due: <% tp.date.now("YYYY-MM-DD") %>
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-03-30
Course:
Tags: 

# Content
A binary search tree (BST) is a type of binary tree. A BST has the following property:
For each node, all values in its left subtree are less than the value in the node, and all values in its right subtree are greater than the value in the node.
$ This property also implies that values in a BST must be unique.$

![600](assets/Binary%20Search%20Trees(BST)/file-20260330234442967.png)
With a binary search tree, operations like searching, adding, and removing can be done in <span style="color:red">O(log⁡n)</span> time on average, where n is the number of nodes in the tree, using something called **binary search**, which is the focus of an upcoming chapter.

Let's say you have the above tree, and you want to check if the value `20` existed. Starting at the root, we can see that `23 > 20`. This means we can ignore the right subtree, because every value in the subtree is also going to be greater than `20`. We start searching in the left subtree. At the next step, `20 > 8`, so now we can ignore the left subtree, and move to the right. Next, `20 > 17`, so once again we can ignore the left subtree. Finally, we find the `20` after moving right once more.

This process has an average time complexity of <span style="color:red">O(log⁡n)</span>. In the worst case scenario, let's say with a tree that had no `right` children and was just a straight line (basically a linked list), the time complexity would be <span style="color:red">O(n)</span>

![](assets/Binary%20Trees%20-%20Types/file-20260330013538803.png)


# Note


# Reference

