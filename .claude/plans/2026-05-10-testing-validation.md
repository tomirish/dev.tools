# Testing & Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a pytest + Pillow test suite that catches runtime failures, format errors, and visual regressions for both image-generation scripts.

**Architecture:** Each script gets its own test file. Tests run the script via subprocess, then use Pillow to validate dimensions/format/size, and do an exact pixel comparison against committed fixture images in `tests/fixtures/`.

**Tech Stack:** Python, pytest, Pillow (`PIL`), subprocess

---

### Task 1: Scaffold test infrastructure

**Files:**
- Create: `requirements-dev.txt`
- Create: `tests/__init__.py`
- Create: `tests/fixtures/` (directory with copied PNGs)

- [ ] **Step 1: Create `requirements-dev.txt`**

```
pytest
Pillow
```

- [ ] **Step 2: Install dependencies**

```bash
pip install -r requirements-dev.txt
```

Expected: both packages install without error.

- [ ] **Step 3: Copy current outputs to fixtures**

```bash
mkdir -p tests/fixtures
cp output/github-profile.png tests/fixtures/
cp output/github-profile-simple.png tests/fixtures/
cp output/ti-element.png tests/fixtures/
```

- [ ] **Step 4: Create empty `tests/__init__.py`**

Create `tests/__init__.py` as an empty file.

- [ ] **Step 5: Verify fixture files exist**

```bash
ls tests/fixtures/
```

Expected:
```
github-profile-simple.png  github-profile.png  ti-element.png
```

- [ ] **Step 6: Commit**

```bash
git add requirements-dev.txt tests/
git commit -m "Add test scaffold: fixtures and requirements-dev.txt"
```

---

### Task 2: Tests for `generate_github_profile.py`

**Files:**
- Create: `tests/test_generate_github_profile.py`

- [ ] **Step 1: Write the test file**

Create `tests/test_generate_github_profile.py`:

```python
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops

REPO_ROOT = Path(__file__).parent.parent
FIXTURES  = Path(__file__).parent / "fixtures"

OUTPUTS = [
    REPO_ROOT / "output" / "github-profile.png",
    REPO_ROOT / "output" / "github-profile-simple.png",
]


def run_script():
    result = subprocess.run(
        [sys.executable, "tools/generate_github_profile.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return result


def test_smoke():
    result = run_script()
    assert result.returncode == 0, f"Script failed:\n{result.stderr}"


def test_outputs_exist():
    run_script()
    for path in OUTPUTS:
        assert path.exists(), f"Missing output: {path.name}"


def test_dimensions():
    run_script()
    for path in OUTPUTS:
        img = Image.open(path)
        assert img.size == (2048, 2048), f"{path.name}: expected 2048x2048, got {img.size}"


def test_format():
    run_script()
    for path in OUTPUTS:
        img = Image.open(path)
        assert img.mode in ("RGB", "RGBA"), f"{path.name}: unexpected mode {img.mode}"
        size_kb = path.stat().st_size // 1024
        assert size_kb >= 500, f"{path.name}: file too small ({size_kb} KB) — may be blank or corrupt"


def test_regression():
    run_script()
    for path in OUTPUTS:
        fixture = FIXTURES / path.name
        assert fixture.exists(), f"No fixture for {path.name} — run: cp output/{path.name} tests/fixtures/"
        img_new = Image.open(path).convert("RGB")
        img_ref = Image.open(fixture).convert("RGB")
        diff = ImageChops.difference(img_new, img_ref)
        assert diff.getbbox() is None, (
            f"{path.name} differs from fixture. "
            "If this change is intentional, update fixtures: cp output/*.png tests/fixtures/"
        )
```

- [ ] **Step 2: Run the tests to verify they pass**

```bash
pytest tests/test_generate_github_profile.py -v
```

Expected: 5 tests pass — `test_smoke`, `test_outputs_exist`, `test_dimensions`, `test_format`, `test_regression`.

- [ ] **Step 3: Commit**

```bash
git add tests/test_generate_github_profile.py
git commit -m "Add tests for generate_github_profile.py"
```

---

### Task 3: Tests for `generate_ti_element_icon.py`

**Files:**
- Create: `tests/test_generate_ti_element_icon.py`

- [ ] **Step 1: Write the test file**

Create `tests/test_generate_ti_element_icon.py`:

```python
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops

REPO_ROOT = Path(__file__).parent.parent
FIXTURES  = Path(__file__).parent / "fixtures"

OUTPUT = REPO_ROOT / "output" / "ti-element.png"


def run_script():
    result = subprocess.run(
        [sys.executable, "tools/generate_ti_element_icon.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return result


def test_smoke():
    result = run_script()
    assert result.returncode == 0, f"Script failed:\n{result.stderr}"


def test_output_exists():
    run_script()
    assert OUTPUT.exists(), f"Missing output: {OUTPUT.name}"


def test_dimensions():
    run_script()
    img = Image.open(OUTPUT)
    assert img.size == (2048, 2048), f"Expected 2048x2048, got {img.size}"


def test_format():
    run_script()
    img = Image.open(OUTPUT)
    assert img.mode in ("RGB", "RGBA"), f"Unexpected mode: {img.mode}"
    size_kb = OUTPUT.stat().st_size // 1024
    assert size_kb >= 500, f"File too small ({size_kb} KB) — may be blank or corrupt"


def test_regression():
    run_script()
    fixture = FIXTURES / OUTPUT.name
    assert fixture.exists(), f"No fixture for {OUTPUT.name} — run: cp output/{OUTPUT.name} tests/fixtures/"
    img_new = Image.open(OUTPUT).convert("RGB")
    img_ref = Image.open(fixture).convert("RGB")
    diff = ImageChops.difference(img_new, img_ref)
    assert diff.getbbox() is None, (
        f"{OUTPUT.name} differs from fixture. "
        "If this change is intentional, update fixtures: cp output/*.png tests/fixtures/"
    )
```

- [ ] **Step 2: Run the tests to verify they pass**

```bash
pytest tests/test_generate_ti_element_icon.py -v
```

Expected: 5 tests pass — `test_smoke`, `test_output_exists`, `test_dimensions`, `test_format`, `test_regression`.

- [ ] **Step 3: Commit**

```bash
git add tests/test_generate_ti_element_icon.py
git commit -m "Add tests for generate_ti_element_icon.py"
```

---

### Task 4: Full suite run and README update

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Run the full suite**

```bash
pytest -v
```

Expected: 10 tests pass across both files.

- [ ] **Step 2: Add a Testing section to `README.md`**

Append to `README.md` after the Dependencies section:

```markdown
## Testing

```bash
pip install -r requirements-dev.txt
pytest
```

Tests run both scripts and validate each output for correct dimensions (2048×2048), file format, minimum file size, and exact pixel match against reference images in `tests/fixtures/`.

To update fixtures after an intentional parameter change:

```bash
cp output/*.png tests/fixtures/
git add tests/fixtures/
git commit -m "Update test fixtures"
```
```

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "Document test suite in README"
```
