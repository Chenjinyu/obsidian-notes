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
`b`: Matches where the specified characters are at the beginning or at the end of a word. eg. `r"\bain"` `r"ain\b"`
`\B`: Matches where the specified characters are present, but 
# Note


# Reference

