# Home

<!-- ci/cd -->
[![CI](https://img.shields.io/github/actions/workflow/status/Winipedia/pyrig-fixtures/health_check.yml?label=CI&logo=github)](https://github.com/Winipedia/pyrig-fixtures/actions/workflows/health_check.yml)
[![CD](https://img.shields.io/github/actions/workflow/status/Winipedia/pyrig-fixtures/deploy.yml?label=CD&logo=github)](https://github.com/Winipedia/pyrig-fixtures/actions/workflows/deploy.yml)
<!-- testing -->
[![CoverageTester](https://codecov.io/gh/Winipedia/pyrig-fixtures/branch/main/graph/badge.svg)](https://codecov.io/gh/Winipedia/pyrig-fixtures)
[![ProjectTester](https://img.shields.io/badge/tested%20with-pytest-46a2f1.svg?logo=pytest)](https://pytest.org)
<!-- code-quality -->
[![DependencyAuditor](https://img.shields.io/badge/security-pip--audit-blue?logo=python)](https://github.com/pypa/pip-audit)
[![DependencyChecker](https://img.shields.io/badge/dependencies-deptry-blue)](https://github.com/osprey-oss/deptry)
[![MarkdownLinter](https://img.shields.io/badge/markdown-rumdl-darkgreen)](https://github.com/rvben/rumdl)
[![PythonLinter](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![SecurityChecker](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![SpellChecker](https://img.shields.io/badge/spell--check-typos-blue)](https://github.com/crate-ci/typos)
[![TypeChecker](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![VersionControlHookManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
<!-- tooling -->
[![PackageManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Pyrigger](https://img.shields.io/badge/built%20with-pyrig-3776AB?logo=buildkite&logoColor=black)](https://github.com/Winipedia/pyrig)
[![RemoteVersionController](https://img.shields.io/github/stars/Winipedia/pyrig-fixtures?style=social)](https://github.com/Winipedia/pyrig-fixtures)
[![VersionController](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white)](https://git-scm.com)
<!-- project-info -->
[![DocsBuilder](https://img.shields.io/badge/MkDocs-Documentation-326CE5?logo=mkdocs&logoColor=white)](https://Winipedia.github.io/pyrig-fixtures)
[![PackageIndex](https://img.shields.io/pypi/v/pyrig-fixtures?logo=pypi&logoColor=white)](https://pypi.org/project/pyrig-fixtures)
[![ProgrammingLanguage](https://img.shields.io/pypi/pyversions/pyrig-fixtures)](https://www.python.org)
[![License](https://img.shields.io/github/license/Winipedia/pyrig-fixtures)](https://github.com/Winipedia/pyrig-fixtures/blob/main/LICENSE)

---

> A pyrig plugin that provides pytest fixtures support.

---

## Overview

pyrig-fixtures provides a library of reusable pytest fixtures for testing
[pyrig](https://github.com/Winipedia/pyrig)-managed projects. Installed as a
development dependency, it makes fixtures available in every project's test
suite — its own and those contributed by any installed package that depends on
it — and adds a command for scaffolding new ones.

## Installation

```bash
uv add pyrig-fixtures --dev
uv run pyrig sync
```

## How it works

### Automatic, cross-package availability

The generated `tests/conftest.py` registers pyrig-fixtures' conftest as a pytest
plugin. That conftest registers, as pytest plugins, every fixture module in
pyrig-fixtures' `rig/tests/fixtures/` package **and** in the matching
`rig/tests/fixtures/` package of every installed package that depends on
pyrig-fixtures — discovered automatically, with no registration. All discovered
fixtures are then usable in any test without an explicit import.

Fixtures therefore compose across packages: any package that depends on
pyrig-fixtures contributes fixtures simply by placing them under its own
`rig/tests/fixtures/` package. Your own project is one such dependent, so the
fixtures you add there are picked up too.

### Scaffolding command

`pyrig mk fixture <name>` appends a new `@pytest.fixture` stub to your project's
shared fixtures module under `rig/tests/fixtures/`, creating it if needed — a
discovered location, so the new fixture is registered and available
automatically.

## API Reference

For class- and method-level details, see the [API Reference](api.md), generated
automatically from the source.
