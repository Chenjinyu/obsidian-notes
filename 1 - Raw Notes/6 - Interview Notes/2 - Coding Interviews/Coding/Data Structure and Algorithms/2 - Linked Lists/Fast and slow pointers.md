---
sr-due: 2026-03-14
sr-interval: 10
sr-ease: 2.5
---

Date: 2026-03-14
Course:
Tags: 

# Content
## pseudocode
```python
// head is the head node of a linked list
function fn(head):
    slow = head
    fast = head

    while fast and fast.next:
        Do something here
        slow = slow.next
        fast = fast.next.next
```

#### **`fast` catches the even-length case**
If the list has an even number of nodes, `fast` lands on `null` itself (not on the last node). So without checking `fast`, you'd do `null.next` immediately on the next iteration:
```text
1 -> 2 -> 3 -> 4 -> null 

After some iterations, fast = null 
fast.next → ❌ NullPointerException
```

#### **`fast.next` catches the odd-length case**

If the list has an odd number of nodes, `fast` lands on the last node (not null). So `fast` itself is valid, but `fast.next` is null:
```text
1 -> 2 -> 3 -> null 

fast = 3 (last node)
fast.next = null 
fast.next.next → ❌ NullPointerException
```

So the two conditions guard two different failure modes:

| Condition | Prevents |
|---|---|
| `fast` | dereferencing null when list is even-length |
| `fast.next` | dereferencing null.next when list is odd-length |

# Note


# Reference

