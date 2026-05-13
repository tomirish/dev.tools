# CI Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add MIT License, a two-job GitHub Actions CI workflow (lint + test), and Dependabot config to dev.tools.

**Architecture:** Two parallel jobs — `lint` runs ruff against `tools/` and `tests/`, `test` installs Playwright and runs pytest. Both use pinned action SHAs. Dependabot watches `pip` and `github-actions` weekly. MIT License covers code; OFL covers the bundled font.

**Tech Stack:** GitHub Actions, ruff, pytest, Playwright

---

### Task 1: Add MIT License

**Files:**
- Create: `LICENSE`

- [ ] **Step 1: Create `LICENSE` at repo root**

```
MIT License

Copyright (c) 2026 Tom Irish

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

`assets/DMSerifDisplay-Regular.ttf` is licensed under the SIL Open Font License 1.1.
See https://openfontlicense.org for details.
```

- [ ] **Step 2: Commit**

```bash
git add LICENSE
git commit -m "Add MIT License (font asset remains OFL)"
```

---

### Task 2: Create CI workflow


**Files:**
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Verify ruff passes locally**

Run from repo root:
```bash
pip install ruff
ruff check tools/ tests/
```
Expected: no output, exit code 0. If ruff flags anything, fix it before proceeding — CI will fail on the same issues.

- [ ] **Step 2: Create `.github/workflows/ci.yml`**

```bash
mkdir -p .github/workflows
```

Create `.github/workflows/ci.yml` with this exact content:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd  # v6.0.2
      - uses: actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405  # v6.2.0
        with:
          python-version: "3.12"
      - run: pip install ruff
      - run: ruff check tools/ tests/

  test:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd  # v6.0.2
      - uses: actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405  # v6.2.0
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: playwright install --with-deps chromium
      - run: pytest -v
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "Add CI workflow: lint (ruff) + test (pytest + Playwright)"
```

---

### Task 3: Create Dependabot config

**Files:**
- Create: `.github/dependabot.yml`

- [ ] **Step 1: Create `.github/dependabot.yml`**

```yaml
version: 2

updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
      day: monday
    labels: [dependencies]

  - package-ecosystem: pip
    directory: /
    schedule:
      interval: weekly
      day: monday
    labels: [dependencies]
```

- [ ] **Step 2: Commit**

```bash
git add .github/dependabot.yml
git commit -m "Add Dependabot: weekly pip + github-actions updates"
```

---

### Task 4: Push and verify

**Files:** none

- [ ] **Step 1: Push**

```bash
git push
```

- [ ] **Step 2: Watch CI run**

```bash
gh run list --repo tomirish/dev.tools --limit 5
```

Wait ~3 minutes for the test job (Playwright install is the slow part), then:

```bash
gh run watch --repo tomirish/dev.tools
```

- [ ] **Step 3: Confirm both jobs passed**

```bash
gh run list --repo tomirish/dev.tools --limit 1
```

Expected: `completed  success` for the most recent run. Both `lint` and `test` jobs should show green.

If either job fails, view logs:
```bash
gh run view --repo tomirish/dev.tools --log-failed
```
