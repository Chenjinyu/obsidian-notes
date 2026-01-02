Date: 2025-11-05
Course:
Tags: [[Platform]] [[Security]] [[CICD Pipeline]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content
Fantastic question — **Checkmarx vs SonarQube** is a very common comparison when teams are choosing a **code security and quality scanning** solution.

They seem similar at first, but they actually focus on **different layers** of code analysis.
Let’s break it down clearly 👇

---

## ⚙️ 1. Quick Comparison Table

| Feature                     | **Checkmarx**                                    | **SonarQube**                                                  |
| --------------------------- | ------------------------------------------------ | -------------------------------------------------------------- |
| **Primary Focus**           | ✅ **Security (SAST)**                            | ✅ **Code Quality & Maintainability**                           |
| **Main Use Case**           | Find **security vulnerabilities** in source code | Find **bugs**, **code smells**, and some **security hotspots** |
| **Analysis Type**           | Static Application Security Testing (**SAST**)   | Static Code Analysis (style, quality, minor security)          |
| **Languages Supported**     | ~30+ (Java, JS, Python, C#, Go, etc.)            | 25+ (Java, JS, Python, C#, C/C++, Go, etc.)                    |
| **Depth of Security Scans** | 🔥 Deep security scanning (OWASP, CWE, CVE)      | ⚠️ Shallow security checks, mostly maintainability             |
| **Integration**             | CI/CD, IDEs, GitHub, GitLab, Jenkins, etc.       | IDEs, CI/CD, and code hosting (GitHub/GitLab)                  |
| **Reports & Dashboards**    | Enterprise-grade vulnerability dashboards        | Developer-friendly code quality dashboards                     |
| **License / Cost**          | 💰 Commercial (Checkmarx One platform)           | 🆓 Free Community Edition + paid Enterprise                    |
| **False Positive Rate**     | Lower (custom rules)                             | Higher for security issues                                     |
| **Deployment**              | Cloud or on-prem (enterprise focus)              | Self-hosted or cloud (easy to set up)                          |

---

## 🧠 2. Conceptual Difference

### 🔒 **Checkmarx = Security Scanner (SAST)**

* Detects **security vulnerabilities** in your source code — before runtime.
* Matches patterns against known vulnerabilities (e.g., SQL injection, XSS, path traversal).
* Classifies issues using **CWE / OWASP** standards.
* Often integrated into **DevSecOps pipelines**.

✅ Example issues Checkmarx flags:

* Hardcoded passwords
* Unsafe SQL queries (`cursor.execute(f"SELECT * FROM {user_input}")`)
* Path traversal (`open(f"../../etc/passwd")`)
* Insecure deserialization

---

### 🧹 **SonarQube = Code Quality & Maintainability Tool**

* Focuses on **code cleanliness, duplication, complexity, coverage**, and some **security hotspots**.
* Encourages writing maintainable, testable, well-structured code.
* Flags issues like:

  * Duplicated logic
  * Functions too long or complex
  * Unused variables/imports
  * Potential null-pointer risks
  * Some security patterns (basic)

✅ Example issues SonarQube flags:

* "This method has too many parameters."
* "Use try-with-resources to close this stream."
* "This function has cognitive complexity of 20."

---

## 🧩 3. Typical Workflow Integration

| Pipeline Stage                      | Checkmarx                           | SonarQube                                 |
| ----------------------------------- | ----------------------------------- | ----------------------------------------- |
| **Developer IDE check**             | Yes (plugin for VSCode, IntelliJ)   | Yes                                       |
| **Pre-commit / Pull request**       | Scan for security issues            | Check code quality                        |
| **CI/CD (Jenkins, GitHub Actions)** | Run SAST + generate security report | Analyze code metrics + coverage           |
| **Reporting**                       | OWASP Top 10, CWE, CVE mapping      | Code coverage, maintainability, tech debt |

Most large teams use **both**:

> * **Checkmarx** → deep **security** coverage
> * **SonarQube** → ongoing **code quality + maintainability**

---

## ⚡ 4. Example in Practice

| Example Use Case                                                  | Recommended Tool                   |
| ----------------------------------------------------------------- | ---------------------------------- |
| You need to **detect security vulnerabilities** before deploying  | ✅ **Checkmarx**                    |
| You want to **maintain code quality** and enforce style standards | ✅ **SonarQube**                    |
| You want to catch **SQL injection, XSS, path traversal, etc.**    | ✅ **Checkmarx**                    |
| You want to enforce **clean architecture, test coverage**         | ✅ **SonarQube**                    |
| You want a **free tool for CI/CD quality checks**                 | 🆓 **SonarQube Community Edition** |

---

## 🧩 5. Integration Example (CI/CD)

**With Checkmarx:**

```yaml
# GitHub Actions Example
- name: Checkmarx SAST Scan
  uses: Checkmarx/ast-github-action@v1
  with:
    project_name: my-app
    cx_tenant: ${{ secrets.CX_TENANT }}
    cx_client_id: ${{ secrets.CX_CLIENT_ID }}
    cx_client_secret: ${{ secrets.CX_CLIENT_SECRET }}
```

**With SonarQube:**

```yaml
- name: SonarQube Scan
  uses: sonarsource/sonarqube-scan-action@v2
  with:
    projectBaseDir: .
    args: >
      -Dsonar.projectKey=my-app
      -Dsonar.organization=my-org
```

---
## ✅ TL;DR

| Goal                              | Best Tool                |
| --------------------------------- | ------------------------ |
| **Security vulnerabilities**      | 🔒 **Checkmarx (SAST)**  |
| **Code quality, maintainability** | 🧹 **SonarQube**         |
| **Full DevSecOps setup**          | 🤝 **Use both together** |

---
👉 **Summary**

* **Checkmarx** = “Security-first”
* **SonarQube** = “Quality-first”
* **Ruff + Flake8/Black** = Developer productivity tools
# Note


# Reference

