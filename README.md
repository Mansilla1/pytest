# Pytest-Test

## 📌 Project Overview

This project is configured to **run automated tests with Pytest**, perform **static code analysis** with **Ruff and MyPy**, check **code coverage**, and scan for potential secrets using **Talisman**. It is also integrated with **GitHub Actions** to ensure quality on every `push` or `pull request`.

---

## 🛠️ **Setup & Dependencies**

This project uses **Poetry** for dependency management. To install dependencies, run:

```sh
make install
```

Main dependencies:
- `pytest` → Testing framework.
- `pytest-cov` → Code coverage reports.
- `ruff` → Linter and formatter.
- `mypy` → Static type checker.
- `pre-commit` → Automatic pre-commit hooks.
- `talisman` → Security scanner for secrets.

---

## 🚀 **Available Commands**

The project includes a `Makefile` to streamline execution of key tools.

### 🔹 **Pre-commit Hooks**
Run all pre-commit hooks:
```sh
make pre-commit
```
This will execute **Ruff, MyPy, and Talisman** before committing code.

### 🔹 **Run Tests**
Execute all tests with Pytest:
```sh
make test
```
This also generates a **code coverage report**.

### 🔹 **Linting and Formatting**
Run Ruff to check and format the code:
```sh
make ruff-checker
```

### 🔹 **Static Analysis with MyPy**
Run **MyPy** to check static types:
```sh
make mypy
```

### 🔹 **Generate and View Coverage Report**
Run tests with coverage and generate an **HTML** report:
```sh
make test
```
To view the report in the browser:
```sh
make coverage-report
```
Then, open [http://localhost:8080](http://localhost:8080).

### 🔹 **Secret Scanning with Talisman**
Run Talisman to detect secrets in the code:
```sh
make talisman-report
```
This will generate a report and serve it locally on port 8080.

---

## 🏗️ **CI/CD Integration with GitHub Actions**

The project is configured with **GitHub Actions** to automatically run checks on every `push` or `pull request`.

📌 **Implemented Workflows:**
- ✅ **Linting** → Runs `Ruff` and `MyPy`.
- ✅ **Testing** → Runs `pytest` and generates a coverage report.
- ✅ **Coverage Report** → Uploaded as an `artifact` on each execution.
- ✅ **Code Security Scan** → Runs Talisman to check for secrets.

### **📂 Artifacts in GitHub Actions**
Reports generated in each pipeline execution can be downloaded from the **Artifacts** section in GitHub Actions:
- 🔹 `coverage-report` → HTML coverage report.
- 🔹 `talisman-report` → Security report from Talisman.

---

## 🎯 **Project Structure**

```
.
├── Makefile                # Automated commands
├── README.md               # Project documentation
├── poetry.lock             # Dependencies
├── pyproject.toml          # Poetry and tool configurations
├── src/                    # Source code
│   ├── __init__.py
│   └── main.py
└── tests/                  # Tests
    ├── __init__.py
    ├── conftest.py
    └── test_main.py
```

