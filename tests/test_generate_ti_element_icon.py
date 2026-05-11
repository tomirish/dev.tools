import os
import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image, ImageChops

skip_in_ci = pytest.mark.skipif(os.getenv("CI") == "true", reason="Font rendering differs across platforms")

REPO_ROOT    = Path(__file__).parent.parent
FIXTURES     = Path(__file__).parent / "fixtures"
EXPECTED_SIZE = (2048, 2048)

OUTPUT = REPO_ROOT / "assets" / "images" / "ti-element.png"


@pytest.fixture(scope="module")
def script_result():
    return subprocess.run(
        [sys.executable, "scripts/generate_ti_element_icon.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def test_smoke(script_result):
    assert script_result.returncode == 0, f"Script failed:\n{script_result.stderr}"


def test_output_exists(script_result):
    assert script_result.returncode == 0, f"Script failed:\n{script_result.stderr}"
    assert OUTPUT.exists(), f"Missing output: {OUTPUT.name}"


def test_dimensions(script_result):
    assert script_result.returncode == 0, f"Script failed:\n{script_result.stderr}"
    img = Image.open(OUTPUT)
    assert img.size == EXPECTED_SIZE, f"{OUTPUT.name}: expected {EXPECTED_SIZE}, got {img.size}"


def test_format(script_result):
    assert script_result.returncode == 0, f"Script failed:\n{script_result.stderr}"
    img = Image.open(OUTPUT)
    assert img.mode in ("RGB", "RGBA"), f"{OUTPUT.name}: unexpected mode {img.mode}"
    size_kb = OUTPUT.stat().st_size // 1024
    assert size_kb >= 20, f"{OUTPUT.name}: file too small ({size_kb} KB) — may be blank or corrupt"


@skip_in_ci
def test_regression(script_result):
    assert script_result.returncode == 0, f"Script failed:\n{script_result.stderr}"
    fixture = FIXTURES / OUTPUT.name
    assert fixture.exists(), f"No fixture for {OUTPUT.name} — run: cp assets/images/{OUTPUT.name} tests/fixtures/"
    img_new = Image.open(OUTPUT).convert("RGB")
    img_ref = Image.open(fixture).convert("RGB")
    diff = ImageChops.difference(img_new, img_ref)
    assert diff.getbbox() is None, (
        f"{OUTPUT.name} differs from fixture. "
        "If this change is intentional, update fixtures: cp assets/images/*.png tests/fixtures/"
    )
