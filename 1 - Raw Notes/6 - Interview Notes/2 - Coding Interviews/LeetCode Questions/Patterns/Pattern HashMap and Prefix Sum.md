---
sr-due: 2026-03-14
sr-interval: 1
sr-ease: 2.5
---
# Reference
- [[../0525. Contiguous Array|0525. Contiguous Array]]
- [[../0560. Subarray Sum Equals K (M)|0560. Subarray Sum Equals K (M)]]
- [[../0974. Subarray Sums Divisible by K|0974. Subarray Sums Divisible by K]]
- [[../1248. Count Number of Nice Subarrays|1248. Count Number of Nice Subarrays]]
- [[../2342. Max Sum of a Pair With Equal Sum of Digits|2342. Max Sum of a Pair With Equal Sum of Digits]]
- 

# The criteria to meet the pattern
```text
1. Count the number of subarrays (NOTE: it's not get the sub-array)
2. The problem involves a target condition on subarray sum:
   - exact sum == k          (LC 560)
   - exact odd count == k    (LC 1248)
   - sum divisible by k      (LC 974)
3. The subarray sum can be expressed as a gap between two prefix sums:
   prefix_sum[j] - prefix_sum[i] = k
   → rearranges to: prefix_sum[i] = prefix_sum[j] - k
   → so you look up (curr - k) in the hashmap
4. Elements can be negative or zero (sliding window breaks down,
   prefix sum + hashmap handles it)
```

# The template
```python
pref_sum = {0: 1}   # seed: one left boundary before the array, Without it, you'd miss all subarrays that start from index 0.
# because the ans is be added before the prefix[] += 1
curr = 0
ans = 0

for num in nums:
    curr += transform(num)          # e.g. num, num%2, num%k
    ans += pref_sum[curr - k]       # look up left boundary
    pref_sum[curr] += 1             # store current checkpoint
```

# The transform step by problem
```text
- LC 560  : transform(num) = num        (raw value)
- LC 1248 : transform(num) = num % 2   (odd=1, even=0)
- LC 974  : transform(num) = num % k   (remainder)
```