Date: 2026-02-26
Course: https://www.w3schools.com/dsa/dsa_algo_mergesort.php
Tags: [[W3Schools]] [[Arrary]] [[Sort]]

# Content

The Merge Sort algorithm is a divide-and-conquer algorithm that sorts an array by first breaking it down into smaller arrays, and then building the array back together the correct way so that it is sorted.

**Divide:** The algorithm starts with breaking up the array into smaller and smaller pieces until one such sub-array only consists of one element.

**Conquer:** The algorithm merges the small pieces of the array back together by putting the lowest values first, resulting in a sorted array.

The breaking down and building up of the array to sort the array is done recursively.

In the animation above, each time the bars are pushed down represents a recursive call, splitting the array into smaller pieces. When the bars are lifted up, it means that two sub-arrays have been merged together.

## Here's a simple merge sort example:

**Time complexity:** O(n log n) — splits log n times, each merge is O(n)  
**Space complexity:** O(n) — needs extra space for the merged result

```python
def merge_sort(nums):
    # base case: a single element is already sorted
    if len(nums) <= 1:
        return nums

    # split the list in half
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])   # recursively sort left half
    right = merge_sort(nums[mid:])  # recursively sort right half

    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0

    # compare elements from both halves and merge in sorted order
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # append any remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# Test
nums = [38, 27, 43, 3, 9, 82, 10]
print(merge_sort(nums))  # [3, 9, 10, 27, 38, 43, 82]
```

**How it works visually:**

```
Example of sort first left half:
merge_sort([38, 27, 43])
├── left  = merge_sort([38, 27])
│   ├── left  = merge_sort([38]) → returns [38]  # base case
│   └── right = merge_sort([27]) → returns [27]  # base case
│       └── merge([38], [27]) → returns [27, 38]
└── right = merge_sort([43]) → returns [43]       # base case
    └── merge([27, 38], [43]) → returns [27, 38, 43]
    
[38, 27, 43, 3, 9, 82, 10]
        /               \
  [38, 27, 43]        [3, 9, 82, 10]
    /       \           /          \
[38, 27]  [43]      [3, 9]      [82, 10]
  /    \              /    \      /     \
[38]  [27]          [3]   [9]  [82]   [10]
  \    /              \    /      \     /
[27, 38]             [3, 9]      [10, 82]
        \            /                \
      [27, 38, 43]  [3, 9, 10, 82]
              \         /
        [3, 9, 10, 27, 38, 43, 82] ✅
```



# Note


# Reference

