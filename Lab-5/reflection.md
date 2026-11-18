# Lab 5 – Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest were the Flake8 style issues: long lines, the `l=` spacing and the variable name `l`. They are mechanical and the tool says exactly which line and column. The hardest was the mutable default argument and the global `conn`. They aren't just style; I had to understand how the function was being called (`totals` was passed back in on purpose) to make sure changing `extras={}` to `None` didn't change the output. Moving the database out of global scope also meant touching every function.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Yes, partly. Bandit flagged `hashlib.md5` as a high-severity weak hash, but here MD5 only makes a short 6-character display ID for an observer. It isn't used for passwords or security. So the risk Bandit describes doesn't apply. I kept MD5, so the IDs stay the same, and marked it `usedforsecurity=False`, which tells both Bandit and the reader that this is intentional. The `assert` warning (B101) is also low risk in a demo script, but replacing it was still better practice.

**3. How would you integrate static analysis tools into your actual software development workflow?**

Run Flake8 and Pylint locally through a pre-commit hook so style problems never get committed, and run all three tools, Bandit included, in a CI pipeline (for example GitHub Actions) on every push or pull request. The build would fail on Bandit medium/high findings or a Pylint score below a threshold such as 9.5. Editor plugins in VS Code can show the same warnings while typing, which is cheaper than finding them later.

**4. What tangible improvements did you observe in code quality, readability, or robustness after applying the fixes?**

- **Security/robustness:** the parameterised query stops SQL injection. Names with apostrophes like `O'Brien's owl` now work instead of crashing.
- **Correctness:** each `log_sighting` call without a `totals` dict now gets a fresh one instead of a hidden shared dict.
- **Readability:** snake_case names, docstrings and shorter lines make the code easier to read. Pylint went from a low score to 10/10, and Flake8 and Bandit report no issues.
- **Reusability:** no database is created at import time, so the module can be imported or tested without side effects.
