# Lab 6 – Code and Branch Coverage (PES1UG24CS326, Prachi Jalan)

Source repo: https://github.com/SETAPESU26/L6_L7_21_gym_membership (folder `Lab 6`)

| File | Purpose |
|------|---------|
| `gym_membership.py` | Module under test (unchanged) |
| `test_gym_membership.py` | Starter tests (unchanged) |
| `CodeCoverageTest_PES1UG24CS326_gym_membership.py` | Tests that run every line (100% line coverage) |
| `BranchCoverageTest_PES1UG24CS326_gym_membership.py` | Tests that take every branch both ways + boundary values (100% branch coverage) |
| `screenshots/` | Terminal output of the coverage reports |

## Commands
    pip install coverage pytest

    # Code (line) coverage
    coverage run -m pytest CodeCoverageTest_PES1UG24CS326_gym_membership.py
    coverage report -m

    # Branch coverage
    coverage run --branch -m pytest BranchCoverageTest_PES1UG24CS326_gym_membership.py
    coverage report -m

## Line vs branch
The code-coverage tests reach 100% of lines but miss one branch: `if plan == "yearly"`
is only ever True (a yearly plan with a trainer). The branch-coverage file adds a
monthly plan with a trainer (False path), plus boundary cases such as age 14/59/60,
hours 4/5/22/23, women-only slot with a male member, and BMI exactly 18.5/25/30.
