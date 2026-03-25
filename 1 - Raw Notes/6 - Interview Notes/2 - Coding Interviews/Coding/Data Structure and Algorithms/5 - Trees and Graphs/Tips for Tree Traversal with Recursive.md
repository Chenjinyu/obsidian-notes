---
sr-due: <% tp.date.now("YYYY-MM-DD") %>
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-03-24
Course:
Tags: 

# Content

Great example to learn from. Let me break down the thinking process.

**The two questions to ask for any recursive tree function:**
### **1. What is the base case? (when to stop)** 
### **2. What does this function return / do for a single node?**

---

## **Base case first:**
Ask yourself — _"what is the smallest valid input where the answer is obvious?"_

For max depth:

- An empty tree (`None`) has depth `0` — that's your exit

```python
if not root:
    return 0
```

For most tree problems the base case is either:

- `if not root: return 0` (for counting/depth problems)
- `if not root: return None` (for search problems)
- `if not root.left and not root.right: return ...` (leaf node problems)

---

## **Then define what the function means for one node:**

Ask — _"if I trust that my recursive calls give me the correct answer for the left and right subtrees, what do I do with those results at the current node?"_

For max depth:

- Left subtree gives me its depth
- Right subtree gives me its depth
- Current node adds `1` to the deeper side

```python
left = self.maxDepth(root.left)   # trust this is correct
right = self.maxDepth(root.right) # trust this is correct
return max(left, right) + 1
```

This mindset — **trust the recursion, don't trace it** — is the key. You don't need to mentally simulate the whole call stack. Just define what's correct for the current node assuming children are already solved.

---

## **The general template:**

```python
def solve(node):
    # 1. base case — exit
    if not node:
        return <base_value>
    
    # 2. recurse on children — trust the results
    left = solve(node.left)
    right = solve(node.right)
    
    # 3. combine results for current node
    return <something with left, right, node.val>
```

Almost every tree problem fits this shape. What changes is just step 3 in above example.

# Note


# Reference

