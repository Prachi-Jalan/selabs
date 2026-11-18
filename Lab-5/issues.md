# Lab 5 – Static Code Analysis: Issue Table

**File:** `wildlife_sightings.py` (repo: SETAPESU26/L5_21_wildlife_sightings)
**Student:** Prachi Jalan, PES1UG24CS326

| # | Issue | Tool / Code | Type | Severity | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|----------|---------|-------------|--------------|
| 1 | SQL injection | Bandit B608 | Security | Medium | 9 | INSERT built with `str.format()`, so a species/zone value can change the SQL. A name like `O'Brien's owl` breaks the query. | Parameterised query with `?` placeholders and a values tuple. |
| 2 | Weak hash (MD5) | Bandit B324 | Security | High | 15 | `hashlib.md5()` is flagged as insecure. Here it only makes a short display ID, not a password or signature. | Kept MD5 (so IDs don't change) but marked it `usedforsecurity=False`. |
| 3 | Use of `assert` | Bandit B101 | Security / Bug | Low | 36 | `assert` is removed when Python runs with `-O`, so the check silently disappears. | Replaced with `if ...: raise RuntimeError(...)`. |
| 4 | Mutable default argument | Pylint W0102 | Bug | Medium | 8 | `extras={}` is created once and shared by every call, so totals leak between unrelated calls. | Default to `None` and create a new dict inside the function. |
| 5 | Redefined outer name `conn` | Pylint W0621 | Code smell | Medium | 4, 8, 18, 26 | Global `conn` shadowed by every function parameter; DB created at import time. | Moved DB setup into `create_db()`, called from `main()`; parameter renamed `db`. |
| 6 | Naming convention | Pylint C0103 | Style | Low | 8, 14, 18, 28 | camelCase function names (`logSighting`, `observerId`, `zoneSummary`) and one-letter `l`. | Renamed to snake_case: `log_sighting`, `observer_id`, `zone_summary`, `least`. |
| 7 | Missing docstrings | Pylint C0114 / C0116 | Documentation | Low | 1, all functions | No module or function docstrings. | Added a module docstring and one per function. |
| 8 | Unnecessary `else` after `return` | Pylint R1705 | Refactor | Low | 20–23 | `else` after a `return` adds nesting for nothing. | Removed `else`; return directly. |
| 9 | Format string | Pylint C0209 | Style | Low | 9 | `.format()` instead of f-string. | Gone with fix #1 (no string formatting in SQL at all). |
| 10 | Code runs on import | Pylint (best practice) | Design | Low | 40 | `main()` runs whenever the module is imported. | Wrapped in `if __name__ == "__main__":`. |
| 11 | Lines too long | Flake8 E501 / Pylint C0301 | Style | Low | 5, 9, 19, 27 | Lines of 93–117 chars, PEP 8 limit is 79. | Split SQL strings and calls across lines. |
| 12 | Ambiguous variable name `l` | Flake8 E741 | Style | Low | 28 | `l` looks like `1` / `I`. | Renamed to `least`. |
| 13 | Missing whitespace around operator | Flake8 E225 | Style | Low | 28 | `l=min(...)` | `least = min(...)` |

**Behaviour check:** before and after, the program prints `5455c3 25 Leopard`.
