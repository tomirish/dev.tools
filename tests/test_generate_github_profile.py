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
        assert size_kb >= 20, f"{path.name}: file too small ({size_kb} KB) — may be blank or corrupt"


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
