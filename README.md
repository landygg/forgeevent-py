# forgeevent

[![Release](https://img.shields.io/github/v/release/landygg/forgeevent-py)](https://github.com/landygg/forgeevent-py/releases)
[![Build status](https://img.shields.io/github/actions/workflow/status/landygg/forgeevent-py/main.yml?branch=main)](https://github.com/landygg/forgeevent-py/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/landygg/forgeevent-py/branch/main/graph/badge.svg)](https://codecov.io/gh/landygg/forgeevent-py)
[![Commit activity](https://img.shields.io/github/commit-activity/m/landygg/forgeevent-py)](https://github.com/landygg/forgeevent-py/graphs/commit-activity)
[![License](https://img.shields.io/github/license/landygg/forgeevent-py)](LICENSE)

**forgeevent** is a Python library for event management and dispatching, designed to be simple, flexible, and extensible.

- **GitHub repository:** [https://github.com/landygg/forgeevent-py/](https://github.com/landygg/forgeevent-py/)
- **Documentation:** [https://landygg.github.io/forgeevent/](https://landygg.github.io/forgeevent/)

---

## Features

- Simple and intuitive event registration and dispatching
- Flexible event handler system
- Extensible for custom event types and workflows
- Python 3.12+ support

## Installation

```bash
pip install forgeevent
```

Or, for development:

```bash
git clone https://github.com/landygg/forgeevent-py.git
cd forgeevent-py
make install
```

## Usage

See the [documentation](https://landygg.github.io/forgeevent/) for more examples and API details.

## Getting Started for Development

1. **Clone the repository:**
    ```bash
    git clone https://github.com/landygg/forgeevent-py.git
    cd forgeevent-py
    ```

2. **Install dependencies and pre-commit hooks:**
    ```bash
    make install
    ```

3. **Run pre-commit hooks:**
    ```bash
    uv run pre-commit run -a
    ```

4. **Commit any formatting changes:**
    ```bash
    git add .
    git commit -m "Fix formatting issues"
    git push origin main
    ```

## Running Tests

To run all tests:

```bash
make test
```

Or directly with pytest:

```bash
uv run pytest
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

- Report bugs or request features via [GitHub Issues](https://github.com/landygg/forgeevent-py/issues).
- Pull requests should include tests and documentation updates as appropriate.

---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
