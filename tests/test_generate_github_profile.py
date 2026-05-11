import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image, ImageChops

REPO_ROOT    = Path(__file__).parent.parent
FIXTURES     = Path(__file__).parent / "fixtures"
EXPECTED_SIZE = (2048, 2048)

OUTPUTS = [
    REPO_ROOT / "assets" / "images" / "github-profile.png",
    REPO_ROOT / "assets" / "images" / "github-profile-simple.png",
]


@pytest.fixture(scope="module")
def script_result():
    return subprocess.run(
        [sys.executable, "scripts/generate_github_profile.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def test_smoke(script_result):
    assert script_result.returncode == 0, f"Script failed:\n{script_result.stderr}"


def test_outputs_exist(script_result):
    assert script_result.returncode == 0, f"Script failed:\n{script_result.stderr}"
    for path in OUTPUTS:
        assert path.exists(), f"Missing output: {path.name}"


def test_dimensions(script_result):
    assert script_result.returncode == 0, f"Script failed:\n{script_result.stderr}"
    for path in OUTPUTS:
        img = Image.open(path)
        assert img.size == EXPECTED_SIZE, f"{path.name}: expected {EXPECTED_SIZE}, got {img.size}"


def test_format(script_result):
    assert script_result.returncode == 0, f"Script failed:\n{script_result.stderr}"
    for path in OUTPUTS:
        img = Image.open(path)
        assert img.mode in ("RGB", "RGBA"), f"{path.name}: unexpected mode {img.mode}"
        size_kb = path.stat().st_size // 1024
        assert size_kb >= 20, f"{path.name}: file too small ({size_kb} KB) — may be blank or corrupt"


def test_regression(script_result):
    assert script_result.returncode == 0, f"Script failed:\n{script_result.stderr}"
    for path in OUTPUTS:
        fixture = FIXTURES / path.name
        assert fixture.exists(), f"No fixture for {path.name} — run: cp assets/images/{path.name} tests/fixtures/"
        img_new = Image.open(path).convert("RGB")
        img_ref = Image.open(fixture).convert("RGB")
        diff = ImageChops.difference(img_new, img_ref)
        assert diff.getbbox() is None, (
            f"{path.name} differs from fixture. "
            "If this change is intentional, update fixtures: cp assets/images/*.png tests/fixtures/"
        )
