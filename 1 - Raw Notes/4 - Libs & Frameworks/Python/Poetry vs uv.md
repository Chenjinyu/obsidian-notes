Date: 2025-11-08
Course:
Tags: [[Python]] 
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content

## ⚡ Overview: Poetry vs uv

|Feature|🧰 **Poetry**|⚡ **uv**|
|---|---|---|
|Creator|Python community|[Astral](https://astral.sh/) (creators of `ruff`)|
|Purpose|Full project & dependency manager|Ultra-fast dependency resolver & package manager|
|Config file|`pyproject.toml`|`pyproject.toml`|
|Project creation|✅ `poetry new app`|✅ `uv init app`|
|Virtual environment|✅ Automatic|✅ Automatic & instant|
|Dependency resolution|Medium speed|⚡ Extremely fast (Rust-based)|
|Install method|`pip install poetry`|`curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh)|
|Build & publish|✅ Built-in|✅ Built-in (faster)|
|Performance|🐢 Slower (Python-based)|⚡ 10–100× faster (Rust binary)|
|Lock file|`poetry.lock`|`uv.lock`|
|Compatibility|Works anywhere with Python|Works with `pip`, `poetry.lock`, and `requirements.txt`|

---
## 🧪 What is **uv**?

**uv** is a **modern Python package manager written in Rust**, designed to replace **pip**, **virtualenv**, and **Poetry** — all in one tool.

Think of it as:

> **npm + npx + poetry + pip + virtualenv → combined and 100x faster.**

### Example commands:

```bash
# Initialize a project (like npm init or poetry new)
uv init my_project
cd my_project

# Add a package
uv add fastapi

# Run code in isolated env
uv run python main.py

# Lock dependencies
uv lock
```

✅ uv automatically creates a virtual environment, installs dependencies, and maintains reproducible builds — instantly.

---

## 🧰 Poetry example (for comparison)

```bash
poetry new my_project
cd my_project
poetry add fastapi
poetry run python main.py
```

It does the same thing — but slower, since it’s Python-based and needs to manage its own environment via `venv`.

## ✅  Run up a web server

In Poetry, you typically do:

```bash
poetry run uvicorn --app-dir=backend main:app --reload
```

In **uv**, the equivalent command is simply:

```bash
uv run uvicorn --app-dir=backend main:app --reload
```

💡 `uv run` behaves almost identically to `poetry run`, but it’s faster and lighter.
---

## ⚙️ Speed Comparison

|Operation|Poetry|uv|
|---|---|---|
|`add requests`|~5–10s|<0.5s|
|Resolve 50 deps|30s+|~2–3s|
|Fresh install|~15s|~1s|

💨 uv is **Rust-compiled** and uses **parallel network + dependency resolution**, which makes it incredibly fast.

---

## 🧩 Integration

|Integration|Poetry|uv|
|---|---|---|
|IDE support|✅ Mature (VS Code, PyCharm)|⚠️ Emerging (CLI only for now)|
|Works with PyPI|✅|✅|
|Docker-friendly|⚠️ Moderate|✅ Lightweight binary|
|PEP 582 (`__pypackages__`)|❌|✅ Optional|

---

## 🏁 Recommendation

|Use Case|Best Choice|
|---|---|
|Existing project using Poetry|✅ Stick with **Poetry**|
|New modern project|🚀 **uv** (faster, simpler, future-proof)|
|Need stable IDE support & ecosystem|✅ **Poetry**|
|Want npm-like experience & speed|⚡ **uv**|

---

## 🧱 Summary

|Category|**Poetry**|**uv**|
|---|---|---|
|Language|Python|Rust|
|Speed|Medium|⚡ Super Fast|
|Stability|Mature|New but rapidly growing|
|Project setup|`poetry new`|`uv init`|
|Virtualenv|Built-in|Built-in (faster)|
|Ideal for|Reliable builds|Modern workflows & speed|

---
Excellent question 👏 — and yes, **`uv` absolutely can do that** — it’s actually one of the things it does _better and faster_ than Poetry.

Let’s go over it clearly 👇

---





---

## ⚙️ How it works

When you run:

```bash
uv run <command>
```

`uv` will:

1. Create or use the project’s virtual environment automatically.
    
2. Ensure all dependencies (like `uvicorn`) are installed and isolated.
    
3. Execute the command inside that environment.
    

---

## 🧱 Example: Complete FastAPI project setup with `uv`

```bash
# 1️⃣ Initialize project
uv init fastapi-app
cd fastapi-app

# 2️⃣ Add dependencies
uv add fastapi uvicorn

# 3️⃣ Create your FastAPI app
echo '
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def hello():
    return {"msg": "Hello, uv!"}
' > main.py

# 4️⃣ Run the server
uv run uvicorn main:app --reload
```

✅ Output:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 💨 Why `uv run` is faster

Unlike Poetry (which spawns a Python subprocess and manually activates the venv),  
`uv run` uses a **native Rust launcher** that directly executes the command in an isolated environment — with zero activation overhead.

---

## 🧩 Bonus Tip — “npm-like” workflow

If you prefer shorter commands (like `npm run start`),  
you can define a script alias inside `pyproject.toml`:

```toml
[tool.uv.scripts]
start = "uvicorn --app-dir=backend main:app --reload"
```

Then simply run:

```bash
uv run start
```

---

✅ **Summary**

|Feature|Poetry|uv|
|---|---|---|
|Run command in venv|`poetry run cmd`|`uv run cmd`|
|Start FastAPI|✅|✅|
|Speed|🐢 Slower (Python subprocess)|⚡ Instant (Rust binary)|
|Script alias|✅|✅|
|Setup overhead|High|Minimal|

---

So yes — your example

```bash
poetry run uvicorn --app-dir=backend main:app --reload
```

becomes perfectly valid and faster as:

```bash
uv run uvicorn --app-dir=backend main:app --reload
```

---

Would you like me to show how to **structure a FastAPI + uv project folder** (like `/backend`, `/frontend`, `/tests`) so it’s ready for production setup?


# Note


# Reference

