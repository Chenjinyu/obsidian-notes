Date: 2025-11-04
Course:
Tags: [[Python]] [[Code Formatter]] 
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content
## ⚙️ 1. Quick Summary Table

| Tool       | Type      | Purpose                   | Speed                  | Configurable  | Notes                         |
| ---------- | --------- | ------------------------- | ---------------------- | ------------- | ----------------------------- |
| **flake8** | Linter    | Style, PEP8, error checks | 🐢 Slow (Python-based) | ✅ Yes         | Very stable, classic tool     |
| **black**  | Formatter | Auto code formatting      | ⚡ Fast                 | ❌ Opinionated | Enforces one consistent style |
|            |           |                           |                        |               |                               |
|**ruff**|Linter + Formatter (soon full)|Linting, formatting, import sorting, error checks|🚀 Super fast (Rust-based)|✅ Yes|Replaces flake8, isort, black (optional)|
---

## 🧩 2. What Each One Does

### 🧠 **flake8**
- Written in Python 🐍
- Focuses on **linting only** — doesn’t change your code.
- Warns about unused imports, indentation issues, undefined variables, etc.
- Has a plugin system (`flake8-bugbear`, `flake8-docstrings`, etc.).
- Slower on big projects.
    
```bash
flake8 my_project/
```
---
### ⚡ **black**
- Only **formats** code (not linting).
- Opinionated — no configuration beyond line length.
- Very reliable and widely adopted in major projects.
- Usually paired with `flake8` and `isort`.

```bash
black my_project/
```
---
### 🚀 **ruff**
- Written in **Rust** → about **10–100× faster** than flake8 + black combo.
- Supports **linting**, **import sorting**, and now **formatting** (Black-compatible mode).
- Emulates many tools in one:
    - `flake8` + all major plugins
    - `isort` (import sorting)
    - `pylint` (some checks)
    - `black` (formatter via `ruff format`)
- Actively maintained, used by **FastAPI**, **Pydantic**, **Polars**, etc.
    
```bash
ruff check my_project/
ruff format my_project/
```

---
## 🧠 3. Real-world popularity (2025 snapshot)

|Tool|Popularity|Trend|
|---|---|---|
|**flake8**|🔹 Mature, still widely used in legacy codebases|⬇️ Slowly declining|
|**black**|🔹 Extremely popular for formatting|⬆️ Stable|
|**ruff**|🔥 Rapidly growing, used in modern Python projects|⬆️⬆️ Exploding|

You’ll find `ruff` now adopted in:

- **FastAPI**
    
- **Pydantic**
    
- **Astral**
    
- **HuggingFace**
    
- **Many Data/AI projects**
    

---

## 🧰 4. Example setup: `ruff` replacing all three

`pyproject.toml`:

```toml
[tool.ruff]
line-length = 88
extend-select = ["I"]  # enable import sorting
fix = true

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

Then:

```bash
ruff check .
ruff format .
```

Ruff now lints, formats, and sorts imports — in milliseconds 🚀.

---

## 🧩 5. Recommendation (2025+)

|Use Case|Recommended Tool|
|---|---|
|**New project**|✅ **Ruff** (does everything)|
|**Existing codebase using flake8 + black**|Keep them for now, migrate slowly to Ruff|
|**You want max consistency & speed**|Ruff|
|**You like Black’s exact formatting rules**|Ruff + `ruff format` (Black-compatible)|

---

### ✅ TL;DR

|Tool|Keep Using?|Reason|
|---|---|---|
|**flake8**|⚠️ Legacy only|Ruff replaces it|
|**black**|✅ Still great|If you only want formatting|
|**ruff**|🚀 Yes — best modern choice|Combines speed + features|

---

Would you like me to show you a **step-by-step VS Code setup** where Ruff automatically lints and formats your Python files on save (replacing flake8 + black)? It’s the cleanest dev experience right now.

# Note


# Reference

