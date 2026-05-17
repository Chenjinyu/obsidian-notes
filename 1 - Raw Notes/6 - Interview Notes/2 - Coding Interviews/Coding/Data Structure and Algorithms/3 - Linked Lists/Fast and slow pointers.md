---
sr-due: 2026-06-13
sr-interval: 15
sr-ease: 2.5
---

Date: 2026-03-14
Course:
Tags: 

#review/15d 

# Reviews Knowledges Points
```text
03/23/2026
- check kth node from the end, let fast node loop to k first.
```

# Review Dates
- 03/23/2026
# Content
## pseudocode
```python
# head is the head node of a linked list
function fn(head):
    slow = head
    fast = head

    while fast and fast.next: # needs to check fast if is None first and then fast.next. other wise null.next raise None exeption
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

# Example 1
141. Linked List Cycle: Given the `head` of a linked list, determine if the linked list has a cycle.
```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None
from typing import Optional
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
    # Time complexity: O(n), space complexity: O(1)
        slow = head
        fast = head
        
        while fast and fast.next: # if there is no loop, then, the while loop will exit, after end of link
            slow = slow.next
            fast = fast.next.next
            
            # if its a cycle, how matter the rounds, eventually, 
            # the fast pointer will catch up and equals to slow.
            if slow == fast:
                return True
        return False
```

# Example 2
Given the head of a linked list and an integer `k`, return the k_th node from the end.
For example, given the linked list that represents `1 -> 2 -> 3 -> 4 -> 5` and `k = 2`, return the node with value `4`, as it is the 2nd node from the end.
```python
def find_node(head, k):
	fast = head
	slow = head
	
	for _ in range(k):
		fast = fast.next
	
	while fast:
		slow = slow.next
		fast = fast.next
		
	return slow
```
> Note: we could just convert the list to an array, or we could iterate through once to find the length and then iterate again once we know the length, but there is a more elegant solution.
# Note


# Reference

