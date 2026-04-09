---
sr-due: 2026-04-11
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-04-09
Course:
Tags: 

# Content
Here are **10 popular LeetCode problems that use the Multi‑Source BFS pattern**, based on common interview patterns and widely referenced problem lists online. These are all well‑known problems where you **start BFS from multiple sources simultaneously** to compute minimum distances or simulate spreading processes. 

---

# 🔟 **Top 10 Multi‑Source BFS LeetCode Problems**

### **1. 994. Rotten Oranges**  
The classic multi‑source BFS example. All rotten oranges start as sources and spread simultaneously.

### **2. 542. 01 Matrix**  
Compute the distance of each cell to the nearest 0. All 0‑cells are BFS sources.

### **3. 286. Walls and Gates**  
All gates (value 0) are sources; BFS fills in minimum distances to each room.

### **4. 1293. Shortest Path in a Grid with Obstacles Elimination**  
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

| Pattern | Key Idea |
|--------|----------|
| **Spreading** | BFS simulates time steps |
| **Nearest Source** | BFS computes minimum distance |
| **State-space** | BFS explores multiple initial states |
| **Multi-entrance maze** | BFS from all entrances at once |

# Note


# Reference

