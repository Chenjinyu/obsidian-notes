Date: 2026-03-08
Course:
Tags: 

# Content

## 1. The total sum from 0 to n or from 1 to n
n = len(nums)
total_sum = n * (n + 1) // 2


## 2. // is **integer division** (floor division) — it divides and drops the decimal.
```python
11 // 6 = 1   # 11 / 6 = 1.83 → drop .83 → 1.   向下取整除法(floor division)
12 // 6 = 2   # 12 / 6 = 2.0  → drop .0  → 2
0  // 6 = 0   # 0  / 6 = 0.0  → drop .0  → 0
7  // 6 = 1   # 7  / 6 = 1.16 → drop .16 → 1
13 // 6 = 2   # 13 / 6 = 2.16 → drop .16 → 2
```

## 3. % is the modulo operator - it gives the remainder after division.
```python
11 % 6 = 5    # 11 = 1*6 + 5  → remainder 5 取余
12 % 6 = 0    # 12 = 2*6 + 0  → remainder 0
0  % 6 = 0    # 0  = 0*6 + 0  → remainder 0
7  % 6 = 1    # 7  = 1*6 + 1  → remainder 1
13 % 6 = 1    # 13 = 2*6 + 1  → remainder 1
4  % 2 = 0
3  % 2 = 1
6 % 10 = 6   # 6 = 0*10 + 6 -> remainder 6
```
# Note


# Reference

