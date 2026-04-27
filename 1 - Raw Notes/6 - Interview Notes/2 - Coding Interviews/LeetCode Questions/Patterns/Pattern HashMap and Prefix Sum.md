---
sr-due: 2026-05-09
sr-interval: 1
sr-ease: 2.5
---
# Reference
- [[../M - 1248. Count Number of Nice Subarrays|M - 1248. Count Number of Nice Subarrays]]
- [[../M - 0974. Subarray Sums Divisible by K|M - 0974. Subarray Sums Divisible by K]]
- [[../M - 0560. Subarray Sum Equals K|M - 0560. Subarray Sum Equals K]]
- [[../M - 0525. Contiguous Array|M - 0525. Contiguous Array]]
- [[../M - 2342. Max Sum of a Pair With Equal Sum of Digits|M - 2342. Max Sum of a Pair With Equal Sum of Digits]]

## Why ans += prefix[gap] in above references?

```python
ans += prefix[gap]
# IS NOT 
ans += 1
```
### Example with example from [[../M - 0560. Subarray Sum Equals K|M - 0560. Subarray Sum Equals K]]
```text
04/04/2026
nums =   [1, 2, 3, 6, -6, 6, -6, 5, 1] 
idx =     0   1  2  3  4  5   6  7  8
prefix = [0, 1, 3, 6, 12, 6, 12, 6, 11, 12] 
k = 6
I was thinking the ans += prefix[gap] should change to ans = prefix[gap] + 1.
actually, I was wrong, because when iterate to i = 5, the prefix[6] = 2, means when nums[5]=6, it has 2 sub_array matches. 
and includes when i = 3's subarray to when i = 5's subarrary
                  [6]                      [6,-6,6], the first 6 to be included to new sub-array. 

i=3: num=6,  cur_sum=12, gap=6  → prefix_sum[6]=1 → count+=1 → count=2
     prefix_sum = {0:1, 1:1, 3:1, 6:1, 12:1}
     matched:
         prefix was 6 at i=2 → [6]

i=5: num=6,  cur_sum=12, gap=6  → prefix_sum[6]=2 → count+=2 → count=5
     prefix_sum = {0:1, 1:1, 3:1, 6:2, 12:2}
     matched:
         prefix was 6 at i=2 → [6,-6,6] <- the first 6 already count when i = 3
         prefix was 6 at i=4 → [6]

i=8: num=1,  cur_sum=12, gap=6  → prefix_sum[6]=3 → count+=3 → count=9
     prefix_sum = {0:1, 1:1, 3:1, 6:3, 11:1, 12:3}
     matched:
         prefix was 6 at i=2 → [1,2,3]
        [6,-6,6,-6,5,1] <- the first 6 already count then i = 3
                        <- the [6,-6,6] already count when i = 5 
                        <- the last one positive [6] already count when i = 5
         prefix was 6 at i=4 → [6,-6,5,1]
         prefix was 6 at i=6 → [5,1]
```
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