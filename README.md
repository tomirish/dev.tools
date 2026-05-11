# dev.tools

One-off utilities for generating design assets and other dev tasks.

## Structure

```
assets/   — shared resources (fonts, etc.)
output/   — generated files (committed as design artifacts)
tools/    — scripts
```

## Scripts

### `tools/generate_github_profile.py`

Generates two 2048×2048 GitHub profile pictures:

- `output/github-profile.png` — Ti element card with cream border ring
- `output/github-profile-simple.png` — same layout, no border (cleaner at small sizes)

### `tools/generate_ti_element_icon.py`

Generates `output/ti-element.png` — a periodic-table-style element icon, browser-rendered via Playwright to match icon.kitchen's faux-bold rendering exactly.

## Usage

Run from the repo root:

```bash
python3 tools/generate_github_profile.py
python3 tools/generate_ti_element_icon.py
```

Each script deletes any existing output and rebuilds on every run. Tweak the parameters at the top of each file and rerun to adjust.

## Dependencies

Both scripts require Playwright:

```bash
pip install playwright && playwright install chromium
```

`assets/DMSerifDisplay-Regular.ttf` is included in the repo.
