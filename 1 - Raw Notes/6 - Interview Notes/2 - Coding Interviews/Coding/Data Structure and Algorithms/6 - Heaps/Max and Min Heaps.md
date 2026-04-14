---
sr-due: <% tp.date.now("YYYY-MM-DD") %>
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-04-14
Course:
Tags: 

# 🧪 Quick code demo
```python
import heapq

left = []   # max heap (negatives)
right = []  # min heap

def add(num):
    if not left or num <= -left[0]:
        heapq.heappush(left, -num)
    else:
        heapq.heappush(right, num)

    # rebalance
    if len(left) > len(right) + 1:
        heapq.heappush(right, -heapq.heappop(left))
    elif len(right) > len(left):
        heapq.heappush(left, -heapq.heappop(right))
```

# 🎯 Goal of two heaps
We want to split numbers into two halves:
```text
Left (max heap)   |   Right (min heap)
smaller numbers   |   larger numbers
```
👉 So we can quickly get the **median**

# ⚠️ Problem: Python has NO max heap
Python only has a **min heap** (`heapq`).
So we fake a max heap by storing **negative values**.
# 🔥 Example (step-by-step)
Let’s insert numbers:
```text
[5, 2, 8]
```

## Step 1: Insert 5
We put it in left (max heap):
```python
left = [-5]   # store negative!
right = []
```
Interpretation:
```text
Left = [5]
Right = []
```
## Step 2: Insert 2
Compare with max of left:
```python
2 <= 5 → goes to left
```
```python
left = [-5, -2]
right = []
```
But now it's unbalanced → move largest from left → right
```python
move 5 to right
```
Final:
```python
left = [-2]
right = [5]
```
Interpretation:
```text
Left = [2]
Right = [5]
```
## Step 3: Insert 8
```python
8 > 2 → goes to right
```

```python
left = [-2]
right = [5, 8]
```
Unbalanced → move smallest from right → left
```python
move 5 to left
```

Final:
```python
left = [-5, -2]
right = [8]
```
Interpretation:
```text
Left = [5, 2]   ← max heap (largest = 5)
Right = [8]     ← min heap (smallest = 8)
```
# 🧠 Key insight (THIS is what you need to remember)
## Why left = max heap?
Because we need:
```text
max(left) ≤ min(right)
```
So:
- Left keeps track of the **largest of the smaller half**
- Right keeps track of the **smallest of the larger half**

# ⚡ Why negatives?
Because Python’s heap always gives the **smallest**:
```python
import heapq

heap = []
heapq.heappush(heap, -5)
heapq.heappush(heap, -2)

heap[0]  # = -5
```
Convert back:
```python
-max = 5
```
👉 That’s your “max heap”
# 📊 Visual intuition
Think of it like this:
```text
          median
            |
   [2, 5]   |   [8]
    left    |   right
```

- Left top = 5
- Right top = 8
# 🚨 The mistake people make

They try:
```text
left = min heap
right = min heap
```
👉 Then you lose control of the boundary → median breaks

---

# ✅ Bottom line
- Left = **max heap** → store negatives
- Right = **min heap**
- Left holds **smaller half**
- Right holds **larger half**
    
If you want, I can walk you through **one full median problem execution line-by-line**—that’s where this really locks in.

# Note


# Reference

