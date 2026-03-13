---
sr-due: 2026-03-28
sr-interval: 15
sr-ease: 2.5
---
Date: 2026-03-01
Course:
Tags: 

# Content

## `1. [[]] * 10`

Python will create 10 sub-lists, and all sub-lists pointer point to the first sub-list in memory.
### What happens?
because, the `* 10` copies the reference, not the object itself.
so, when you change one sub-list value, rest of sub-lists will be changed at the same time

## `2. [] * 10`
 It  only create an empty list. * on empty list is always []

## 3 zip
`grip = [[1,2,3],[3,2,1], [2,1,1]]`
`print(list(zip(grip)))` returns:
`[([1, 2, 3],), ([3, 2, 1],), ([2, 1, 1],)]`  <- change to set, element is a list
`print(list(zip(*grip)))` returns:
`[(1, 3, 2), (2, 2, 1), (3, 1, 1)]` <- rotate the row and column

# Note


# Reference

