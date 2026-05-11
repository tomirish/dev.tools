# Testing & Validation Design

**Date:** 2026-05-10
**Repo:** dev.tools

## Overview

Add a pytest-based test suite that catches four failure modes for the two image-generation scripts: silent failures (wrong output), runtime failures (script crashes), format errors (corrupt/blank output), and visual regressions (output changed unexpectedly).

## Structure

```
tests/
  fixtures/
    github-profile.png          — golden reference image
    github-profile-simple.png   — golden reference image
    ti-element.png              — golden reference image
  test_generate_github_profile.py
  test_generate_ti_element_icon.py
requirements-dev.txt
```

`tests/fixtures/` contains committed copies of the current known-good outputs. These are the regression baseline.

## Dependencies

`requirements-dev.txt`:
```
pytest
Pillow
```

## Test Coverage

Each script gets its own test file. Both follow the same pattern:

1. **Smoke** — run the script via `subprocess.run` from repo root, assert return code 0
2. **Existence** — assert all expected output files exist after the run
3. **Dimensions** — open each PNG with Pillow, assert 2048×2048
4. **Format** — assert mode is `RGB` or `RGBA`; assert file size > 500 KB (catches blank/corrupt renders)
5. **Regression** — use `ImageChops.difference()` between fresh output and fixture; assert diff bounding box is `None` (exact pixel match)

### `test_generate_github_profile.py`

Covers: `output/github-profile.png`, `output/github-profile-simple.png`

### `test_generate_ti_element_icon.py`

Covers: `output/ti-element.png`

## Running Tests

```bash
pytest
```

Run from repo root. Tests invoke the scripts via subprocess, so Playwright and `chromium` must be installed.

## Updating Fixtures

When output parameters change intentionally:

1. Run the scripts to regenerate outputs
2. Manually verify the new outputs look correct
3. `cp output/*.png tests/fixtures/`
4. Commit the updated fixtures

This is a deliberate, manual step — fixture updates should always be a conscious decision.
