Date: 2026-01-10
Course:
Tags: 

# Content

## 1️⃣ What is OOD (Object-Oriented Design)?

**OOD = how you structure software using objects.**

It answers questions like:

* What classes should exist?
* What responsibilities should each class have?
* How do objects interact?
* Where should logic live?

OOD is about **designing the shape of your system**.

### Core OOD ideas

* Encapsulation
* Abstraction
* Inheritance
* Polymorphism
* Composition over inheritance

### Example (OOD thinking)

Instead of:

```python
def process_payment(type, amount):
    if type == "credit":
        ...
    elif type == "paypal":
        ...
```

OOD says:

```python
class PaymentMethod:
    def pay(self, amount): ...

class CreditCard(PaymentMethod):
    def pay(self, amount): ...

class PayPal(PaymentMethod):
    def pay(self, amount): ...
```

That’s **OOD**.

# Note


# Reference

