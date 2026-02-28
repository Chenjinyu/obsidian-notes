Date: 2026-02-28
Course:
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
`^` starts with "^hello"
`$` Ends with "world$"
`*` Zero or more occurrences "aix*"
`+` One or more occurrences "aix+"
`{}` Exactly the specified number of occurrences: "al{2}", eg: `all`
`[]` A set of characters "[a-m]" 
`\` Special sequence (or escape special characters), "\d"
`|` Either or "falls|stays"
`()` Capture and group

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

| Regular String  | Raw string   | To Match    |
| --------------- | ------------ | ----------- |
| `"ab*"`         | `r"ab*"`\    | eg. ab, abb |
| `"\\\\section"` | r"\\section" | \\session   |
| `"\\w+\\s+\\1"` | r"\w+\s+\1"  | ab \1       |
|                 |              |             |

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

```
# Note


# Reference

