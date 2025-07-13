# 🧼 tidycode

✨ A CLI utility to make your Python projects clean, organized, and compliant with DevSecOps best practices.

---

## 🚀 Main Features

- Fast setup for config files (`pyproject.toml`, `.pre-commit-config.yaml`, etc.)
- Linters & formatters support: `black`, `ruff`, `isort`, `mypy`
- Integrates `pre-commit`, `commitizen`, `safety`, `bandit`, and more
- Built with `Typer`: typed, simple, intuitive CLI
- Modular commands: quality, security, hooks, dependencies

---

## 🛠️ Installation

```bash
pip install tidycode
```

or

```bash
poetry add tidycode

poetry add -D tidycode
```

---

## 📦 Basic Usage

```bash
tidycode init
```

Automatically configures:
 - Black
 - Ruff
 - isort
 - mypy
 - Commitizen
 - pre-commit

## ✅ Code Quality

```bash
tidycode quality setup-all
```

Adds quality tools to pyproject.toml (black, ruff, etc.)

## 🤖 Pre-commit

```bash
tidycode hooks install
```

Installs .pre-commit-config.yaml and all hooks.

## 🔐 Security

```bash
tidycode security scan
```
Run security audits using safety and bandit.


## 🧪 Tests

```bash
pytest
```

```bash
pytest --cov=src
```

or simply

```bash
tidycode cov
```

## 📓 Commit Convention

```bash
tidycode commitizen bump
```
Automatically manages versioning and changelogs via Commitizen.

## 📄 License

This project is licensed under the MIT License.
