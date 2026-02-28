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
`[]` 
# Note


# Reference

