## adding below to  the top of note page

copy below and ctrl + p to choose: templater: Replace templates in the active file
```text
---
sr-due: <% tp.date.now("YYYY-MM-DD", 3) %>
sr-interval: 1
sr-ease: 2.5
---
```
### Explaination
```text
sr-due: is the next review date
sr-interval: how many days until next review
sr-ease: how fast the interval grows. rough idea: next_iterval = interval *  ease.
- higher ease -> review less often
- lower case -> review more often
```

After n days
```yaml
sr-due: <% tp.date.now("YYYY-MM-DD", n) %>
```


## Daily
```query
tag:#review/daily
```

## Every 3 Days
```query
tag:#review/3d
```

## Every 7 Days
```query
tag:#review/7d
```

## Every 15 Days
```query
tag:#review/15d
```

## Monthly
```query
tag:#review/30d
```

## Interview Review
```query
tag:#interview_review
```


# When to move notes between frequencies  
  
This is the **key habit**.  
When you review a note:  
- still confusing → move to **#review/daily**  
- mostly understand → **#review/3d**  
- comfortable → **#review/7d**  
- mastered → **#review/30d**  
  
Just **change the tag**.

