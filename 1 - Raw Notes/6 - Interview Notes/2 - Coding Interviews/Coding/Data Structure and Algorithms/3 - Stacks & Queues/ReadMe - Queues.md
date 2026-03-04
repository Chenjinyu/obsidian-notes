Date: 2026-03-03
Course: https://www.w3schools.com/dsa/dsa_data_queues.php
Tags: [[DSA]]

# Python Queue — Interview Study Notes

## Overview

A **queue** is a First-In-First-Out (FIFO) data structure. In Python, it can be implemented using:

- A **Python list**
- A **collections.deque**
- A **Linked list** (custom `Node` class)

Each has different tradeoffs. Understanding them is key for interviews.

---

## Q1: What is a Queue?

A queue works like a line at a store:

- **Enqueue** — add to the **back**
- **Dequeue** — remove from the **front**
- **Peek** — read the **front** without removing

```
Front                    Back
 ← [1] [2] [3] [4] [5] ←
dequeue                enqueue
```

---

## Q2: What are the time complexities for each implementation?

### Python List-based Queue ❌ (naive, not recommended)

|Operation|Time Complexity|Notes|
|---|---|---|
|`enqueue` (append to end)|O(1) amortized|Same reallocation behavior as stack|
|`dequeue` (pop from front)|**O(n)**|Shifts all remaining elements left — expensive!|
|`peek`|O(1)|Read index 0|
|`len()`|O(1)|Python stores length internally|
|`is_empty`|O(1)|Based on `len()`|

> **Key insight:** Using a plain list as a queue is a common mistake. `pop(0)` is O(n) because every element shifts left after removal.

---

### collections.deque (pronounce: de:k)-based Queue ✅ (recommended for interviews)

| Operation           | Time Complexity | Notes                               |
| ------------------- | --------------- | ----------------------------------- |
| `enqueue` (append)  | O(1) amortized  | Add to right end                    |
| `dequeue` (popleft) | O(1)            | Remove from left end — no shifting! |
| `peek`              | O(1)            | Read `deque[0]`                     |
| `len()`             | O(1)            | Built-in                            |
| `is_empty`          | O(1)            | Based on `len()`                    |

`deque` (double-ended queue) is implemented as a **doubly linked list of fixed-size blocks** internally, so both ends are O(1).

---

### Linked List-based Queue

|Operation|Time Complexity|Notes|
|---|---|---|
|`enqueue`|O(1)|Insert at tail — requires a `_tail` pointer|
|`dequeue`|O(1)|Remove from head|
|`peek`|O(1)|Read head value|
|`len()`|O(n) default / O(1) with `_count`|Same trick as stack|
|`is_empty`|O(n) default / O(1) with `_count`|Same trick as stack|

> **Key insight:** You need **both a `_head` and `_tail` pointer**. Without `_tail`, enqueue would be O(n) since you'd have to traverse to the end every time.

---

## Q3: Full Implementation — Linked List Queue

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class LinkedListQueue:
    def __init__(self):
        self._head = None   # front — dequeue from here
        self._tail = None   # back  — enqueue from here
        self._count = 0

    def enqueue(self, val):
        node = Node(val)
        if self._tail:
            self._tail.next = node
        self._tail = node
        if self._head is None:   # first element
            self._head = node
        self._count += 1         # O(1)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        val = self._head.val
        self._head = self._head.next
        if self._head is None:   # queue is now empty
            self._tail = None
        self._count -= 1         # O(1)
        return val

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._head.val

    def is_empty(self):
        return self._count == 0  # O(1)

    def __len__(self):
        return self._count       # O(1)
```

---

## Q4: Full Implementation — deque-based Queue

```python
from collections import deque

class Queue:
    def __init__(self):
        self._data = deque()

    def enqueue(self, val):
        self._data.append(val)       # add to right

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._data.popleft()  # remove from left — O(1)

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._data[0]

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)
```

---

## Q5: What about Search, Insert, and Delete?

Queues are also **restricted structures** — you enqueue at the back and dequeue from the front only. Arbitrary access is not part of the queue interface. But interviewers may ask about the underlying cost.

### Python List / deque-based Queue

|Operation|Time Complexity|Notes|
|---|---|---|
|Search (find a value)|O(n)|Must scan all elements|
|Insert (at arbitrary position)|O(n)|List shifts elements; deque also O(n) for middle|
|Delete (at arbitrary position)|O(n)|Same reason as insert|

### Linked List-based Queue

|Operation|Time Complexity|Notes|
|---|---|---|
|Search (find a value)|O(n)|Traverse node by node|
|Insert (at arbitrary position)|O(n) to find + O(1) to rewire|Traversal is the bottleneck|
|Delete (at arbitrary position)|O(n) to find + O(1) to rewire|Same|

> **Note:** Insert/delete at the **front or back** specifically are O(1) for a linked list queue since you have `_head` and `_tail` pointers — but arbitrary middle positions are still O(n).

### deque insert/delete edge case

`collections.deque` supports `appendleft` / `popleft` at O(1), but inserting or deleting from the **middle** (via `insert(i, val)` or `del`) is still **O(n)**.

---

## Q6: Why not just use a list with `pop(0)`?

`pop(0)` on a list is **O(n)** because Python must shift every remaining element one position to the left in memory.

```
Before dequeue: [1, 2, 3, 4, 5]
Remove index 0: [2, 3, 4, 5]   ← elements 2-5 all shifted left
```

For n dequeue operations on a list, that's **O(n²) total** — a performance disaster for large queues.

---

## Q7: Stack vs Queue — side by side

|Stack|Queue| |
|---|---|---|
|Order|LIFO (Last In, First Out)|FIFO (First In, First Out)|
|Add|push → top|enqueue → back|
|Remove|pop ← top|dequeue ← front|
|Common use|undo, recursion, DFS|scheduling, BFS, task queues|

---

## Design Decision: When to choose which implementation?

|Use case|Better choice|
|---|---|
|Quick implementation in interview|`collections.deque`|
|Need strict O(1) guaranteed (no amortized)|Linked list with `_head`, `_tail`, `_count`|
|Memory efficiency|`deque` (internally optimized blocks)|
|Teaching/understanding internals|Linked list|

---

## Interview Cheat Sheet

|Concept|One-liner|
|---|---|
|Queue order|FIFO — First In, First Out|
|List `pop(0)`|O(n) — never use for queue dequeue|
|`deque.popleft()`|O(1) — use this instead|
|Linked list enqueue|O(1) — but needs a `_tail` pointer|
|Linked list dequeue|O(1) — remove from `_head`|
|Linked list `len()` with `_count`|O(1) — same trick as stack|
|`_tail` pointer purpose|Avoid O(n) traversal on enqueue|
|When `_tail` must be set to None|When the last element is dequeued|
|Best built-in for queue in Python|`collections.deque`|