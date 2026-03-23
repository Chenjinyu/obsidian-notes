---
sr-due: 2026-03-28
sr-interval: 4
sr-ease: 22.5
---

Date: 2026-03-14
Course:
Tags: [[../../../../../../3 - Zettelkasten/A - Templates/LeetCode Template|LeetCode]] [[Linked Lists]]
#review/15d 

# Review Notes
- to understand the purposes of different pointers. 


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

# Takeaway
### Reverse entire list - Both `prev` and `curr` move
```txt
prev = curr           # prev advances
curr = next_node      # curr advances  
```
> Both pointers walk forward together, `prev` is the "last reversed node" and keeps moving. 
### Reverse sublist - Only `curr`  moves, and `prev` stays frozen. 
reference: [[../../../LeetCode Questions/M - 0092. Reverse Linked List II|M - 0092. Reverse Linked List II]]
```text
prev.next = next_node       # prev stays, but re-aims at new front
curr stays at tail          # 
```
> `prev` is an anchor - it never moves, it just keeps re-pointing to whoever is the new front of the reversed section. `curr` is also frozen as the tail of the growing reversed section.
# Note


# Reference
- [[../../../LeetCode Questions/M - 0092. Reverse Linked List II|M - 0092. Reverse Linked List II]]

