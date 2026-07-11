# pyrig-fixtures

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
[![SecretsChecker](https://img.shields.io/badge/secrets-detect--secrets-blue)](https://github.com/Yelp/detect-secrets)
[![SecurityLinter](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
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

pyrig-fixtures is a [pyrig](https://github.com/Winipedia/pyrig) plugin that
provides a library of reusable pytest fixtures for testing pyrig projects. Its
fixtures — and any contributed by packages that depend on it — are made
available automatically in every project that installs it.

## What it adds

- **A fixture library** — ready-made fixtures for common testing needs:
  temporary project trees, module and package creation, config-file testing,
  CLI-command assertions, and environment gating.
- **Automatic, cross-package availability** — fixtures are registered as a
  pytest plugin so they work without imports, and any installed package that
  depends on pyrig-fixtures contributes its own fixtures the same way.
- **A scaffolding command** — `pyrig mk fixture <name>` adds a new fixture stub
  to your project's shared fixtures module.

## Usage

```bash
uv add pyrig-fixtures --dev
uv run pyrig sync
```

## Documentation

Full documentation, including the auto-generated API reference, is available on
the [documentation site](https://Winipedia.github.io/pyrig-fixtures).
