# Test conventions (`tests/`)

Applies to everything under `tests/`. Canonical source: `.claude/rules/python-tools.md`; the full
discipline is in the `validation-standards` skill.

- **Tests land with the change.** Bug fix → regression test first. New seam → suite lands with it.
  CLI behaviour → subprocess pin with `PYTHONIOENCODING=utf-8`.
- **Tests never touch the three live DBs** — `:memory:` or `tmp_path` only. `KBStore` (intel.db)
  needs a tmp FILE, never `:memory:`.
- **No network in tests.** An autouse socket guard in `tests/conftest.py` blocks it; a test that
  genuinely needs it must be marked `@pytest.mark.network`. Four tests reached the live API for
  months while their docstrings claimed otherwise — that is the failure this prevents.
- **Fix ALL red tests, not just yours.** A missing dependency means `pip install`, never a mock,
  skip decorator, or `sys.modules` injection.
- **Absolute `tools.` imports only** — bare imports are the known collection-breaker.

Run from the repo root: `python -m pytest tests/ -q`.
