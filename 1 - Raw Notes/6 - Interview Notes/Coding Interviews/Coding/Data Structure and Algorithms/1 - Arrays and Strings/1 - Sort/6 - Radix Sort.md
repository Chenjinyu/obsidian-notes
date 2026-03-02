Date: 2026-02-26
Course: https://www.w3schools.com/dsa/dsa_algo_radixsort.php
Tags: [[W3Schools]] [[Arrary]] [[Sort]]

# Content

The Radix Sort algorithm sorts an array by individual digits, starting with the least significant digit (the rightmost one).

The radix (or base) is the number of unique digits in a number system. In the decimal system we normally use, there are 10 different digits from 0 till 9.

Radix Sort uses the radix so that decimal values are put into 10 different buckets (or containers) corresponding to the digit that is in focus, then put back into the array before moving on to the next digit.

##### Radix Sort is a non comparative algorithm that only works with non negative integers.

### **How it works:**
1. Start with the least significant digit (rightmost digit).
2. Sort the values based on the digit in focus by first putting the values in the correct bucket based on the digit in focus, and then put them back into array in the correct order.
3. Move to the next digit, and sort again, like in the step above, until there are no digits left.

```python
from typing import List

nums = [12,23,135,1567,119]

def radix_array(nums: List) -> List:
	"""
	Time complexity: O(n * k), where n is the number of elements in the input list and k is the number of digits in the largest number.

	Space complexity: O(n + k), where n is the number of elements in the input list and k is the number of digits in the largest number (for the buckets).
	"""
    max_digits = max([len(str(x)) for x in nums]) # O(n)
        
    def sort_by_digit(nums, digit_pos):
        # cannot create the radix_array with [[]] * 10, because each sub list will assign to the first sublist at the same time
        buckets = [ [] for _ in range(10) ] # 0-9
        for num in nums:
            digit = (num // digit_pos) % 10
            buckets[digit].append(num)
        result = []
        for bucket in buckets:
            result.extend(bucket)
        return result
    
    digit_pos = 1
    for _ in range(max_digits):
        nums = sort_by_digit(nums, digit_pos)
        digit_pos *= 10
    return nums	

```
# Note


# Reference

