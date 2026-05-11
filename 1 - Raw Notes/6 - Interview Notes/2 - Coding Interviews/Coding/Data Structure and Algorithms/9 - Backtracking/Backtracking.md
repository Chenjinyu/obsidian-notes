---
sr-due: <% tp.date.now("YYYY-MM-DD") %>
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-05-11
Course:
Tags: 

# Content

**Backtracking** is a way to efficiently run through all possibilities in a problem. It typically uses an optimization that involves abandoning a "path" once it is determined that the path cannot lead to a solution. The idea is similar to binary search trees - if you're looking for a value `x`, and the root node has a value greater than `x`, then you know you can ignore the entire right subtree. Because the number of nodes in each subtree is exponential relative to the depth, backtracking can save huge amounts of computation. Imagine if the constraint was that the string could only have vowels - an exhaustive search would still generate all 26n26n strings, and then check each one for if it only had vowels. With backtracking, we discard all subtrees that have non-vowels, improving from O(26n)O(26n) candidates to O(5n)O(5n).
![800](assets/Backtracking/file-20260511001721935.png)
<span style="color: orange">
Abandoning a path is also sometimes called "pruning(修剪)". <br/>
To summarize the difference between exhaustive search and backtracking: <br/>
In an exhaustive search, we generate all possibilities and then check them for solutions. <br/>
In backtracking, we prune(修剪) paths that cannot lead to a solution, generating far fewer possibilities
</span>

On LeetCode, a strong hint that you should use backtracking is if the input constraints are very small  `(n <= ~15)`, as backtracking algorithms usually have <span style="color:red">exponential time </span> complexities.
Unfortunately in an interview, you will not usually be told the constraints, and even if you try to clarify with the interviewer, they will give a vague answer or just tell you to do your best. This is why it's important to build a good intuition for recognizing when to use a certain algorithm.

# **Implementation**
Backtracking is almost always implemented with recursion - it really doesn't make sense to do it iteratively. In most backtracking problems, you will be building something, either directly (like modifying an array) or indirectly (using variables to represent some state). Here is some pseudocode for a general backtracking format:
```python
// let curr represent the thing you are building
// it could be an array or a combination of variables

function backtrack(curr) {
    if (base case) {
        Increment or add to answer
        return
    }

    for (iterate over input) {
        Modify curr
        backtrack(curr)
        Undo whatever modification was done to curr
    }
}
```

# Note


# Reference

