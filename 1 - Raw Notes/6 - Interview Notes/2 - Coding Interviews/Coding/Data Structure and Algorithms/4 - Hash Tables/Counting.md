Date: 2026-03-09
Course:
Tags: 

# Content

Counting is a very common pattern with hash maps. By "counting", we are referring to tracking the frequency of things. This means our hash map will be mapping keys to integers. Anytime you need to count anything, think about using a hash map to do it.


# Note

In Python, the [collections module](https://docs.python.org/3/library/collections.html) provides very useful data structures. We will be using a [defaultdict](https://docs.python.org/3/library/collections.html#collections.defaultdict) in the Python code. Functionality-wise, a defaultdict is the same as a hash map, it's just more pleasant to work with.
```python
from collections import defaultdict

counts = defaultdict(int)
counts["a"] += 1   # "a" didn't exist → defaults to 0, then +1 → 1
counts["a"] += 1   # now "a" = 2
counts["b"]        # "b" didn't exist → defaults to 0

print(counts)  # defaultdict(<class 'int'>, {'a': 2, 'b': 0})
```
# Reference

