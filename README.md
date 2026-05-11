# dev.tools

[![CI](https://github.com/tomirish/dev.tools/actions/workflows/ci.yml/badge.svg)](https://github.com/tomirish/dev.tools/actions/workflows/ci.yml)

One-off utilities for generating design assets and other dev tasks.

## Structure

```
assets/fonts/   — shared fonts
assets/images/  — generated image files (committed as design artifacts)
scripts/        — scripts
tests/          — pytest suite
```

## Scripts

| Script | Output |
|---|---|
| [`scripts/generate_github_profile.py`](scripts/generate_github_profile.py) | [<img src="assets/images/github-profile.png" width="80">](assets/images/github-profile.png) [<img src="assets/images/github-profile-simple.png" width="80">](assets/images/github-profile-simple.png) |
| [`scripts/generate_ti_element_icon.py`](scripts/generate_ti_element_icon.py) | [<img src="assets/images/ti-element.png" width="80">](assets/images/ti-element.png) |

## Usage

Run from the repo root:

```bash
python3 scripts/generate_github_profile.py
python3 scripts/generate_ti_element_icon.py
```

Each script deletes any existing output and rebuilds on every run. Tweak the parameters at the top of each file and rerun to adjust.

## Dependencies

Both scripts require Playwright:

```bash
pip install playwright && playwright install chromium
```

`assets/fonts/DMSerifDisplay-Regular.ttf` is included in the repo.

## Testing

```bash
pip install -r requirements.txt
pytest
```

Tests run both scripts and validate each output for correct dimensions (2048×2048), file format, minimum file size, and exact pixel match against reference images in `tests/fixtures/`.

To update fixtures after an intentional parameter change:

```bash
cp assets/images/*.png tests/fixtures/
git add tests/fixtures/
git commit -m "Update test fixtures"
```
