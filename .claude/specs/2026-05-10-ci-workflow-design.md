# CI Workflow Design

**Date:** 2026-05-10
**Repo:** dev.tools

## Overview

Add a GitHub Actions CI workflow that runs on every push to `main` and on every PR. Two parallel jobs: `lint` (ruff) and `test` (pytest + Playwright).

## Trigger

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

## Jobs

### `lint`

- Runner: `ubuntu-latest`
- Steps: checkout → setup Python 3.12 → `pip install ruff` → `ruff check tools/ tests/`
- No heavy dependencies; completes in ~30 seconds
- No ruff config file needed — defaults are appropriate for scripts this size

### `test`

- Runner: `ubuntu-latest`
- Steps: checkout → setup Python 3.12 → `pip install -r requirements.txt` → `playwright install --with-deps chromium` → `pytest -v`
- `--with-deps` installs system-level Playwright dependencies (same pattern as tom.irish)
- `output/` directory already exists in the repo (committed PNGs), no setup needed

## Action Versions

All GitHub Actions pinned to commit SHAs (not version tags), consistent with tom.irish's codeql.yml. Dependabot keeps them updated via the `github-actions` ecosystem.

## Dependabot

Add `github-actions` ecosystem to `.github/dependabot.yml` alongside the existing `pip` entry. Weekly on Mondays, same as tom.irish.

## Files

- Create: `.github/workflows/ci.yml`
- Create: `.github/dependabot.yml`

## Python Version

3.12 — current stable release.

## No Additional Config

No `pyproject.toml` or `ruff.toml` needed. ruff's defaults cover the codebase. No mypy — scripts are simple and unannotated; ruff catches what matters at this scale.
