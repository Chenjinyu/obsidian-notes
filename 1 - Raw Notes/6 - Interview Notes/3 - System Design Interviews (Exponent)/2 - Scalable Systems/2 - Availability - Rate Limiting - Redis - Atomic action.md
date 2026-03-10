Date: 2026-02-03
Course:
Tags: [[System Design Interview]] [[Availability]]

# Content

“Atomic” means **indivisible**: an operation happens **all at once**, so other clients will never see a “half-done” state.
In Redis, when people say “an operation is atomic,” they usually mean:
1. **No interleaving:**  
    While Redis is executing that command, **no other command runs in the middle of it**.
2. **All-or-nothing effect:**  
    The command’s changes either **fully apply** or (if it errors) **do not partially apply**.
### Concrete examples
- `INCR key` is atomic  
    If 10 clients call `INCR` at the same time, the result will be 1..10 with no duplicates/missed values.
- `LPUSH mylist a` is atomic  
    The element is either pushed or not; the list won’t be corrupted by concurrent pushes.
### What “atomic” does _not_ mean

- It does **not** mean “a whole workflow of multiple commands is atomic.”  
    Example: these two commands are **not** atomic as a pair:
    1. `GET tokens`
    2. `DECR tokens`
    Between them, another client could change `tokens`. That’s exactly how you get broken rate limiters.
### How to make multiple steps atomic in Redis
Use one of these:
- **Lua script (`EVAL`)**: multiple reads/writes in one script are executed as one atomic unit.
- **Transactions (`MULTI/EXEC`)**: executes a batch sequentially without interleaving, but if you need “check then set” correctness, you usually pair it with **WATCH** (optimistic locking).
- **Single composite commands** when available (e.g., `INCR` + `EXPIRE` patterns often use Lua to avoid races).
### Why this matters for rate limiting
A limiter usually needs: “read state → compute → update state → decide allow/deny.”  
If that’s not atomic, two requests can both pass when only one should.
So the statement “all Redis operations are atomic” should be interpreted as:
- **Each single Redis command is atomic**, and
- **Lua scripts are atomic**, but
- **Your multi-command logic is NOT automatically atomic unless you wrap it** (Lua or transaction with WATCH).

If you tell me which limiter you’re implementing (fixed window / token bucket / sliding window), I can show the exact atomic Redis pattern for it.
# Note


# Reference

