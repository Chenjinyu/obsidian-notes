Date: 2025-10-26
Course:
Tags: [[Ansible]] [[Terrform]] [[Kubernetess]] [[AutoHook]] [[Pre-commit]] [[PyHusky]] [[Kitchen]]
Revisit: <% tp.date.now("YYYY-MM-DD", +7) %>

# Content
## Table of Contents
- [Ansible](#ansible)
- [PyHusky](#pyhusky)
- [AutoHook vs pre-commit](#autohook-vs-pre-commit)
- [kitchen.yml](#kitchenyml-test-kitchen)
- [tox.ini](#toxini)


## Ansible
is an open-source IT automation tool used to configure systems, deploy applications, and orchestrate infrastructure. it's simple, agentless, and highly extensible.

#### What Can Ansible Do?
- Provision servers (e.g., install Python, configure Nginx)
- Deploy applications (e.g., copy files, restart services)
- Manage infrastructure as code (like Terraform or CloudFormation)
- Orchestrate multi-tier environments (e.g., web → app → DB stack)


#### Ansible vs Kubernetes
**TL;DR Summary**

| Feature          | **Ansible**                                         | **Kubernetes**                                      |
| ---------------- | --------------------------------------------------- | --------------------------------------------------- |
| Primary Use      | Automate **configuration** and **deployment tasks** | **Manage and orchestrate** containers in clusters   |
| Type             | Automation tool / Infrastructure as Code (IaC)      | Container orchestration system                      |
| Works On         | VMs, bare-metal servers, cloud hosts                | Containers (e.g., Docker)                           |
| Architecture     | Agentless (uses SSH/WinRM)                          | Requires Kubernetes cluster with agents (kubelet)   |
| Common Use Case  | Install packages, push config, deploy apps          | Run, scale, and heal containerized applications     |
| State Management | **Push-based**, doesn’t store system state          | **Declarative, self-healing**, stores desired state |

**Think of a restaurant:**

- Ansible is the kitchen manager who sets up the kitchen: buys equipment, stocks ingredients, trains staff.
- Kubernetes is the floor manager who coordinates the chefs: tells them what dish to prepare, when to serve, and replaces them if someone is sick.

#### Ansible vs Terraform
|                 | **Terraform**                    | **Ansible**                                   |
| --------------- | -------------------------------- | --------------------------------------------- |
| **Focus**       | Infrastructure provisioning      | Configuration management                      |
| **State**       | Maintains and compares state     | Stateless                                     |
| **When to use** | Create/update/delete cloud infra | Configure servers & applications              |
| **Example use** | Create VPC, EC2, RDS             | Install NGINX, deploy code, update app config |


#### Ansible vs Chef
| Scenario                        | Use **Ansible**        | Use **Chef**            |
| ------------------------------- | ---------------------- | ----------------------- |
| Small to mid-sized environments | ✅ Yes                  | ❌ Overkill              |
| No agent installation allowed   | ✅ SSH-based            | ❌ Requires client/agent |
| Declarative, reusable configs   | ⚠️ Less strict         | ✅ Strong pattern        |
| Large, multi-region enterprise  | ⚠️ Possible, not ideal | ✅ Scales better         |
| Steep learning curve ok         | ✅ Easy learning curve  | ❌ Requires Ruby & DSL   |

---


## PyHusky

## AutoHook vs pre-commit
Autohook is a tool that manages Git pre-commit hooks in Python projects using python-native configuration.
unlike `.pre-commit-config.yml` from `pre-commit`, autohooks allows you to configure and chain multiple Python tooling (like `flake8`, `pylint`, `isort`, `black`, etc) directly in your project directory using .ini or .toml config files.

- black: Code formatter
- flake8: Linter for syntax/sytle violation
- pylint: Deeper static code analysis
- mypy: type-checking using annotations
- isort: sort and organize imports

example looks like:
```toml
[default]
hooks = ["black", "flake8", "pylint", "mypy", "isort"]

[black]
args = ["--check"]

[flake8]
args = ["--max-line-length=88", "--ignore=E203,W503"]

[pylint]
args = ["yourapp_sdk"]

[mypy]
args = ["yourapp_sdk", "--ignore-missing-imports"]

[isort]
args = ["--check-only", "--profile", "black"]

```
#### pre-commit
    A widely adopted hook manager that supports multi-language tools, Dockerized hooks, and Git repo integration. 
    is yaml-based, cross-lanauge support, and good commnuity. 

---

## kitchen.yml ([Test Kitchen](https://kitchen.ci/))
a tool used for testing infrastructure code (like Chef, Ansible, or other configuration management scripts). it defines the configuration for how Test Kitchen spins up instances(e.g. Docker, EC2, Vagrant), runs provisioning, and eecutes tests.

### Typical Use Case
Primarily used in DevOps or infrastructure-as-code (IaC) workflows to:
- Provision a temporary instance (e.g., with Docker or VirtualBox)
- Apply Chef/Ansible/Puppet scripts
- Run test suites (like InSpec or shell tests)
- Tear down the instance

---

## tox.ini
tox.ini(Python Test Automation Configuration) is the configuration file for tox, a popular Python testing tool used to:
- Automate testing across multiple Python environments
- Manage virtualenvs
- Run linters, tests, and packaging commands

It's especially useful for:
- Ensuring your package works on multiple Python versions (e.g. 3.8, 3.9, 3.11)
- Automating CI test suites
- Standardizing local development environments

```ini
[tox]
envlist = py38, py39, lint

[testenv]
deps = pytest
commands = pytest tests/

[testenv:lint]
skip_install = true
deps = flake8
commands = flake8 src/ tests/

```
| Section        | Purpose                                                         |
| -------------- | --------------------------------------------------------------- |
| `[tox]`        | Defines tox’s general config, like which environments to run    |
| `envlist`      | List of environments (like `py38` = Python 3.8) to test against |
| `[testenv]`    | Default test environment setup: what to install, what to run    |
| `deps`         | Dependencies to install (e.g., `pytest`, `flake8`)              |
| `commands`     | Commands to run in that environment                             |
| `skip_install` | If `true`, skip installing your package into the virtualenv     |

#### Use Cases
- Run tox to test your code across all versions in envlist
- Add a [testenv:docs] for building documentation
- Add [testenv:format] for running black code formatter
- Use in CI/CD to ensure compatibility

```bash
pip install tox
tox  # runs all environments
tox -e py39  # only run for Python 3.9
tox -e lint  # run linter
```


Example of execute tox with all envlist: py38, py39, py310, docs, flake8, precommit.
```ini
[tox]
envlist = py38, py310, flake8, docs, precommit
isolated_build = true  # use PEP 517 if you're using pyproject.toml

# ---------------------------
[testenv]
description = Run tests with pytest
deps = pytest
commands = pytest tests/

# ---------------------------
[testenv:flake8]
description = Lint with flake8
skip_install = true
deps = flake8
commands = flake8 src/ tests/

# ---------------------------
[testenv:docs]
description = Build Sphinx documentation
deps =
    sphinx
    -rdocs/requirements.txt  # if needed
commands = sphinx-build -b html docs/ docs/_build/html

# ---------------------------
[testenv:precommit]
description = Run pre-commit hooks
skip_install = true
deps = pre-commit
commands = pre-commit run --all-files

```

#### How it Works
- py38 and py310 run your main test suite using those Python versions.
- The rest (flake8, docs, pre-commit) are utility environments.

#### tox.ini vs makefile

**tox.ini — Best For:**
- Python projects
- Testing across multiple versions (py38, py39, py310, etc.)
- Linting/formatting with consistent isolated environments
- Automating docs/testing in CI/CD pipelines

**Makefile - Best for**:
- Complex workflows across multiple tools/languages
- Docker, Node.js, Go, shell scripts, AWS CLI, etc.
- Chaining build steps and deploying
- Platform-specific automation (e.g., make dev, make deploy)
- However the makefile also is able to use in CI/CD pipeline.


| Use Case                              | Recommended Tool |
| ------------------------------------- | ---------------- |
| Run Python tests on multiple versions | ✅ `tox`          |
| Run Python linter with venv isolation | ✅ `tox`          |
| Build Docker images                   | ✅ `Makefile`     |
| Deploy to AWS or run shell scripts    | ✅ `Makefile`     |
| Mixed-language project (JS + Python)  | ✅ `Makefile`     |
| Just a Python app with CI needs       | ✅ `tox.ini`      |



# Note


# Reference

