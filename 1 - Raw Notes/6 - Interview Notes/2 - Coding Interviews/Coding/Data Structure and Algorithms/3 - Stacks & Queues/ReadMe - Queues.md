Date: 2026-03-03
Course: https://www.w3schools.com/dsa/dsa_data_queues.php
Tags: [[DSA]]

# Python Queue — Interview Study Notes

## What is a Queue?

FIFO — First In, First Out. Like a line at a store: you join at the back, leave from the front.

```
Front                    Back
 ← [1] [2] [3] [4] [5] ←
dequeue                enqueue
```

Three operations matter:
- **enqueue** — add to the back
- **dequeue** — remove from the front
- **peek** — read the front without removing. queue[0]  peek from front, queue[-1], peek from end, no removal

---
## Always use `collections.deque`

```python
from collections import deque
queue = deque()

queue.append(val)      # enqueue — O(1)
queue.popleft()        # dequeue — O(1)
queue[0]               # peek front — O(1), no removal
queue[-1]              # peek back  — O(1), no removal
```

### **Never use a plain list as a queue.** `list.pop(0)` is O(n) because every element shifts left. For n operations that becomes O(n²).

---
## `deque` as Stack vs Queue

`deque` works for both, but for a pure stack a plain `list` is simpler:

```python
stack = []
stack.append(val)   # push — O(1)
stack.pop()         # pop  — O(1)
```

Use `deque` only when you need both ends — queue, sliding window, or monotonic(单调) deque problems.

---

## Time Complexity
|Operation|`deque`|`list`|
|---|---|---|
|enqueue (add to back)|`queue.append(val)` O(1)|`lst.append(val)` O(1) amortized|
|add to front|`queue.appendleft(val)` O(1)|`lst.insert(0, val)` O(n) ❌|
|add to middle|`queue.insert(i, val)` O(n)|`lst.insert(i, val)` O(n)|
|dequeue (remove from front)|`queue.popleft()` O(1) ✅|`lst.pop(0)` O(n) ❌|
|remove from back|`queue.pop()` O(1)|`lst.pop()` O(1)|
|remove from middle|`del queue[i]` O(n)|`del lst[i]` O(n)|
|update by index|`queue[i] = val` O(n)|`lst[i] = val` O(1) ✅|
|peek front|`queue[0]` O(1)|`lst[0]` O(1)|
|peek back|`queue[-1]` O(1)|`lst[-1]` O(1)|
|search|`val in queue` O(n)|`val in lst` O(n)|

### One notable difference worth highlighting — **update by index**:
- `list[i] = val` is O(1) because list is backed by a contiguous array, direct memory access
- `deque[i] = val` is O(n) because deque is a doubly linked list of blocks, index `i` requires traversal

So if your problem needs frequent random index access, `list` wins. If you need fast operations on both ends, `deque` wins.

---
## Peek — Python has no `.peek()`

Unlike Java, Python `deque` has no `.peek()` method. Use index access instead:
```python
queue[0]    # front
queue[-1]   # back
```
---
## LeetCode Example — 933. Number of Recent Calls

### Code Example: [933. Number of Recent Calls](https://leetcode.com/problems/number-of-recent-calls/)
```text
You have a `RecentCounter` class which counts the number of recent requests within a certain time frame.
Implement the `RecentCounter` class:
- `RecentCounter()` Initializes the counter with zero recent requests.
- `int ping(int t)` Adds a new request at time `t`, where `t` represents some time in milliseconds, and returns the number of requests that has happened in the past `3000` milliseconds (including the new request). Specifically, return the number of requests that have happened in the inclusive range `[t - 3000, t]`.

It is **guaranteed** that every call to `ping` uses a strictly larger value of `t` than the previous call.

**Example 1:**
**Input**
["RecentCounter", "ping", "ping", "ping", "ping"]
[[], [1], [100], [3001], [3002]]
**Output**
[null, 1, 2, 3, 3]
**Explanation**
RecentCounter recentCounter = new RecentCounter();
recentCounter.ping(1);     // requests = [1], range is [-2999,1], return 1
recentCounter.ping(100);   // requests = [1, 100], range is [-2900,100], return 2
recentCounter.ping(3001);  // requests = [1, 100, 3001], range is [1,3001], return 3
recentCounter.ping(3002);  // requests = [1, 100, 3001, 3002], range is [2,3002], return 3

**Constraints:**
- `1 <= t <= 109`
- Each test case will call `ping` with **strictly increasing** values of `t`.
- At most `104` calls will be made to `ping`.
```
### Code solution
```python
from collections import deque

class RecentCounter:
    def __init__(self):
        self.queue = deque()

    def ping(self, t: int) -> int:
        self.queue.append(t)
        while self.queue[0] < t - 3000:
            self.queue.popleft()
        return len(self.queue)
```

Key insight: since `t` is always increasing, anything outside `[t-3000, t]` will never be valid again — safe to evict from the left permanently.

---
## When to Reach for a Queue in LeetCode

|Pattern|Why queue fits|
|---|---|
|Sliding window with eviction|Evict stale elements from the left|
|BFS / level-order traversal|Process nodes level by level, FIFO order|
|Moving average / recent window|Fixed-size window, drop oldest first|