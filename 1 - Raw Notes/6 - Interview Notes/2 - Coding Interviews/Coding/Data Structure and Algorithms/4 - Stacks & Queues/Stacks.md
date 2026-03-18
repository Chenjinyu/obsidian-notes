Date: 2026-02-27
Course: https://www.w3schools.com/dsa/dsa_data_stacks.php
Tags: [[DSA]]

# Python Stack — Interview Study Notes

## Overview
A **stack** is a Last-In-First-Out (LIFO) data structure. In Python, it can be implemented using:

- A **Python list**
- A **Linked list** (custom `Node` class)

Each has different tradeoffs. Knowing them deeply will help you answer follow-up questions in interviews.



---

## Q1: What are the time complexities for each stack operation?

### Python List-based Stack

|Operation|Time Complexity|Notes|
|---|---|---|
|`push` (append)|O(1) amortized|Occasional reallocation happens|
|`pop`|O(1)|Removes from end of list|
|`peek`|O(1)|Access last element|
|`len()`|O(1)|Python stores length internally|
|`is_empty`|O(1)|Based on `len()`|

### Linked List-based Stack

|Operation|Time Complexity|Notes|
|---|---|---|
|`push`|O(1)|Insert at head|
|`pop`|O(1)|Remove from head|
|`peek`|O(1)|Read head value|
|`len()`|O(n)|Must traverse all nodes — _unless_ you use a `_count` attribute|
|`is_empty`|O(n)|Same as above — _unless_ you use a `_count` attribute|

---

## Q2: What about Search, Insert, and Delete?

Stacks are **restricted structures** — you can only legally interact with the top. So arbitrary search, insert, and delete are not standard stack operations. But interviewers may ask about the underlying cost if you bypassed the stack rules.

### Python List-based Stack

| Operation                      | Time Complexity | Notes                               |
| ------------------------------ | --------------- | ----------------------------------- |
| Search (find a value)          | O(n)            | Must scan from top to bottom        |
| Insert (at arbitrary position) | O(n)            | Shifts all elements after the index |
| Delete (at arbitrary position) | O(n)            | Shifts all elements after the index |

### Linked List-based Stack

|Operation|Time Complexity|Notes|
|---|---|---|
|Search (find a value)|O(n)|Must traverse node by node|
|Insert (at arbitrary position)|O(n) to find + O(1) to insert|No shifting, but traversal needed|
|Delete (at arbitrary position)|O(n) to find + O(1) to delete|Same — find is the bottleneck|

> **Interview tip:** For a stack, always clarify — "Are you asking about the standard push/pop interface, or arbitrary access into the underlying structure?" This shows you understand the abstraction vs implementation distinction.

### Key insight: Insert/Delete comparison

- **List**: insert/delete in the middle requires **shifting elements** → O(n)
- **Linked list**: insert/delete in the middle requires **traversal to find the position** → O(n), but the actual pointer rewire is O(1) — no shifting needed

The Big O looks the same (O(n)), but the _reason_ is different and worth explaining in an interview.

---

## Q3: Can we make `len()` and `is_empty` O(1) for a linked list?

**Yes.** Add a `_count` attribute to the stack class and update it on every `push` and `pop`. This is the **standard approach** used in production-grade implementations.

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class LinkedListStack:
    def __init__(self):
        self._head = None
        self._count = 0

    def push(self, val):
        node = Node(val)
        node.next = self._head
        self._head = node
        self._count += 1       # O(1)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        val = self._head.val
        self._head = self._head.next
        self._count -= 1       # O(1)
        return val

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._head.val

    def is_empty(self):
        return self._count == 0    # O(1)

    def __len__(self):
        return self._count         # O(1)
```

**With `_count`, all operations on a linked list stack are O(1).**

---

## Q4: Does Python list reallocation affect time complexity?

**Yes, it happens — but it doesn't change the Big O.**

When you `append` to a Python list and it runs out of space, Python:

1. Allocates a **new, larger block** of memory (roughly doubling the size)
2. **Copies all existing elements** to the new block
3. That single operation costs **O(n)**

### Growth pattern (approximate):

```
Capacity 0  → grows to 4
Capacity 4  → grows to 8
Capacity 8  → grows to 16
...
```

### Why we still say O(1) — Amortized Analysis

Reallocation happens _rarely_. The cost gets spread over all the cheap appends:

- n appends total = O(n) total work
- Therefore, **each append = O(1) on average = O(1) amortized**

### Complexity breakdown for a single `append`:

|Scenario|Time|
|---|---|
|Normal append (no realloc)|O(1) actual|
|Append that triggers realloc|O(n) worst case|
|n appends total|O(n) → O(1) amortized per append|

---
## Q5: Should I mention amortized analysis in an interview?
**Yes, and it signals strong understanding.**
- Just saying `O(1)` is acceptable for most answers
- But saying **"O(1) amortized"** shows you know _why_ and earns more credibility
- If an interviewer pushes back on `O(1)`, explain the amortized argument above

Contrast with linked list push: it is **O(1) strict/guaranteed** every single call — no amortization needed.

---

## Design Decision: When to choose which implementation?

|Use case|Better choice|
|---|---|
|Push/pop frequently, rarely check size|Both are fine — linked list has strict O(1) push/pop|
|Check `len()` or `is_empty` often|Python list (or linked list with `_count`)|
|Memory efficiency matters|Python list (contiguous memory, better cache locality)|
|Guaranteed worst-case performance|Linked list (no reallocation surprises)|

### Key tradeoff to remember:

- **Python list**: contiguous memory → better **cache locality**, but occasional reallocation
- **Linked list**: scattered nodes in heap → each node carries a `next` pointer overhead, but **no reallocation ever**

---

## Interview Cheat Sheet

|Concept|One-liner|
|---|---|
|Stack order|LIFO — Last In, First Out|
|List `append`/`pop`|O(1) amortized|
|Linked list push/pop|O(1) strict|
|Linked list `len()` default|O(n) — traverse all nodes|
|Linked list `len()` with `_count`|O(1) — just read the attribute|
|Amortized meaning|Total cost spread over many operations|
|When realloc hits|O(n) worst case for that one append|