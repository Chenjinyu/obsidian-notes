---
sr-due: 2026-04-12
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-04-09
Course:
Tags: 

# Content

# 🧠 Single-source vs Multi-source BFS

| Category                     | Single-source BFS                              | Multi-source BFS                                 |
| ---------------------------- | ---------------------------------------------- | ------------------------------------------------ |
| **Definition**               | Start BFS from **one node**                    | Start BFS from **multiple nodes simultaneously** |
| **Queue Initialization**     | `queue = [start]`                              | `queue = [s1, s2, s3, ...]`                      |
| **Goal**                     | Find shortest path **from one node to others** | Find shortest distance **to the nearest source** |
| **Direction (mental model)** | From source → outward                          | From all sources → outward (covers space)        |
| **Typical Question Pattern** | “Shortest path from A”                         | “Nearest / closest / minimum distance to X”      |
| **Distance Meaning**         | Distance from the starting node                | Distance to the closest source                   |
| **Number of BFS runs**       | Usually **1 BFS**                              | Still **1 BFS** (not multiple!)                  |
| **Performance impact**       | Efficient                                      | Avoids repeated BFS → much more efficient        |
| **Common mistake**           | N/A                                            | People incorrectly run BFS from each node        |
| **Parallel expansion**       | Yes (level-order BFS)                          | Yes (but from multiple starting points)          |
| **State transition**         | `dist[next] = dist[curr] + 1`                  | Same                                             |
| **Visited logic**            | Mark visited when pushed                       | Same                                             |
| **Graph requirement**        | Unweighted graph                               | Unweighted graph                                 |
| **Complexity**               | O(V + E)                                       | O(V + E)                                         |
| **When to use**              | One fixed starting point                       | Multiple “target” nodes or sources               |
| **Key optimization idea**    | Standard BFS                                   | Reverse thinking: let sources expand             |

# ✅ What’s the SAME (important)

| Aspect           | Both BFS types                    |
| ---------------- | --------------------------------- |
| Traversal style  | Level-order (layer by layer)      |
| Data structure   | Queue                             |
| Distance update  | `+1 per level`                    |
| Guarantees       | Shortest path in unweighted graph |
| Complexity       | O(V + E)                          |
| Visited handling | Prevent revisits                  |
# 🔥 What’s DIFFERENT (core insight)

| Core Difference     | Explanation                                                                                                                                                                                    |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Starting points     | One vs many                                                                                                                                                                                    |
| Problem perspective | From source → others vs To nearest source (思考的方向不一样，Single Source从自身出发去寻找，Multi-source 向外搜寻任何可能的节点再与自身比较)， both them are outward to explore, but the comparison stands on opposite directions. |
| Thinking direction  | Forward search vs “reverse” thinking                                                                                                                                                           |
| Use case trigger    | “from A” vs “nearest / closest / minimum distance to any”                                                                                                                                      |
# 🧠 One-line mental model

* **Single-source BFS** → *“How far is everything from me?”*
* **Multi-source BFS** → *“How far am I from the nearest of them?”*

---
# Steps with the Multi-Source BFS
## 🎯 **What This Demonstrates About Multi‑Source BFS**

### ✔ All fire sources start at distance 0  
### ✔ BFS expands in perfect “waves”  
### ✔ Each wave represents 1 time unit  
### ✔ All sources spread simultaneously 
### ✔ The queue always contains the current wave  
### ✔ The algorithm naturally finds the minimum time to reach each cell  

## 🔥 The Key Principle of Multi‑Source BFS
- **All sources spread simultaneously.**  
- Each BFS wave expands from *every* source in the queue.

```text
1. My understanding of simultaneously
eg: first time, append (1,1), (2,3) to the queue, in the while loop, we defined the two nodes are the frist time processed, it's like simultaneously, but it's not really processing at the exactally the same time. the (1,1) popleft first, and append its childrend to queue, the (2,3) popleft after (1,1), and append its childrend after (1,1)'s children.
eg. [[../M - 0542. 01 Matrix|M - 0542. 01 Matrix]], which has multi nodes(sources) are loaded into queue in the first time

2. Even like [[../H - 1293. Shortest Path in a Grid with Obstacles Elimination|H - 1293. Shortest Path in a Grid with Obstacles Elimination]], the first time, only (0,0) loaded, but its children will be proceseed "simultaneously"

```

## 📌 Results in each wave

### 1. Initial Grid (wave 0)
Fire at `(1,1)` and `(2,3)`:
the fire is 0s, the ∞ s are unvisited lands
```
∞   ∞   ∞   ∞
∞   0   ∞   ∞
∞   ∞   ∞   0
∞   ∞   ∞   ∞
```

Queue:
```
[(1,1), (2,3)]
```

### 2. 🌊 Wave 1 — Spread from BOTH sources
Neighbors of `(1,1)` catch fire:
```
(1,0), (1,2), (0,1), (2,1)
```

Neighbors of `(2,3)` catch fire:
```
(2,2), (1,3), (3,3)
```

So Wave 1 should be:
```
∞   1   ∞   ∞
1   0   1   1
∞   1   1   0
∞   ∞   1   1
```
### # 🌟 Why this happens
Because BFS processes the queue like this:
```
Wave 0 queue: [(1,1), (2,3)]
```
When we expand Wave 1:
- We pop `(1,1)` → ignite its neighbors  
- We pop `(2,3)` → ignite its neighbors  

### 🌊 **Wave 2 — Fire spreads again**

Now BFS expands from *all* distance‑1 cells in parallel.
```
2   1   2   ∞
1   0   1   2
2   1   2   0
∞   2   1   2
```
Cells at distance 2 catch fire.
### 🌊 **Wave 3 — Next layer**
```
2   1   2   3
1   0   1   2
2   1   2   0
3   2   1   2
```
### 🔥 **Final Distance Matrix (Fire Spread Time)**
```
2 1 2 3
1 0 1 2
2 1 2 0
3 2 1 2
```

Each number tells you: <span style="color:orange">**How many steps until fire reaches that cell.**</span>


So if you have two fire cells, both ignite their neighbors **in the same wave**.

This is exactly the same pattern used in:
- **01 Matrix**  
- **Rotting Oranges**  
- **Walls and Gates**  
- **Map of Highest Peak**  
- **As Far From Land As Possible**  

### Leetcode [[../M - 0542. 01 Matrix|M - 0542. 01 Matrix]] is the good example

Here are **10 popular LeetCode problems that use the Multi‑Source BFS pattern**, based on common interview patterns and widely referenced problem lists online. These are all well‑known problems where you **start BFS from multiple sources simultaneously** to compute minimum distances or simulate spreading processes. 

---

# 🔟 **Top 10 Multi‑Source BFS LeetCode Problems**

### **1. 994. Rotten Oranges**  
The classic multi‑source BFS example. All rotten oranges start as sources and spread simultaneously.

### **2. [[../M - 0542. 01 Matrix|M - 0542. 01 Matrix]]
Compute the distance of each cell to the nearest 0. All 0‑cells are BFS sources.

### 3.  **[[../M - 0286. Walls and Gates|M - 0286. Walls and Gates]]
All gates (value 0) are sources; BFS fills in minimum distances to each room.

### **4. [[H - 1293. Shortest Path in a Grid with Obstacles Elimination]] 
Often solved with BFS + state, but multi‑source BFS variants appear in optimized solutions.

### **5. 1765. Map of Highest Peak**  
All water cells start as sources; BFS grows land heights outward.

### **6. 1162. As Far from Land as Possible**  
All land cells are sources; BFS finds the farthest water cell.

### **7. 847. Shortest Path Visiting All Nodes**  
Uses BFS with bitmask; multi‑source initialization from all nodes.

### **8. 317. Shortest Distance from All Buildings**  
Each building is a source; multi‑source BFS is used repeatedly.

### **9. 490. The Maze II** (and similar maze problems)  
Some variants use multi‑source BFS when starting from multiple entry points.

### **10. 773. Sliding Puzzle**  
State‑space BFS; multi‑source BFS appears in generalized puzzle variants.

---
# ⭐ Why these are considered “multi‑source BFS”  
Multi‑source BFS is used when:
- You have **multiple starting points** (e.g., all rotten oranges, all gates, all land cells).  
- You want to compute **minimum distance to the nearest source**.  
- You want to simulate **simultaneous spreading** (infection, fire, water, etc.).  
- You want to avoid running BFS **k times** (one per source), and instead run **one BFS** with all sources in the queue initially.

---
# 🧩 **1. Multi‑Source BFS Patterns (Grouped)**

## **A. “Spreading / Infection / Propagation” Problems**  
These simulate something spreading outward at the same speed from multiple starting points.

| Problem | What spreads? | Sources |
|--------|----------------|---------|
| **994. Rotten Oranges** | Rot spreads | All rotten oranges |
| **1765. Map of Highest Peak** | Height grows | All water cells |
| **1162. As Far from Land as Possible** | Distance from land | All land cells |

**Pattern:**  
Start BFS from all initial “active” cells → expand outward → track time/distance.

## **B. “Nearest Source / Distance Transform” Problems**  
Compute the shortest distance to the nearest special cell.

| Problem | Goal | Sources |
|--------|------|---------|
| **542. 01 Matrix** | Distance to nearest 0 | All 0s |
| **286. Walls and Gates** | Distance to nearest gate | All gates |
| **317. Shortest Distance from All Buildings** | Distance to buildings | All buildings (run BFS per building or optimized multi-source variants) |

### **Pattern:**  
Push all special cells (0s, gates, buildings) into the queue → BFS fills distances.

## **C. “State‑Space Multi‑Start” Problems**  
These are not grid-based but use BFS from multiple states.

| Problem                                   | Why multi-source?                            |
| ----------------------------------------- | -------------------------------------------- |
| **847. Shortest Path Visiting All Nodes** | BFS starts from every node (bitmask)         |
| **773. Sliding Puzzle**                   | BFS over states; multi-source variants exist |
|                                           |                                              |
### **Pattern:**  
Initialize BFS with multiple starting states → explore state graph.

## **D. “Maze / Grid with Multiple Entrances” Problems**  
Sometimes you start BFS from all entrances simultaneously.

| Problem | Why multi-source? |
|--------|--------------------|
| **490. The Maze II** | Some variants start from all possible start points |

### **Pattern:**  
Push all valid starting positions → BFS to compute shortest reachability.

---

# ⭐ Summary of Patterns

| Pattern                 | Key Idea                             |     |
| ----------------------- | ------------------------------------ | --- |
| **Spreading**           | BFS simulates time steps             |     |
| **Nearest Source**      | BFS computes minimum distance        |     |
| **State-space**         | BFS explores multiple initial states |     |
| **Multi-entrance maze** | BFS from all entrances at once       |     |

# Note


# Reference

