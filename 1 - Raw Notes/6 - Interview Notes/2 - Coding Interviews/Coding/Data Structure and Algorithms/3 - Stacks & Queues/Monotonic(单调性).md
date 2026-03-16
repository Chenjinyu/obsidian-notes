---
sr-due: <% tp.date.now("YYYY-MM-DD") %>
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-03-16
Course:
Tags: 

# Content
A monotonic stack or queue is one whose elements are always sorted. It can be sorted either ascending or descending, depending on the algorithm. Monotonic stacks and queues maintain their sorted property by removing elements that would violate the property before adding new elements. For example, let's say you had a monotonically increasing stack, currently `stack = [1, 5, 8, 15, 23]`. You want to push `14` onto the stack. To maintain the sorted property, we need to first pop the `15` and `23` before pushing the `14` - after the push operation, we have `stack = [1, 5, 8, 14]`.

Here's some pseudocode for maintaining a monotonic increasing stack over an input array:
```python
Given an integer array nums

stack = []
for num in nums:
    while stack.length > 0 AND stack.top >= num:
        stack.pop()
    // Between the above and below lines, do some logic depending on the problem
    stack.push(num)
    
    
As you can see, before we push a `num` onto the stack, 
we first check if the monotonic property would be violated(违反), and pop elements until it won't be.    
```

>As we discussed earlier in the sliding window chapter, despite the nested loop, the total time complexity is still O(n), where n is the length of the array, 
>because the inner while loop can only iterate over each element once across all for loop iterations, making the for loop iterations amortized O(1).

Monotonic stacks and queues are useful in problems that, for each element, involves finding the "next" element based on some criteria, for example, the next greater element. They're also good when you have a dynamic window of elements and you want to maintain knowledge of the maximum or minimum element as the window changes. In more advanced problems, sometimes a monotonic stack or queue is only one part of the algorithm. Let's look at some examples.

- [[../../../LeetCode Questions/M - 0739. Daily Temperatures|M - 0739. Daily Temperatures]]
# Note


# Reference

