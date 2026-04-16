---
sr-due: 2026-04-30
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-03-17
Course: https://leetcode.com/explore/interview/card/leetcodes-interview-crash-course-data-structures-and-algorithms/708/heaps/4638/
Tags: [[Heaps]]

#review/15d 
# Content

## IMPORTANT FIRST
```python
import heapq
nums = [10, 21,4,1,3,6]
heapq.heapify(nums)
print(nums) # [1, 3, 4, 21, 10, 6]
heapq.heappush(nums, 0)
print(nums) # [0, 3, 1, 21, 10, 6, 4]
heapq.heappop(nums)
print(nums) # [1, 3, 4, 21, 10, 6]
```
<span style="color:red">-> A heap is not a sorted array. It only guarantees the minimum is at index 0.</span>
## The heap property (min-heap)
Every parent must be **smaller than its children**. That's the only rule — siblings have no guaranteed order.
```
heapify([10, 21, 4, 1, 3, 6])  →  [1, 3, 4, 21, 10, 6]

visualized as a tree:
        1          ← index 0 (min, always here)
       / \
      3    4       ← children of 1
     / \  /
   21  10 6        ← children of 3 and 4

parent < children  ✅ (heap property satisfied)
but siblings have no order between them)
```



---
A heap is a data structure that is an implementation of the [priority queue](https://en.wikipedia.org/wiki/Priority_queue).

Note that a priority queue is an abstract data structure. A heap is one of many ways to implement a priority queue. However, people often use the two terms interchangeably. In this course, we will use the term "heap".

A heap is a container that stores elements, and supports the following operations:
- Add an element in O(log⁡n)
- Remove the minimum element in O(log⁡n)
- Find the minimum element in O(1)
- heapify array takes O(n)

> > A heap can also find the max elements instead of the min elements. 
> > If a heap is configured to find/remove the min element, it's called a min heap. 
> > If it's configured to find/remove the max element, it's called a max heap.

A binary heap implements a binary tree, but with only an array. 
The idea is that each element in the array is a node in the tree. 
The smallest element in the tree is the root, and the following property is maintained at every node: if `A` is the parent of `B`, then `A.val <= B.val`. 
**Notice that this property directly implies that the root is the smallest element.**
<span style="color:red">Another constraint is that the tree must be a [complete tree](https://en.wikipedia.org/wiki/Binary_tree#complete).</span>
## Bubbling up
“**Bubbling up**” (also called **sift-up** or **heapify-up**) is what happens after you insert a new element into a heap.
Insert at bottom, then keep swapping with parent until heap property is restored
#### If a node is at index `i`, then its children are at indices `2i + 1` and `2i + 2`.
### # The core idea
A heap must satisfy a rule:
- **Min-heap** → parent ≤ children
- **Max-heap** → parent ≥ children
When you insert a new element, you:
1. Put it at the **end (bottom)** of the heap
2. It might **break the heap rule**
3. So you **move it upward step by step** until the rule is restored
👉 That upward movement = **bubbling up**

## Bubbling down
- **Bubbling up** → used when inserting
- **Bubbling down (heapify-down)** → used when removing root

## An existing array of elements can also be converted into a heap in linear time, although the process is complicated. 
```python
# In Python, we will use the heapq module
# Note: heapq only implements min heaps
import heapq

# Declaration: heapq does not give you a heap data structure.
# You just use a normal list, and heapq provides you with
# methods that can be used on this list to perform heap operations
heap = []

# Add to heap
heapq.heappush(heap, 1)
heapq.heappush(heap, 2)
heapq.heappush(heap, 3)

# Check minimum element
heap[0] # peek top heap[0] to get the min value, just read, no restructuring, so its O(1)

# Pop minimum element
heapq.heappop(heap) # 1

# Get size
len(heap) # 2

# Bonus: convert a list to a heap in linear time
heap = [67, 341, 234, -67, 12, -976]
heapq.heapify(heap)

heapq.heappush(heap, 7451)
heapq.heappush(heap, -5352)

# The numbers will be printed in sorted order
while heap:
	# the heapq.heappop(heap) will always return the min one, but does not mean the heap is sorted. 
	# it will sifting the tree strcture and move the next min value to the top of tree.
    print(heapq.heappop(heap)) # O(log n)
    
# Now, you can use heappush and heappop on nums
# and nums[0] will always be the minimum element
```

## How to get a max heaps
```python
import heapq

nums = [3, 1, 5, 7, 2]
max_heap = []

# push (invert values)
for n in nums:
    heapq.heappush(max_heap, -n)

# pop (invert back)
while max_heap:
    print(-heapq.heappop(max_heap))
```

## One simple problem and solution: [1046. Last Stone Weight](https://leetcode.com/problems/last-stone-weight/)

The problem
```text
You are given an array of integers `stones` where `stones[i]` is the weight of the `ith` stone.
We are playing a game with the stones. On each turn, we choose the **heaviest two stones** and smash them together. Suppose the heaviest two stones have weights `x` and `y` with `x <= y`. The result of this smash is:

- If `x == y`, both stones are destroyed, and
- If `x != y`, the stone of weight `x` is destroyed, and the stone of weight `y` has new weight `y - x`.

At the end of the game, there is **at most one** stone left.

Return _the weight of the last remaining stone_. If there are no stones left, return `0`.

**Example 1:**
**Input:** stones = [2,7,4,1,8,1]
**Output:** 1
**Explanation:** 
We combine 7 and 8 to get 1 so the array converts to [2,4,1,1,1] then,
we combine 2 and 4 to get 2 so the array converts to [2,1,1,1] then,
we combine 2 and 1 to get 1 so the array converts to [1,1,1] then,
we combine 1 and 1 to get 0 so the array converts to [1] then that's the value of the last stone.

**Example 2:**
**Input:** stones = [1]
**Output:** 1

**Constraints:**

- `1 <= stones.length <= 30`
- `1 <= stones[i] <= 1000`
```

```python
import heapq

class Solution:
	def lastStoneWeight(self, stones: List[int]) -> int:
		"""
			Space Complexity: O(1), the stones is modified in place. and space complexity typically measures
			extra space allocated beyong the input 
			Time Complexity: O(n log n)
				- heapify: O(n)
				- while: loop runs at most n-1 times, each with O(log n) push/pop
				- overall: O(n log n)
		"""
		stones = [-s for s in stones]
		# turns an array into a heap in inear time O(n)
		heapq.heapify(stones) 
		while len(stones) > 1:
			fisrt = heapq.heappop(stones)
			second = heapq.heappop(stones)
			if first != second:
				heapq.heappush(stones, -abs(first - second))
				
		return -stones[0] if stones else 0

```

# Note


# Reference

