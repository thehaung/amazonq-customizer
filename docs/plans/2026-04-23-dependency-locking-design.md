# Design: Strict Dependency Locking for Compliance

## Goal
Implement a robust dependency management system that ensures all installed Python packages (including transitive dependencies) are at least 24 hours old, complying with company security policy.

## Proposed Changes

### 1. Tooling
- Adopt `pip-tools` as the dependency locking mechanism.
- Use `pip-compile` to generate deterministic lock files from `pyproject.toml`.

### 2. Files
- **`pyproject.toml`**: Main source for dependency definitions and version ranges.
- **`requirements.txt`**: Production lock file containing all pinned dependencies.
- **`requirements-dev.txt`**: Development lock file containing all pinned dependencies including `dev` extras.

### 3. Workflow
1. Define top-level dependencies in `pyproject.toml`.
2. Generate lock files using `pip-compile`.
3. Verify that the resolved versions in the lock files are older than 24 hours via PyPI metadata.
4. Use `pip install -r requirements.txt` (or `-r requirements-dev.txt`) for all installations.

## Verification Plan
- Manually check the latest versions of `typer` and `pytest` (and their sub-dependencies) on PyPI.
- Ensure the generated lock files do not include any version released after 2026-04-22T22:08:17+07:00.
