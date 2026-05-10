# dev.tools

One-off utilities for generating design assets and other dev tasks.

## Scripts

| Script | Description |
|--------|-------------|
| `generate_github_profile.py` | Generates two 2048×2048 GitHub profile pictures (`github-profile.png`, `github-profile-simple.png`) |
| `generate_ti_element_icon.py` | Generates `ti-element.png` — a periodic-table-style element icon, browser-rendered via Playwright |

## Usage

```bash
python3 generate_github_profile.py
python3 generate_ti_element_icon.py
```

Each script deletes any existing output and rebuilds on every run. Tweak parameters at the top of each file and rerun to adjust.

`generate_ti_element_icon.py` requires Playwright (`pip install playwright && playwright install chromium`) and `DMSerifDisplay-Regular.ttf` (included).
