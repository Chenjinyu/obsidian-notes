---
sr-due: <% tp.date.now("YYYY-MM-DD") %>
sr-interval: 15
sr-ease: 2.5
---

Date: 2026-03-14
Course:
Tags: 
#review/15d 
# Content

While [reversing a linked list](https://leetcode.com/problems/reverse-linked-list/) is a common interview problem in itself, it is also a technique that can be a step in solving different problems. 
[[Elegantly performing]] the reversal requires a good understanding of how to move pointers around,

# Example

```python
def reverse_list(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next # first, make sure we don't lose the next node
        curr.next = prev      # reverse the direction of the pointer
        prev = curr           # set the current node to prev for the next node
        curr = next_node      # move on
    
    # here should return prev, because the curr will point to None in the last step when curr is the end of node.
    return prev
```
# Note


# Reference

