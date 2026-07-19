# Home

<!-- project-status -->
[![CI](https://img.shields.io/github/actions/workflow/status/Winipedia/pyrig-fixtures/health_check.yml?label=CI&logo=github)](https://github.com/Winipedia/pyrig-fixtures/actions/workflows/health_check.yml)
[![CD](https://img.shields.io/github/actions/workflow/status/Winipedia/pyrig-fixtures/deploy.yml?label=CD&logo=github)](https://github.com/Winipedia/pyrig-fixtures/actions/workflows/deploy.yml)
[![ProjectTester](https://codecov.io/gh/Winipedia/pyrig-fixtures/branch/main/graph/badge.svg)](https://codecov.io/gh/Winipedia/pyrig-fixtures)
<!-- code-quality -->
[![ByteOrderMarkerFormatter](https://img.shields.io/badge/BOM-fix--byte--order--marker-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![CaseConflictChecker](https://img.shields.io/badge/case--conflict-check--case--conflict-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![DependencyAuditor](https://img.shields.io/badge/security-pip--audit-blue?logo=python)](https://github.com/pypa/pip-audit)
[![DependencyChecker](https://img.shields.io/badge/dependencies-deptry-blue)](https://github.com/osprey-oss/deptry)
[![EndOfFileFormatter](https://img.shields.io/badge/EOF-end--of--file--fixer-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![EndOfLineFormatter](https://img.shields.io/badge/EOL-mixed--line--ending-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![JSONFormatter](https://img.shields.io/badge/JSON-pretty--format--json-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![JSONLinter](https://img.shields.io/badge/JSON-check--json-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![LargeFileChecker](https://img.shields.io/badge/large--files-check--added--large--files-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![MarkdownLinter](https://img.shields.io/badge/Markdown-rumdl-darkgreen)](https://github.com/rvben/rumdl)
[![MergeConflictChecker](https://img.shields.io/badge/merge--conflict-check--merge--conflict-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![ModuleTestNamingChecker](https://img.shields.io/badge/test--naming-name--tests--test-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![PythonLinter](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![SecretsChecker](https://img.shields.io/badge/secrets-detect--secrets-blue)](https://github.com/Yelp/detect-secrets)
[![SecurityChecker](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![ShellFormatter](https://img.shields.io/badge/shell-shfmt-orange)](https://github.com/mvdan/sh)
[![ShellLinter](https://img.shields.io/badge/shell-shellcheck-blue)](https://github.com/koalaman/shellcheck)
[![SpellChecker](https://img.shields.io/badge/spell--check-typos-blue)](https://github.com/crate-ci/typos)
[![TOMLLinter](https://img.shields.io/badge/TOML-tombi-blueviolet)](https://github.com/tombi-toml/tombi)
[![TrailingWhitespaceFormatter](https://img.shields.io/badge/whitespace-trailing--whitespace--fixer-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![TypeChecker](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![YAMLLinter](https://img.shields.io/badge/YAML-ryl-red)](https://github.com/owenlamont/ryl)
<!-- tooling -->
[![PackageManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Pyrigger](https://img.shields.io/badge/built%20with-pyrig-3776AB?logo=buildkite&logoColor=black)](https://github.com/Winipedia/pyrig)
[![RemoteVersionController](https://img.shields.io/github/stars/Winipedia/pyrig-fixtures?style=social)](https://github.com/Winipedia/pyrig-fixtures)
[![VersionControlHookManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
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

### End-to-end project initialization check

`init_pyrig_project` is a session-scoped, autouse fixture contributed by
pyrig-fixtures itself, so every project that depends on it runs it once per
test session automatically. It exercises the full pyrig lifecycle end to end:
building the package as a wheel, initializing a scratch project with it
installed as a pyrig plugin, and verifying that everything works as intended.

Because it does a real build, git init, and `uv sync`, it's slow. Pass
`--skip-init-pyrig-project` (or its short alias `--sipp`) to skip it for a
faster local feedback loop.

## API Reference

For class- and method-level details, see the [API Reference](api.md), generated
automatically from the source.
