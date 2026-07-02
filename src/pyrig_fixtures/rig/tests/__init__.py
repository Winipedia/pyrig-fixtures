"""Pytest configuration root pooling fixtures across this package's dependents.

Fixtures defined in this package, and in the equivalent package of every
installed package depending on it, are collected and made available to test
suites without explicit imports.
"""
