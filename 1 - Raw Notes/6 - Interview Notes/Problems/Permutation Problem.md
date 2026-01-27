Date: 2026-01-26
Course:
Tags: [Interview]

# Content
To get all possible orderings of a list, simply pass the list to the function and convert the resulting iterator to a list or loop through it:
```
import itertools

numbers = [1, 2, 3]
result = itertools.permutations(numbers)

print("Full permutations:")
for item in result:
    print(item)

# Output:
# (1, 2, 3)
# (1, 3, 2)
# (2, 1, 3)
# (2, 3, 1)
# (3, 1, 2)
# (3, 2, 1)
```

# Note


# Reference

