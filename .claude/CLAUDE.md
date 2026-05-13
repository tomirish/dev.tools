# CLAUDE.md — Working notes for this repo

This file is gitignored and is just for us. Update it freely as we work together.

---

## Session start

When working in this repo, the global MEMORY.md is not auto-loaded. Read it manually at the start of each session:
`~/.claude/projects/-Users-tom-GitHub/memory/MEMORY.md`
Then read any topic files referenced in it — they contain important context.

---

## What this repo represents

**Philosophy:** Every repo Tom owns is held to the same standard. This is a personal toolbox, but it is also a deliberate learning tool and a leadership credibility artifact — the same as tom.irish. Tom shows his work to his team to demonstrate what's possible and to hold himself accountable. He won't ask his team to do something he isn't willing to do and learn himself.

**Purpose:** Tom uses this repo to produce real design artifacts (profile images, icons, etc.) and to practice the discipline of doing small things well: tested, documented, reproducible. The fact that a script runs once or twice a year is not a reason to cut corners.

**How this should inform decisions:** Never treat this as "just a personal script" when making tradeoffs. If something is worth doing on a production team codebase, it's worth doing here. The overhead and rigor are the point, not a side effect. Skipping something because it's "good enough for a personal tool" is the wrong frame.

---

## How Tom likes to work

**Focused and done right** — stay on the task at hand; don't add scope. But within the task, do it properly — no shortcuts, no hacks, no half-measures.

- Don't add features, abstractions, or error handling that the task doesn't require
- Build what's needed correctly; don't design for requirements that don't exist yet
- No dead code, no stale comments, no debugging artifacts
- Keep styling consistent with whatever's already in the file (indentation, naming, quote style, etc.)
- If something is unused, delete it — don't rename it or add a comment saying it was removed

**When in doubt, talk first** — if something is unclear, uncertain, or has multiple valid approaches, stop and discuss before making changes.

**Quality matters** — these scripts produce real artifacts used publicly (profile images, icons). They should work correctly and produce polished output. "Good enough" isn't the bar. Run tests, verify outputs visually, and confirm before considering anything done.

---

## What this repo is

A collection of standalone Python scripts that generate image assets. Each script uses Playwright to render HTML/CSS and screenshot the result at high resolution.

### Layout

- `scripts/` — scripts (each is standalone)
- `assets/fonts/` — shared fonts
- `assets/images/` — generated files (committed as design artifacts)
- `tests/` — pytest suite
- `tests/fixtures/` — golden reference images for regression testing

---

## Working on scripts

Parameters are at the top of each file in a clearly marked `# --- Parameters ---` block. Tweak and rerun — no other changes needed.

Scripts must be run from repo root:

```bash
python3 scripts/<script>.py
```

Each script deletes existing output and rebuilds on every run.

**Note:** `requirements.txt` includes playwright so CI can run `playwright install --with-deps chromium` after pip install. The README separately documents the `playwright install chromium` step for local use.

---

## Adding a new tool

When adding a new script, the full pattern is:

1. Add script to `scripts/` with a `# --- Parameters ---` block at the top
2. Write output to `assets/images/`
3. Add tests to `tests/test_<script_name>.py` — use the module-scoped fixture pattern from existing test files
4. Copy initial output to `tests/fixtures/` as the regression baseline
5. Update `README.md` — add to the Scripts table and Usage section

All five steps are required before a new tool is considered done.

---

## Tests

```bash
pip install -r requirements.txt
pytest
```

Tests follow a module-scoped fixture pattern: the script runs once per test file (not once per test), validated for smoke (exit 0), existence, dimensions, format/size, and exact pixel regression against `tests/fixtures/`.

**File size threshold is 20KB** (not 500KB) — solid-color PNG regions compress heavily; actual outputs are 20–75KB. Don't raise the threshold without checking actual file sizes first.

**No venv** — use system pip directly (`pip install -r requirements.txt`, `pytest`). Don't create a `.venv`.

**Updating fixtures** — when output changes intentionally:

```bash
cp assets/images/*.png tests/fixtures/
git add tests/fixtures/
git commit -m "Update test fixtures"
```

Always verify the new output visually before committing fixtures.

**Regression tests skip in CI** — `@skip_in_ci` uses `os.getenv("CI") == "true"` (set automatically by GitHub Actions). Playwright font rendering differs between macOS (CoreText) and Ubuntu (FreeType): ~0.18% of pixels, antialiasing edges only, visually identical. Don't remove the skip.

---

## Definition of done

Before any change is considered complete:

- [ ] `pytest` — all tests pass
- [ ] If a script changed: run it end-to-end and verify the output visually
- [ ] If output changed intentionally: fixtures updated and committed
- [ ] If a new tool was added: all five steps in "Adding a new tool" completed
- [ ] No dead code, no stale comments, no debugging artifacts
- [ ] `README.md` is accurate and up to date

---

## CI

Two jobs run in parallel on push to main and PRs:
- `lint` — `ruff check scripts/ tests/`
- `test` — `pytest -v` (regression tests skipped via `CI=true`)

Action SHAs are pinned; Dependabot updates pip + github-actions weekly on Mondays.
To debug CI image output: `gh run download <run-id> --repo tomirish/dev.tools --name <artifact-name> --dir /tmp/`

---

## Gotchas

**`rm` is blocked by the dippy hook** — use `git rm` for tracked files, `git rm -r` for directories. Don't chain `rm -rf` in a Bash command; it will be intercepted and fail.

---

## Backlog

- See `.claude/todo.md`
