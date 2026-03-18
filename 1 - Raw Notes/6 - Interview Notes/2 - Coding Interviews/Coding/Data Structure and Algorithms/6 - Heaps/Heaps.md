---
sr-due: <% tp.date.now("YYYY-MM-DD") %>
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-03-17
Course: https://leetcode.com/explore/interview/card/leetcodes-interview-crash-course-data-structures-and-algorithms/708/heaps/4638/
Tags: [[Heaps]]

# Content

A heap is a data structure that is an implementation of the [priority queue](https://en.wikipedia.org/wiki/Priority_queue).

Note that a priority queue is an abstract data structure. A heap is one of many ways to implement a priority queue. However, people often use the two terms interchangeably. In this course, we will use the term "heap".

A heap is a container that stores elements, and supports the following operations:
- Add an element in O(log⁡n)O(logn)
- Remove the minimum element in O(log⁡n)O(logn)
- Find the minimum element in O(1)O(1)

> > A heap can also find the max elements instead of the min elements. 
> > If a heap is configured to find/remove the min element, it's called a min heap. 
> > If it's configured to find/remove the max element, it's called a max heap.


## Bubbling up
“**Bubbling up**” (also called **sift-up** or **heapify-up**) is what happens after you insert a new element into a heap.

### # The core idea
A heap must satisfy a rule:
- **Min-heap** → parent ≤ children
- **Max-heap** → parent ≥ children
When you insert a new element, you:
1. Put it at the **end (bottom)** of the heap
2. It might **break the heap rule**
3. So you **move it upward step by step** until the rule is restored
👉 That upward movement = **bubbling up**
# Note


# Reference

