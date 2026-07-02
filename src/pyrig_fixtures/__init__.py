"""Pytest fixture plugin for pyrig-managed projects.

Supplies a shared pool of pytest fixtures that pyrig's dependency-discovery
mechanism registers automatically in every dependent project's test suite,
along with the tooling to generate and extend that fixture set.
"""
