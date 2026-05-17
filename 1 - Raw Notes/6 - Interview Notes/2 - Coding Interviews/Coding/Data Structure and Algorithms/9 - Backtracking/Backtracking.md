---
sr-due: 2026-05-18
sr-interval: 1
sr-ease: 2.5
---
Date: 2026-05-11
Course:
Tags: [[Backtracking]] [[../../../../../../DFS & Backtracking|DFS & Backtracking]]

# Reference
- [[../../../LeetCode Questions/M - 0077. Combinations|M - 0077. Combinations]]
- [[../../../LeetCode Questions/M - 0078. Subsets|M - 0078. Subsets]]
- [[../../../LeetCode Questions/M - 0046. Permutations|M - 0046. Permutations]]
- [[../../../LeetCode Questions/M - 0017. Letter Combinations of a Phone Number|M - 0017. Letter Combinations of a Phone Number]]
- [[../../../LeetCode Questions/M - 0039. Combination Sum|M - 0039. Combination Sum]]

# Content

Backtracking is a problem-solving technique where you:
> build a solution step-by-step,  
> explore possibilities,  
> and undo choices when needed.

The key idea is:
```python
try
recurse
undo
```

# Core intuition
Imagine walking through a maze.
At every intersection:
- choose a path
- continue exploring
- if dead end:
    - go back
    - try another path

That “go back and try again” is:
```python
backtracking
```

# Classic structure
```python
def backtrack(path, choices):

    if solution found:
        save answer
        return

    for choice in choices:

        make choice

        backtrack(...)

        undo choice
```
The “undo choice” part is what makes it backtracking.
# Example 1 — Subsets ([[../../../LeetCode Questions/M - 0078. Subsets|M - 0078. Subsets]])
Problem:
```python
nums = [1,2]
```
Find all subsets:
```python
[]
[1]
[2]
[1,2]
```

# Decision tree
Choose or not choose, Leetcode example: [[../../../LeetCode Questions/M - 0078. Subsets|M - 0078. Subsets]]
At each number:
```python
take it
or
skip it
```

# Backtracking code
The same pattern Leetcodes:
- [[../../../LeetCode Questions/M - 0077. Combinations|M - 0077. Combinations]]
- [[../../../LeetCode Questions/M - 0078. Subsets|M - 0078. Subsets]]
- [[../../../LeetCode Questions/M - 0046. Permutations|M - 0046. Permutations]]
```python
# DFS & Backtracking
res = []
def backtrack(start, path):
    res.append(path[:])
    for i in range(start, len(nums)):
        path.append(nums[i])
        backtrack(i + 1, path)
        path.pop()

backtrack(0, [])
```

# Important part
```python
path.append(...) # choose
```
Choose, 
Then:
```python
path.pop() # undo chioce
```
undo choice.

<span style="color:red; font-weight:bold">That is the essence(真髓).</span>

# Why recursion works
Each recursive call represents:
```python
a partial solution state
```
Backtracking explores all valid continuations.

# Common Backtracking Problems

## 1. Mutable-state backtracking

```python
# It has explicit undo
path.append()
backtrack()
path.pop()  # undo
```

### Subsets
Choose/not choose. [[../../../LeetCode Questions/M - 0078. Subsets|M - 0078. Subsets]]
### Permutations
Arrange elements. [[../../../LeetCode Questions/M - 0046. Permutations|M - 0046. Permutations]]

### Combination
Arrange elements. 
[[../../../LeetCode Questions/M - 0077. Combinations|M - 0077. Combinations]]
[[../../../LeetCode Questions/M - 0047. Permutations II|M - 0047. Permutations II]]
[[../../../LeetCode Questions/M - 0017. Letter Combinations of a Phone Number|M - 0017. Letter Combinations of a Phone Number]]
### Combination Sum
Find combinations reaching target. 
- [[../../../LeetCode Questions/M - 0039. Combination Sum|M - 0039. Combination Sum]]
- [[../../../LeetCode Questions/M - 0040. Combination Sum II|M - 0040. Combination Sum II]]
- [[../../../LeetCode Questions/M - 0216. Combination Sum III|M - 0216. Combination Sum III]]

#### Most accurate mental model
think:

| Problem         | What is a node?           | When save answer? |
| --------------- | ------------------------- | ----------------- |
| Subsets         | any partial subset        | every node        |
| CombinationSum3 | partial valid combination | only leaf         |
| Combination Sum | partial sum path          | only valid target |
| Permutations    | ordering state            | leaf              |
That distinction explains the traversal feeling much more accurately.

## N#-Queens
Place queens safely.
[[../../../LeetCode Questions/H - 0051. N-Queens|H - 0051. N-Queens]]
[[../../../LeetCode Questions/H - 0052. N-Queens II|H - 0052. N-Queens II]]
### Word Search
DFS through board. [[../../../LeetCode Questions/M - 0079. Word Search|M - 0079. Word Search]]

### Parentheses
- [[M - 0022. Generate Parentheses]]
- 

### Sudoku Solver
Try valid digits recursively.
### Palindrome Partitioning
Try every valid split.
[[../../../LeetCode Questions/M - 0131. Palindrome Partitioning|M - 0131. Palindrome Partitioning]]

### Other
- 
## 2. Immutable-state backtracking

Each recursive call gets its own independent number/answer, and there is no choose or not choose term, it ONLY provides the possible candidates. 
then to choose them and abandon them(invalid branches). so, it only has choose and abandon.

- [[../../../LeetCode Questions/M - 0967. Numbers With Same Consecutive Differences|M - 0967. Numbers With Same Consecutive Differences]] this problem has a outer for loop, why
- 

# Mental model
Backtracking usually means:
```python
generate all possibilities
```
with pruning to avoid invalid paths.

# The three major ingredients

## 1. State
What currently exists?
Example:
```python
current path
current sum
visited nodes
```

## 2. Choices
What can we try next?
Example:
```python
which number to pick
which cell to visit
which character to use
```

## 3. Constraints
When should we stop/prune?
Example:
```python
sum > target
duplicate detected
invalid queen placement
```

# Why backtracking is expensive
Because it often explores:
```python
all combinations
all permutations
```
Complexity often becomes:
```text
                    O(2^n)  
    or 
                    O(n!)  
```

# Difference between DFS and Backtracking
People often confuse them.
## DFS
General traversal technique.
Example:
- trees
- graphs

May not undo state.

## Backtracking
DFS + undo choices.
Specifically for:
```python
searching solution space
```

# Example analogy

## DFS
Walk through all rooms in a house.
## Backtracking
Try all possible ways to arrange furniture,  
undoing arrangements repeatedly.

# Typical interview signal words

When problem says:
```python
all combinations
all permutations(排列)
generate
find every possible
```

suspect:
```python
backtracking
```

immediately.

# One of the most important interview patterns
Backtracking is a core interview category alongside:
- graph traversal
- sliding window
- binary search
- dynamic programming
- greedy

Mastering it unlocks many medium/hard problems quickly.


## Backtracking has stayed very common in technical interviews because it tests several important skills at once:
- recursion
- state management
- tree/graph traversal
- pruning
- complexity analysis
- clean coding under pressure

Companies like Meta, Google, Amazon, and Capital One often use these problems because they reveal whether a candidate can systematically explore solution spaces.

What you’re noticing on LeetCode is real:  
recent interview trends heavily favor:
- DFS/backtracking
- graphs
- trees
- heap/top-k
- interval problems
- binary search on answer
- dynamic programming with memoization

Pure “hard DP” appears less frequently than a few years ago in many interviews. Backtracking especially appears because it’s flexible.
 
--- 

The important thing now is not memorizing solutions.
You want to train yourself to recognize:
# Signals for Backtracking
If the problem says:
- all possible
- every combination
- enumerate
- generate
- partition
- permutations
- subsets
- paths

you should immediately think:
> “This is probably DFS + backtracking.” and Backtracking is essentially DFS on a decision tree.


A very practical interview strategy:
# Master these patterns deeply

1. Subsets
2. Combinations
3. Permutations
4. Combination Sum
5. Word Search
6. Palindrome Partitioning
7. N-Queens
8. All Paths From Source to Target

If you truly understand these, most interview backtracking problems become variations instead of entirely new problems.


# Note


# Reference

