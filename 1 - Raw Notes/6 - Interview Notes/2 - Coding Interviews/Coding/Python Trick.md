---
sr-due: 2026-05-02
sr-interval: 15
sr-ease: 2.5
---
Date: 2026-03-01
Course:
Tags: 

# Content

## 1. `[[]] * 10`

Python will create 10 sub-lists, and all sub-lists pointer point to the first sub-list in memory.
### What happens?
because, the `* 10` copies the reference, not the object itself.
so, when you change one sub-list value, rest of sub-lists will be changed at the same time

another example to create 3 rows and 3 cols 2D array include 0 integer
```python
matrix = [[0] * mat_len for _ in range(mat_len)]
# [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
# Below example is wrong
matrix = [[0] * mat_len] * mat_len
# although it create the same as above
# [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
# when you 
matrix[0][0] = 1
print(matrix)
# [[1, 0, 0], [1, 0, 0], [1, 0, 0]]
# because in the [[0] * mat_len] is a list, which only reference the pointer. 
```

## 2. `[] * 10`
 It  only create an empty list. * on empty list is always []

## 3 zip
`grip = [[1,2,3],[3,2,1], [2,1,1]]`
`print(list(zip(grip)))` returns:
`[([1, 2, 3],), ([3, 2, 1],), ([2, 1, 1],)]`  <- change to set, element is a list
`print(list(zip(*grip)))` returns:
`[(1, 3, 2), (2, 2, 1), (3, 1, 1)]` <- rotate the row and column

## 4. ord()
the lowercase of english letters are exactly +32 offset from uppercase.
when to solving the string, has upper and lowercase problem. check leetcode: 1544. [Make The String Great](https://leetcode.com/problems/make-the-string-great/)
```python
ord('a') = 97
ord('A') = 65

97 - 65 = 32
```

## 5. set()
the parameter in set must be iterative. 
if want to store (0,0), position in grid
```python
visited = set([(0, 0)])
# equals to below
visited = set()
visited.add((0,0)) # {(0, 0)}

## BUT DOES NOT equal to
visited = set((0,0)) # the (0,0) is treated as two items.
# {0, 0}
```

## 6. List(range(n))
range(10) returns range object, which return an object that produces a sequence of integers 
list(range(10)), list gets the sequence from range 0 to 9
so, list(range(10)) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# Note


# Reference

