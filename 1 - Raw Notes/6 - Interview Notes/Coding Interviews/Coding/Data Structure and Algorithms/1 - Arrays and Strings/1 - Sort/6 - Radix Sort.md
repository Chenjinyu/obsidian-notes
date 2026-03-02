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

nums = [12,23,135,1567,115]
transfer_nums = [] * len(nums)
radix_array = [[]] * 10

for idx in range(len(nums)):
	last_digit, remaining = nums[idx] % 10, nums[idx] // 10
	
	if last_digit != 0:
		

```
# Note


# Reference

