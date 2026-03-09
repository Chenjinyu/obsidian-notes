Date: 2026-01-26
Course:
Tags: [Interview] 

# Content
In python: 
Bitwise XOR
3 ^ 2 （异或关系）bitwise XOR。 相同则0，不同则1
```
  0011
^ 0010 
  ----
  0001
```
in math
A⊕B
True when **exactly one of A or B is 1 then** is 1.

| A   | B   | A XOR B |
| --- | --- | ------- |
| 0   | 0   | 0       |
| 0   | 1   | 1       |
| 1   | 0   | 1       |
| 1   | 1   | 0       |

-----

5 & 3 Bitwise AND. 相同则1，不同则0
```
  101
& 011
-----
  001  -> 1
```
in math: 
5 ∧ 3, eg 1 ∧ 1 = 1 otherwise 0

----

5 | 3 Bitwise OR, Result bit is `1` if **either** bit is 1 每个位数上去最大值
```  
  101
| 011
-----
  111  -> 7
```
in math:
1∨0=1, is 1 if has 1, otherwise is 0

-----

~5: Bitwise Not: Flips all bits (two’s complement!)
```
~00000101 = 5 decimal
= 11111010
```

<< Left Shift: moves the binary representation of a number to the left by a specified number of positions, filling vacated bits with zeros.
```
eg: a << b = a ** 2^b (in math) = a * 2**2
5 << 1
0101 << 1= 1010 = 10
or 5 * 2 ** 1 = 10
```
in math:
5 x 2的一次方
##  >> Right Shift: shift bits right, 
```
5 >> 1
0101 >> 1 ** 2 = 0010 = 2
```
in math
5 / 2 的一次方
x >> n 等于 x除以2的n次方

# Note
hexadecimal：十六进制
decimal： 十进制
binary： 二进制
exponential: 指数
# Reference

