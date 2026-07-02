"""Backend implementations for the `pyrig-fixtures` CLI commands.

Each module implements one command as a plain callable, decoupled from the
CLI registration layer so it can be imported lazily when the command runs.
"""
