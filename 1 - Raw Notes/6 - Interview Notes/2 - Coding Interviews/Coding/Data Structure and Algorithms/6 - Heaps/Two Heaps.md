---
sr-due: 2026-04-19
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-04-14
Course:
Tags: [[Heaps]] [[Two Heaps]]

# Content
Two-heaps is one of those patterns that _looks niche but shows up a lot_—especially when companies want to test <span style="color:orange">streaming logic + data structure discipline.</span>

# 🧠 What “two heaps” is really testing

At its core, interviewers are checking if you can:
- Maintain a **dynamic median or split**
- Keep **two balanced partitions**
- Reason about **invariants under insert/delete**
    
Typical setup: check out [[Two Hapes - Max and MIn]]
- **Max heap (left)** → smaller half
- **Min heap (right)** → larger half
---
# ⚠️ What you MUST get right (this is where people fail)
## 1. Heap roles (don’t mix them up)
- Left = max heap (store negatives in Python)
- Right = min heap
If you mess this up → everything breaks.
## 2. Invariant (non-negotiable)
You must always maintain:
```text
len(left) == len(right)
OR
len(left) == len(right) + 1
```
👉 Left can be 1 bigger (for median)
## 3. Order property
```text
max(left) <= min(right)
```
If violated → rebalance
## 4. Insert logic (this is the pattern)
Never improvise. Use a fixed flow:
```python
if not left or num <= -left[0]:
    push to left
else:
    push to right

rebalance()
```
## 5. Rebalancing (most common bug)
```python
if len(left) > len(right) + 1:
    move left → right
elif len(right) > len(left):
    move right → left
```
## 6. Median retrieval
```python
if odd:
    return -left[0]
else:
    return (-left[0] + right[0]) / 2
```
## 7. Python trap (important)
Python only has min heap (`heapq`)
👉 Max heap = push negative values
## 8. Deletion (hard mode problems)
This is where candidates collapse.
You need:
- **lazy deletion (hash map)**
- or **indexed heap**
Used in:
- sliding window median
# 📊 How often does it show up?
Honest answer:
- 🔹 ~5–10% of interviews (mid-level SWE)
- 🔹 ~15% at companies that like data structures (Google, Meta, etc.)
- 🔹 VERY likely if:
    - streaming data
    - median
    - “kth” dynamic updates

👉 Not the most common pattern, but **high signal when it appears**
# 🔥 Top 10 Two-Heaps LeetCode Problems

These are the ones that actually matter:
## 🟢 Core (you must know these)
1. **Find Median from Data Stream**
    - THE canonical problem
    - If you know only one → this
2. **Sliding Window Median**
    - Adds deletion → real difficulty
    - Interview gold
3. **IPO**
    - Two heaps for greedy selection
4. **Reorganize String**
    - Heap + greedy, sometimes dual heap logic
## 🟡 Medium-level extensions
5. **Top K Frequent Elements**
    - Not strictly two heaps, but heap pattern
6. **Kth Largest Element in a Stream**
    - Variant of streaming heap logic
7. **Last Stone Weight**
    - Heap fundamentals (build intuition)
## 🔴 Advanced / less obvious two-heap usage
8. **Minimum Cost to Hire K Workers**
    - Heap + greedy combo
9. **Meeting Rooms II**
    - Min heap scheduling (related pattern)
10. **Smallest Range Covering Elements from K Lists**
- Multi-heap coordination
# 🎯 What you should actually do (practical advice)
Don’t try to memorize 10 problems.
Do this instead:
### Step 1 (mandatory)
- Master **Median from Data Stream**
- Be able to code it in **10 minutes clean**
### Step 2
- Do **Sliding Window Median**
- Understand **lazy deletion deeply**
### Step 3
- Do 2–3 heap + greedy problems (IPO, Hiring Workers)

# 🚨 Reality check
Most candidates:
- Understand heaps ❌
- Fail at **balancing logic** ❌
- Completely break on **deletion** ❌
If you can:
- cleanly maintain invariants
- explain why rebalance works
👉 You’re already above average.

# Note


# Reference

