Date: 2026-03-02
Course: https://www.w3schools.com/dsa/dsa_algo_linkedlists_operations.php
Tags: [[W3Schools]] [[Linked Lists]]


# Linked List Operations

## Complexity

**Singly vs Doubly Linked List:**

|Operation|Singly Linked List|Doubly Linked List|
|---|---|---|
|**Traversal**|O(n)|O(n)|
|**Access by index**|O(n)|O(n)|
|**Search**|O(n)|O(n)|
|**Insert at head**|O(1)|O(1)|
|**Insert at tail**|O(n) without tail pointer|O(1) with tail pointer|
|**Insert at middle**|O(n) to find + O(1) to insert|O(n) to find + O(1) to insert|
|**Delete at head**|O(1)|O(1)|
|**Delete at tail**|O(n) need to find prev node|O(1) with tail pointer|
|**Delete at middle**|O(n) to find + O(1) to delete|O(n) to find + O(1) to delete|
|**Sort (Merge Sort)**|O(n log n)|O(n log n)|
|**Space**|O(n)|O(n) extra pointer per node|

---

**Compared to Array/List:**

|Operation|Array|Linked List|
|---|---|---|
|**Access by index**|O(1) ✅|O(n) ❌|
|**Search**|O(n)|O(n)|
|**Insert at head**|O(n) shift needed|O(1) ✅|
|**Insert at tail**|O(1) amortized|O(1) with tail pointer|
|**Insert at middle**|O(n) shift needed|O(n) find + O(1) insert|
|**Delete at head**|O(n) shift needed|O(1) ✅|
|**Delete at middle**|O(n) shift needed|O(n) find + O(1) delete|
|**Sort**|O(n log n) Tim Sort|O(n log n) Merge Sort|
|**Space**|O(n) contiguous|O(n) + pointer overhead|

---

**Key reasons why:**

```
Access O(n):
  head → node1 → node2 → ... → nodeN
  must traverse from head, no direct index jump

Insert/Delete at head O(1):
  new_node.next = head   # just redirect pointers
  head = new_node

Insert/Delete at tail O(n) singly:
  must walk entire list to find second-to-last node
  → O(1) if you maintain a tail pointer

Insert/Delete at middle O(n):
  O(n) to find the position
  O(1) to actually rewire the pointers
  total = O(n)

Why Merge Sort for linked lists:
  Quick Sort needs random access → O(n) per pivot → bad
  Merge Sort only needs sequential access → perfect for linked lists
  No extra space needed unlike array merge sort (no copying)
```

---

**When to use Linked List over Array:**

```
✅ Use Linked List when:
- frequent insert/delete at head
- size changes frequently
- no need for random access
- implementing queues, stacks, LRU cache

❌ Avoid Linked List when:
- need fast index access
- cache performance matters (arrays are cache-friendly, linked lists are not)
- memory is limited (each node has pointer overhead)
```


## Basic things we can do with linked lists are:
1. Traversal
2. Remove a node
```python
def deleteSpecificNode(head, nodeToDelete):

    if head == nodeToDelete:
        return head.next

    currentNode = head
    while currentNode.next and currentNode.next != nodeToDelete:
        currentNode = currentNode.next

    if currentNode.next is None:
        return head

    currentNode.next = currentNode.next.next

    return head
```

3. Insert a node
```python
def insertNodeAtPosition(head, newNode, position):
    if position == 1:
        newNode.next = head
        return newNode
    
    currentNode = head
    for _ in range(position - 2):
        if currentNode is None:
            break
        currentNode = currentNode.next

    newNode.next = currentNode.next
    currentNode.next = newNode
    return head
```
3. Sort
   
## Linked Lists vs Arrays

These are some key linked list properties, compared to arrays:
- Linked lists are not allocated to a fixed size in memory like arrays are, so linked lists do not require to move the whole list into a larger memory space when the fixed memory space fills up, like arrays must.
- Linked list nodes are not laid out one right after the other in memory (contiguously), so linked list nodes do not have to be shifted up or down in memory when nodes are inserted or deleted.
- Linked list nodes require more memory to store one or more links to other nodes. Array elements do not require that much memory, because array elements do not contain links to other elements.
- Linked list operations are usually harder to program and require more lines than similar array operations, because programming languages have better built in support for arrays.
- We must traverse a linked list to find a node at a specific position, but with arrays we can access an element directly by writing myArray[5].

## Time Complexity of Linked Lists Operations
# Note


# Reference

