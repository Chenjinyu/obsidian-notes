---
sr-due: 2026-06-07
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-04-17
Course:
Tags: 
#review #review/3d #review/15d 

# Review dates
- 05/22/2026
- 
# 💥 Key takeaway from code
- Greedy = **one path, no correction**, **make the locally optimal choice at each step and never look back**
- DP = **many paths, keeps best**

👉 The real skill:
> Knowing when greedy breaks—and switching to DP fast.
# Greedy vs DP

#### 1. Dynamic Programmin
- Solves problems by breaking them into overlapping sub-problems
- Stores results (Memoization / table)
- Guarantees global optimal solution
👉 Think: _“I’ll explore all possibilities, but efficiently.”_
#### 2. Greedy
- Makes the best choice at the current step
- Never revisits decisions
- Works only if local optimal = global optimal
👉 Think: _“I’ll pick what looks best right now and trust it works out.”_
## 🧩 How to recognize which to use
### Use Greedy if:
- You can prove:
    > “A local best choice always leads to global best”
- Typical patterns:
    - sorting + picking
    - intervals
    - minimum spanning tree (Kruskal, Prim)
    - shortest path (Dijkstra — with constraints)
### Use DP if:
- Problem says:
    - “number of ways”
    - “minimum/maximum”
- And:
    - choices depend on previous results
    - overlapping subproblems exist
👉 Examples:
- Climbing stairs
- Knapsack
- Unique paths

## 💡 Example that exposes the difference

### Coin Change (classic trap)
Coins: `[1, 3, 4]`, target = `6`
#### Greedy approach:
- Pick largest coin first → `4`
- Remaining = `2` → `1 + 1`
- Result = **3 coins**
#### DP approach:
- Finds optimal: `3 + 3`
- Result = **2 coins**

👉 Greedy **fails**, DP **wins**

## 🎯 Problem Example to Explain the difference
```
it has cons = [1,3,4], to get the mim number of cons to count up to target = 6
```

### 1. Greedy Approach (can fail)
```python

def coin_change_greedy(coins, amount):
	"""
	Greedy thinking:
		“Take the biggest coin first”
		→ Fast, but blind to future consequences
	"""
    coins.sort(reverse=True)  # largest first
    count = 0

    for coin in coins:
        if amount == 0:
            break
        num = amount // coin
        count += num
        amount -= num * coin

    return count if amount == 0 else -1

print(coin_change_greedy([1, 3, 4], 6))  # ❌ Output: 3
```
#### What it does:
- Picks `4` first → remaining `2`
- Then `1 + 1`
- Total = **3 coins**
👉 Looks smart locally, but misses the optimal.
### 2. Dynamic Programming (Correct)
```python
def coin_change_dp(coins, amount):
	"""
	DP thinking:
		“What’s the best way to make every amount up to 6?”
		→ Builds knowledge → guarantees optimal
	"""
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1

print(coin_change_dp([1, 3, 4], 6))  # ✅ Output: 2
```
#### What it does:
- Tries **all combinations efficiently**
- Builds from smaller amounts → larger
- Finds: `3 + 3 = 2 coins`
# Note


# Reference

