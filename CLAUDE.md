# dev.tools

One-off utilities for generating design assets.

## Layout

- `tools/` — scripts (each is standalone)
- `assets/` — shared resources (fonts)
- `output/` — generated files (committed as design artifacts)
- `tests/` — pytest suite

## Working on scripts

Parameters are at the top of each file in a clearly marked block. Tweak and rerun — no other changes needed.

Scripts must be run from repo root:

```bash
python3 tools/<script>.py
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

When output changes intentionally, update fixtures before committing:

```bash
cp output/*.png tests/fixtures/
```
