Date: 2026-01-10
Course:
Tags: 

# Content

**SOLID** is a set of **five object-oriented design principles** that help you build software that is:

* easier to maintain
* easier to extend
* less fragile
* more testable

They are **program design principles**, not syntax rules.

---

## What is SOLID?

**SOLID** stands for:

1. **S** — Single Responsibility Principle (SRP)
2. **O** — Open/Closed Principle (OCP)
3. **L** — Liskov Substitution Principle (LSP)
4. **I** — Interface Segregation Principle (ISP)
5. **D** — Dependency Inversion Principle (DIP)

Each principle solves a **specific kind of design problem**.

---

# 1️⃣ Single Responsibility Principle (SRP)

### Definition

> A class should have **only one reason to change**.

### ❌ Bad example (violates SRP)

```python
class UserService:
    def save_user(self, user): ...
    def send_email(self, user): ...
    def log_activity(self, user): ...
```

Problems:

* User persistence
* Email sending
* Logging
  → **three responsibilities**

---

### ✅ Good example (SRP-compliant)

```python
class UserRepository:
    def save(self, user): ...

class EmailService:
    def send(self, user): ...

class AuditLogger:
    def log(self, user): ...
```

Each class has **one job**.

---

# 2️⃣ Open/Closed Principle (OCP)

### Definition

> Software entities should be **open for extension, closed for modification**.

### ❌ Bad example (violates OCP)

```python
def calculate_discount(user_type):
    if user_type == "vip":
        return 0.2
    elif user_type == "regular":
        return 0.1
```

Adding a new type → **modify existing code**.

---

### ✅ Good example (OCP-compliant)

```python
class DiscountStrategy:
    def discount(self): ...

class VIPDiscount(DiscountStrategy):
    def discount(self): return 0.2

class RegularDiscount(DiscountStrategy):
    def discount(self): return 0.1
```

Add new discounts **without touching existing code**.

---

# 3️⃣ Liskov Substitution Principle (LSP)

### Definition

> Subclasses must be **substitutable** for their base classes.

### ❌ Bad example (violates LSP)

```python
class Bird:
    def fly(self): ...

class Penguin(Bird):
    def fly(self):
        raise Exception("Cannot fly")
```

Code expecting `Bird` breaks when given `Penguin`.

---

### ✅ Good example (LSP-compliant)

```python
class Bird: ...

class FlyingBird(Bird):
    def fly(self): ...

class Penguin(Bird):
    def swim(self): ...
```

No false promises.

---

# 4️⃣ Interface Segregation Principle (ISP)

### Definition

> Clients should not be forced to depend on methods they do not use.

### ❌ Bad example (violates ISP)

```python
class Machine:
    def print(self): ...
    def scan(self): ...
    def fax(self): ...
```

```python
class OldPrinter(Machine):
    def scan(self): raise NotImplementedError
    def fax(self): raise NotImplementedError
```

---

### ✅ Good example (ISP-compliant)

```python
class Printable:
    def print(self): ...

class Scannable:
    def scan(self): ...
```

```python
class OldPrinter(Printable):
    def print(self): ...
```

Small, focused interfaces.

---

# 5️⃣ Dependency Inversion Principle (DIP)

### Definition

> High-level modules should not depend on low-level modules.
> Both should depend on **abstractions**.

### ❌ Bad example (violates DIP)

```python
class MySQLDatabase:
    def save(self, data): ...

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()
```

Changing DB → modify business logic.

---

### ✅ Good example (DIP-compliant)

```python
class Database:
    def save(self, data): ...

class MySQLDatabase(Database):
    def save(self, data): ...

class UserService:
    def __init__(self, db: Database):
        self.db = db
```

Now:

* DB is swappable
* Code is testable

---

# How SOLID fits together

| Principle | Solves                     |
| --------- | -------------------------- |
| SRP       | Classes doing too much     |
| OCP       | Constant code modification |
| LSP       | Broken inheritance         |
| ISP       | Fat interfaces             |
| DIP       | Tight coupling             |

They **reinforce each other**.

---

## TL;DR

* **SOLID** = design principles for maintainable software
* Each principle addresses a different design failure
* You don’t “use SOLID everywhere”
* Apply it where code must **evolve**

Great request. Let’s look at **SOLID as it actually appears in real Python frameworks**, not toy examples.

I’ll walk through **FastAPI, SQLAlchemy, Pandas, and Django**, and explicitly map **each SOLID principle** to **real design decisions** they made.

---

# SOLID in Real Python Frameworks

## 1️⃣ SRP — Single Responsibility Principle

> One class / module = one reason to change

### 🔹 FastAPI (very clear SRP)

FastAPI **separates responsibilities strictly**:

|Component|Responsibility|
|---|---|
|Path function|HTTP handling|
|Pydantic model|Validation & serialization|
|Dependency|Business logic|
|Router|URL grouping|

### Example

```python
@app.post("/users")
def create_user(
    user: UserCreate,
    service: UserService = Depends()
):
    return service.create(user)
```

- Endpoint → HTTP concerns
    
- `UserCreate` → validation
    
- `UserService` → business logic
    

✔ Each part changes for **one reason only**

---

### 🔹 SQLAlchemy

SQLAlchemy separates:

- ORM mapping
    
- SQL generation
    
- Connection management
    
- Transaction control
    

You don’t see a “God class” doing everything.

---

## 2️⃣ OCP — Open/Closed Principle

> Open for extension, closed for modification

### 🔹 SQLAlchemy (textbook OCP)

SQLAlchemy supports **dozens of databases** without modifying core ORM code.

```python
engine = create_engine("postgresql://...")
engine = create_engine("mysql://...")
engine = create_engine("sqlite://...")
```

How?

- Dialects are **plug-ins**
    
- New DBs = new dialect classes
    

✔ Core stays closed  
✔ Extensions grow freely

---

### 🔹 FastAPI

FastAPI lets you extend:

- Authentication
    
- Dependencies
    
- Middleware
    
- Validation
    

…without touching FastAPI internals.

```python
app.add_middleware(CustomMiddleware)
```

That’s OCP in practice.

---

## 3️⃣ LSP — Liskov Substitution Principle

> Subtypes must be substitutable for base types

### 🔹 SQLAlchemy Session

Anywhere SQLAlchemy expects a `Session`, you can pass:

- Regular session
    
- Scoped session
    
- Custom session subclass
    

They all honor the same behavioral contract.

```python
def save_user(session: Session):
    session.add(user)
    session.commit()
```

No surprises.  
No broken assumptions.

✔ LSP preserved

---

### 🔹 Pandas Series vs DataFrame

Both expose overlapping behaviors:

- Indexing
    
- Iteration
    
- Aggregation
    

But Pandas is careful **not to promise behavior** it can’t guarantee across types.

That’s deliberate LSP discipline.

---

## 4️⃣ ISP — Interface Segregation Principle

> Clients shouldn’t depend on methods they don’t use

### 🔹 Pandas (classic ISP)

```python
pd.read_csv(file_like)
```

Pandas does NOT require:

- a “PandasFile” base class
    
- a huge interface
    

It only expects:

```python
.read()
```

Anything with `.read()` works:

- File
    
- StringIO
    
- Network stream
    

✔ Minimal interface  
✔ No fat abstractions

---

### 🔹 FastAPI dependencies

A dependency only needs:

- What the endpoint needs
    

No forced “service base class”.

```python
def get_user_service():
    return UserService()
```

That’s ISP + duck typing.

---

## 5️⃣ DIP — Dependency Inversion Principle

> Depend on abstractions, not concretions

### 🔹 FastAPI (one of the best examples)

FastAPI uses **dependency injection everywhere**.

```python
def get_user(service: UserService = Depends()):
    ...
```

The endpoint:

- Does NOT create `UserService`
    
- Does NOT know implementation details
    

You can swap:

- Real service
    
- Mock
    
- Stub
    

✔ High-level code depends on abstractions  
✔ Low-level details injected

---

### 🔹 SQLAlchemy engine abstraction

Your app code depends on:

```python
Engine
```

Not:

- psycopg2
    
- mysqlclient
    
- sqlite3
    

That’s pure DIP.

---

## Why these frameworks prefer Protocol-like design

Even when they don’t explicitly use `typing.Protocol`, they design APIs as if they do.

They rely on:

- Behavior
    
- Capabilities
    
- Contracts
    

Not:

- Inheritance
    
- Concrete types
    

This:

- Enables OCP
    
- Reduces coupling
    
- Improves extensibility
    
- Makes testing easier
    

---

## Summary Table

|Principle|FastAPI|SQLAlchemy|Pandas|
|---|---|---|---|
|SRP|🔥 Strong|🔥 Strong|🔥 Strong|
|OCP|🔥 Plugins, middleware|🔥 Dialects|🔥 Readers|
|LSP|✅ Dependency contracts|🔥 Session types|✅ Careful API|
|ISP|🔥 Small dependencies|🔥 Focused interfaces|🔥 Duck typing|
|DIP|🔥 DI system|🔥 Engine abstraction|⚠️ Partial|

---

## The big takeaway

> **SOLID is not academic — it’s why these frameworks scale to millions of users.**

They:

- Minimize breaking changes
    
- Encourage extension
    
- Avoid inheritance traps
    
- Stay maintainable over years

---

## TL;DR

- FastAPI, SQLAlchemy, Pandas all **actively apply SOLID**
    
- They prefer **behavior over inheritance**
    
- They design APIs to be **extensible, stable, and testable**
    
- `Protocol` is the modern way to express what they already do
    



# Note


# Reference

