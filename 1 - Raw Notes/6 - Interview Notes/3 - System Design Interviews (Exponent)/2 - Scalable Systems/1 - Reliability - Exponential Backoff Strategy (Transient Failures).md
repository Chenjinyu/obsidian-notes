Date: 2026-01-30
Course:
Tags:  [[interview]] [[System Design Interview]] [[../../../../High Level]] [[Low Level]] [[Reliability]]

# Content

## 🧾 Interview-ready explanation (clean)

> Exponential backoff is a retry strategy where the delay between retries increases exponentially after each failure, often with added randomness (jitter), to reduce system load and avoid retry storms while allowing transient failures to recover.


Exponential Backoff Strategy: this is a **core reliability pattern** used everywhere: cloud APIs, message queues, microservices, databases, distributed locks.
## 🎯 Simple definition
> **Exponential Backoff** means: when something fails, you retry — but wait longer and longer between each retry. Instead of hammering the system.

**Interview insight**: "Circuit breakers are for non-transient failures. For transient failures, we use retry logic. Using circuit breaker for transient failures would cause unnecessary service degradation. Using retry for non-transient failures wastes resources and increases latency."
### Retry Example
```python
# Retry with exponential backoff
@retry(
    max_attempts=3,
    backoff=ExponentialBackoff(base=2),
    retryable_exceptions=[NetworkError, TimeoutError]
)
def call_api():
    return requests.get("https://api.example.com/data")

```


---
## 📈 Basic idea (human-friendly)

Instead of:
❌ retry immediately  
❌ retry immediately again  
❌ overload system

You do:

✅ wait 1 second  
✅ then 2 seconds  
✅ then 4 seconds  
✅ then 8 seconds  
✅ then 16 seconds

👉 delays grow exponentially.

---
## ⏱ Example timeline

|Attempt|Wait before next try|
|---|---|
|1st fail|1 second|
|2nd fail|2 seconds|
|3rd fail|4 seconds|
|4th fail|8 seconds|
|5th fail|16 seconds|
Formula:
```
delay = base * 2^attempt
```

---

## 🤔 Why is this important?
Because in distributed systems:
Failures are usually:
• temporary  
• overload-related  
• network hiccups

If everyone retries immediately:
💥 you create a retry storm  
💥 system crashes harder

This is called **thundering herd problem**.

---
## ✅ Exponential backoff solves:
✔ prevents overload  
✔ gives system time to recover  
✔ increases success rate  
✔ improves stability

---
## 📦 Where it’s commonly used

You’ll see it in:
✅ API calls (AWS, Google, OpenAI, etc.)  
✅ message consumers (Kafka, SQS)  
✅ DB connections  
✅ distributed locks  
✅ HTTP retries
AWS SDKs use it by default.

---

## 🧠 Simple real-world analogy
If a website is down:
❌ refreshing every 1 second
vs
✅ wait 1 min  
✅ then 2 min  
✅ then 4 min

The second is smarter and kinder to system.

---

## ⚠️ Add Jitter (VERY important in practice)

Without jitter:
All clients retry at same time again → spike again.
So you add randomness:
```
delay = random(0, base * 2^attempt)
```
This spreads retries.
This is called:
👉 **Exponential Backoff with Jitter** (industry standard)

---
## 🧪 Example in Python

```python
import time
import random

base = 1

for attempt in range(5):
    try:
        call_service()
        break
    except Exception:
        delay = random.uniform(0, base * 2**attempt)
        time.sleep(delay)
```

---

## 🎯 Typical parameters in real systems

• base = 100ms or 1s  
• max delay = 30s or 60s  
• max retries = 5–10
So it doesn’t grow forever.

---
## 📊 Compare retry strategies

|Strategy|Problem|
|---|---|
|Immediate retry|overload, storms|
|Fixed delay|still synchronized spikes|
|Exponential backoff|scalable & stable ✅|

---
## 🚨 Common mistakes

❌ infinite retries without limit  
❌ no jitter  
❌ too aggressive base time

---
## 🎯 How it connects to what you learned earlier

In:
• Saga retries  
• Outbox publishers  
• Worker consumers
You ALWAYS combine:
👉 retries + exponential backoff
This makes pipelines reliable.

---
# ✅ Final takeaway
✔ Failures are normal in distributed systems  
✔ Retrying immediately makes things worse  
✔ Exponential backoff makes retries smart
It’s a must-have reliability pattern.

# Note


# Reference

