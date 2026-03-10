---
sr-due: 2026-03-12
sr-interval: 3
sr-ease: 250
---
Date: 2026-03-01
Course:
Tags: 


# Content

#review

**Time Complexity Comparison:**

|Algorithm|Best|Average|Worst|Space|Stable|
|---|---|---|---|---|---|
|Radix Sort|O(nk)|O(nk)|O(nk)|O(n+k)|✅|
|Counting Sort|O(n+k)|O(n+k)|O(n+k)|O(k)|✅|
|Merge Sort|O(n log n)|O(n log n)|O(n log n)|O(n)|✅|
|Heap Sort|O(n log n)|O(n log n)|O(n log n)|O(1)|❌|
|Quick Sort|O(n log n)|O(n log n)|O(n²)|O(log n)|❌|
|Tim Sort|O(n)|O(n log n)|O(n log n)|O(n)|✅|
|Shell Sort|O(n log n)|O(n log^2 n)|O(n²)|O(1)|❌|
|Bubble Sort|O(n)|O(n²)|O(n²)|O(1)|✅|
|Insertion Sort|O(n)|O(n²)|O(n²)|O(1)|✅|
|Selection Sort|O(n²)|O(n²)|O(n²)|O(1)|❌|

---

**Ranked most → least popular in practice:**

```
1. Tim Sort      ← Python's built-in sort(), most used in real world
2. Quick Sort    ← most taught, used in many standard libraries
3. Merge Sort    ← fundamental, used in databases, external sorting
4. Heap Sort     ← used in priority queues
5. Insertion Sort← used for small arrays, also used inside Tim Sort
6. Radix Sort    ← used for integers/strings at scale
7. Counting Sort ← used when range of values is known/small
8. Shell Sort    ← improved insertion sort, rarely used today
9. Bubble Sort   ← mostly teaching purposes only
10. Selection Sort← mostly teaching purposes only
```

---

**When to use each:**

```
Small arrays (<20 elements)     → Insertion Sort
General purpose                 → Tim Sort / Quick Sort
Guaranteed O(n log n)           → Merge Sort
Memory constrained              → Heap Sort
Integers with known range       → Counting Sort / Radix Sort
Nearly sorted data              → Insertion Sort / Tim Sort
Linked lists                    → Merge Sort
```

---

**Key takeaways:**

- **Tim Sort** is the most practical — it's a hybrid of Merge Sort + Insertion Sort, used by Python, Java, and Android
- **Quick Sort** is fastest on average in practice despite O(n²) worst case
- **Bubble/Selection Sort** are only useful for learning concepts
- **Radix/Counting Sort** can beat O(n log n) but only work on specific data types

# Note


# Reference

