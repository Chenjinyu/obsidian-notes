---
sr-due: <% tp.date.now("YYYY-MM-DD", 3) %>
sr-interval: 1
sr-ease: 2.5
---

Creation Date: 2026-04-16
Course: https://leetcode.com/problems/seat-reservation-manager/description/
Tags: [[LeetCode Template]]

#review/daily #review/3d 

# Reviews Knowledges Points

# Review dates

# Problem
Design a system that manages the reservation state of `n` seats that are numbered from `1` to `n`.

Implement the `SeatManager` class:

- `SeatManager(int n)` Initializes a `SeatManager` object that will manage `n` seats numbered from `1` to `n`. All seats are initially available.
- `int reserve()` Fetches the **smallest-numbered** unreserved seat, reserves it, and returns its number.
- `void unreserve(int seatNumber)` Unreserves the seat with the given `seatNumber`.

**Example 1:**

**Input**
["SeatManager", "reserve", "reserve", "unreserve", "reserve", "reserve", "reserve", "reserve", "unreserve"]
[[5], [], [], [2], [], [], [], [], [5]]
**Output**
[null, 1, 2, null, 2, 3, 4, 5, null]

**Explanation**
SeatManager seatManager = new SeatManager(5); // Initializes a SeatManager with 5 seats.
seatManager.reserve();    // All seats are available, so return the lowest numbered seat, which is 1.
seatManager.reserve();    // The available seats are [2,3,4,5], so return the lowest of them, which is 2.
seatManager.unreserve(2); // Unreserve seat 2, so now the available seats are [2,3,4,5].
seatManager.reserve();    // The available seats are [2,3,4,5], so return the lowest of them, which is 2.
seatManager.reserve();    // The available seats are [3,4,5], so return the lowest of them, which is 3.
seatManager.reserve();    // The available seats are [4,5], so return the lowest of them, which is 4.
seatManager.reserve();    // The only available seat is seat 5, so return 5.
seatManager.unreserve(5); // Unreserve seat 5, so now the available seats are [5].

**Constraints:**

- `1 <= n <= 105`
- `1 <= seatNumber <= n`
- For each call to `reserve`, it is guaranteed that there will be at least one unreserved seat.
- For each call to `unreserve`, it is guaranteed that `seatNumber` will be reserved.
- At most `105` calls **in total** will be made to `reserve` and `unreserve`.


# Step 1 - Understand the problem (10 mins)
- What are the input and output
- What are the edge cases? create your own examples
- What constraints matter?

1. Allow duplicate?
2. Allow Negative numbers?
3. Allow Empty List

## How do you think about this problem?
## Can you find out the exit condition? 
## What is the solution pattern? and why

# Step 2 - Try Brute Force First to help you understand the structure of the problems
```python

```

# Step 3 - Think about Optimization
```python

```

# Step 4 - If stuck > 20 mins, Study the solution
1. Why does the algorithm work?
2. What pattern is this problem?
3. What problem type does it belong to?

# Step 5 - Re implement from scratch. 
```python

```

# Takeaways

# Reference
