Date: 2026-02-28
Course: https://docs.python.org/3/howto/regex.html
Tags: 

# Content
## Methods on a match:
- match(): Determine if the RE matches at the beginning of the string
- search(): Scan through a string, looking for any location where this RE matches
- findall(): Find all substrings where the RE matches, and returns them as a list
- finditer(): Find all substrings where the RE matches, and returns them as iterator.

## Modification methods
- split(): Returns a list where the string has been split at each match
- sub(): Replaces one or any matches with a string

## Meta Characters:
```
. ^ $ * + ? { } [ ] \ | ( )
```

`.` Any character (except newline charactor)
`^` starts with "^hello", if inside of [], means "except/negation"
`$` Ends with "world$"
`*` Zero or more occurrences "aix*"
`+` One or more occurrences "aix+"
`{}` Exactly the specified number of occurrences: "al{2}", eg: `all`
`[]` A set of characters "[a-m]" 
`\` Special sequence (or escape special characters), "\d"
`|` Either or "falls|stays"
`()` Capture and group
`P<name>` Named groups `(?P<name>...)` simply give groups an **alias**

```python
# example of ^
import re

text = "hello world"
print(re.findall(r'^hello', text))    # ['hello'] ✅ matches, hello is at start
print(re.findall(r'^world', text))    # []  ❌ no match, world is not at start

print(re.findall(r'[^0-9]+', "abc123"))   # ['abc']  → any char except digits
print(re.findall(r'[^a-z]+', "abcDEF"))   # ['DEF']  → any char except lowercase
```
#### Important — `^` inside `[]` only negates if it's at the START:
```
r'[^abc]'    # negation(noun: 否定) — matches anything EXCEPT a, b, c
r'[a^bc]'    # no negation — matches a, ^, b, or c  (^ is literal here)
```


```python
```python
m = re.match(r'(?P<first>\w+) (?P<last>\w+)', 'Jane Doe')

# All of these work ✅
print(m.groupdict())      # {'first': 'Jane', 'last': 'Doe'}
print(m.group('first'))   # Jane
print(m.group('last'))    # Doe
print(m.group(1))         # Jane
print(m.group(2))         # Doe
print(m.group(0))         # Jane Doe  (entire match)
print(m.group(1, 2))      # ('Jane', 'Doe')  (multiple at once)
```
### Quantifiers:
- `*`: 0 or more
- `+`: 1 or more
- `?`: 0 or 1, -> optional character. eg. r'https?", can be http or https. 
- `{4}`: exact numer  
```
eg. 
1. \d{4}, matches the integer has 4 digits, eg "200200" returns  2002. eg "20020001"  returns 2002 and 0001
2. \d{1,4}. "12345", returns 1234 and 1
3. \d{1,7}. "12345", returns 12345
```
- `{4,6}`: range numbers, from 4 to 6 # eg. \d{2,4}, matches the integers has 2 to 4 digits. eg: 12, 123, 1234

```python
pattern = re.compile(regex_exp)
matches = pattern.finditer(test_string)
for match in matches:
	print(match)
	
test_string = "123abc456abc123.ABC"
regex_exp = r"^abc" # returns abc, matched the abc in the begining of test_string
regex_exp = r"\." # . is metecharacter, needs \ to convert. returns .
regex_exp = r"abc$" # return None, because the `abc` is not at the end of test_string

```
### More metacharacters
`\d`: Matches any decimal digit [0-9]
`\D`: Matches any non-digit character
`\s`: Matches any whitespace character; (space " " tab "\t", newline: "\n")
`\S`: Matches any non-whitespace character. 
`\w`: Matches any alphanumeric character. equivalent to the class [a-zA-Z0-9_]
`\W`: Matches any non-alphanumeric character. this is equivalent to class `[^a-zA-Z0-9_]`

NOTE: b means block, or word, it should has space between the words, can be the block
`\b`: Matches where the specified characters are at the beginning or at the end of a word. eg. `r"\bain"` `r"ain\b"` 
`\B`: Matches where the specified characters are present, but NOT at the beginning or at the end of a word. `r"\Bain"` `r"ain\B"`

```python
pattern = re.compile(regex_exp)
matches = pattern.finditer(test_string)
for match in matches:
	print(match) # eg: <re.Match object; span=(6,7), match='1'>
	
test_string = "hello 123_ hello world"
# Case sensitive. but can add `re.IGNORECASE` to p = re.compile('ab*', re.IGNORECASE)
regex_exp = r"\d" # matched 3 integers, which is 1,2,3. since \d only matches one. 
regex_exp = r"\d+" # matched 123.
regex_exp = r"\D" # matched all characters which are not the integer, eg. h, e, l, l, o, space, ...
regex_exp = r"\s" # matched 3 spaces, after first o, afeter _ and after second o
regex_exp = r"\S" # matched all characters except space.
regex_exp = r"\bhello" # matched 2 `hello` in test_string. it seaches words. 
# if test_string = "hello123", returns hello. 
# if test_string = "hello123hello". returns one hello, because the second hello is not at the beginning
# if test_string = "hello123 hello". returns two hello
regex_exp = r"\Bhello" # returns None, because there is no any hello words do not at the beginning.
# if test_string = "hello123 HHhello". returns hello which gets from HHhello

```

| Regular String  | Raw string   | To Match              |
| --------------- | ------------ | --------------------- |
| `"ab*"`         | `r"ab*"`\    | eg. ab, abb           |
| `"\\\\section"` | r"\\section" | \\session             |
| `"\\w+\\s+\\1"` | r"\w+\s+\1"  | ab \1                 |
| `.abc`          | `r"\.adc"`   | the . is actual  dash |

## Sets
use `[]` to get all items in a set. 
```python
pattern = re.compile(regex_exp)
matches = pattern.finditer(test_string)
for match in matches:
	print(match) # eg: <re.Match object; span=(6,7), match='1'>
	

test_string = "hello 123_ hello world"
regex_exp = r"[123]" # return 1,2,3 matches. equivalent r"[1-3]", to matching any integer from 1 to 3
regex_exp = r"[elo]" # return e,l,l,o  4 matches.
regex_exp = r"[\w]" # return all matches, except space

# [0-9] is a range from 0 to 9, [0-9-], the second `-` is actual character. eg: 123-, it returns 1,2,3,-
# [a-z] matches all lower cases, [a-zA-Z] equivalent to re.compile(r"[a-z]", re.IGNORECASE)

```

NOTE: [a-zA-Z] equivalent to re.compile(r"[a-z]", re.IGNORECASE)

## Groups

```python
emails = """
python-abd@gmail.com
jinyu.chen@icloud.com
jinyu2010.chen@xxx.org
"""

pattern = re.compile(r"([a-zA-Z0-9-]+)@([a-zA-Z]+)\.([a-zA-Z]+)")
matches = pattern.finditer(emails)
for match in matches:
	print(match) # return matches object
	print(match.groups())
	print(match.group(0)) # return whole email address
	print(match.group(1)) # return string beore @
	print(match.group(2)) # return string between @ and .
	print(match.group(3)) # return top domian, eg: com
	print(match.span()) # eg. (1, 21)

print(match.group*(1,2,2)) # the index of group 
# ('python-abd', 'gmail', 'gmail')
pritn(match.groups())

# <re.Match object; span=(1, 21), match='python-abd@gmail.com'>
# to get start and end in span, then match.start() and match.end() or match.spam()
```

#### outputs:
```txt
<re.Match object; span=(1, 21), match='python-abd@gmail.com'>
('python-abd', 'gmail', 'com')
python-abd@gmail.com
python-abd
gmail
com
<re.Match object; span=(22, 43), match='jinyu.chen@icloud.com'>
('jinyu.chen', 'icloud', 'com')
jinyu.chen@icloud.com
jinyu.chen
icloud
com
<re.Match object; span=(44, 66), match='jinyu2010.chen@xxx.org'>
('jinyu2010.chen', 'xxx', 'org')
jinyu2010.chen@xxx.org
jinyu2010.chen
xxx
org
```

## Modifications
- split()
- sub() # replace, eg `code = re.sub(r'\s', '', code)` ->  remove all spaces

### split example
```python
# split()
test_string = "123abc456abc123ABC"
pattern = re.compile(r"abc")
splitted_list = pattern.split(test_string)
print(splitted_list)

# OUTPUT
['123', '456', '123ABC']
```

### sub example, it can use group idx
```python

emails = """
python-abd@gmail.com
jinyu.chen@icloud.com
jinyu2010.chen@xxx.org
"""

pattern = re.compile(r"([a-zA-Z0-9-]+)@([a-zA-Z]+)\.([a-zA-Z]+)")
matches = pattern.finditer(emails)
for match in matches:
	print(match) # return matches object
	print(match.group(0)) # return whole email address
	print(match.group(1)) # return string beore @
	print(match.group(2)) # return string between @ and .
	print(match.group(3)) # return top domian, eg: com
sub_emails = pattern.sub(r"\2\3", emails)
print(sub_emails)

# sub_emails OUTPUT
gmailcom
icloudcom
xxxorg
```

```python
reg_exp = r"JIN(YU)?" # JIN or JINYU
reg_exp = r"JIN[YU]?" # JIN or JINY, JINYU
reg_exp = r"JIN[Y|U]" # JINY or JINU
reg_exp = r"JIN[YU]*" # JIN, or JINYU, JINYUYUYUYU...
```

## Complication Flags:
ASCII = American Standard Code for Information Interchange
```txt
ASCII or A: Makes serveal excapes like \w, \b, \s and \d match only on ASCII characters with the respective print
DOTALL or S: Make . match any character, including newlines.
IGNORECASE or I: Do case-insensitive matches
LOCALE or L: Do a locale-aware match. # Mostly relevant for legacy Python 2 code, not recommended in Python 3
NULTILINE or M: Multi-line matching, affecting ^ and $.
VERBOSE or X: (for 'extended'), Enable verbose REs, which can be organized more cleanly and understandably.
```

### re.ASCII

```python
import re

text = "hello 123 café"

# Without re.A — \w matches Unicode letters too
print(re.findall(r"\w+", text))           # ['hello', '123', 'café']

# With re.A — \w matches ASCII only
print(re.findall(r"\w+", text, re.A))     # ['hello', '123', 'caf']  (é is excluded)
```

### re.DOTALL

```python
text = "hello\nworld"

# Without re.S — . does NOT match newline
print(re.findall(r".+", text))            # ['hello', 'world']

# With re.S — . matches everything including newline
print(re.findall(r".+", text, re.S))      # ['hello\nworld']
```
### re.MULTILINE

```python
text = "hello\nworld\npython"

# Without re.M — ^ and $ match only start/end of entire string
print(re.findall(r"^\w+", text))          # ['hello']
print(re.findall(r"\w+$", text))          # ['python']

# With re.M — ^ and $ match start/end of each line
print(re.findall(r"^\w+", text, re.M))    # ['hello', 'world', 'python']
print(re.findall(r"\w+$", text, re.M))    # ['hello', 'world', 'python']
```

### re.VERBOSE(详细)

```python
# How to use VERBOSE
pat_with_annotation = re.compile(r"""
 \s*                 # Skip leading whitespace
 (?P<header>[^:]+)   # Header name
 \s* :               # Whitespace, and a colon
 (?P<value>.*?)      # The header's value -- *? used to
                     # lose the following trailing whitespace
 \s*$                # Trailing whitespace to end-of-line
""", re.VERBOSE)
```

## ?=...
```python
import re

text = "100USD 200EUR 300USD"

# Match numbers only if followed by USD
print(re.findall(r'\d+(?=USD)', text))    # ['100', '300']
# EUR numbers are excluded
```
## !=...
```python
text = "100USD 200EUR 300USD"

# Match numbers only if NOT followed by USD
print(re.findall(r'\d+(?!USD)', text))    # ['200']  → only EUR number
```

# Note


# Reference

