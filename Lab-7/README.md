# Lab 7 – Fuzz Testing with Hypothesis (PES1UG24CS326, Prachi Jalan)

Source repo: https://github.com/SETAPESU26/L6_L7_21_gym_membership (folder `Lab 7`)
In this repo `gym_membership.py` = the handout's `processor.py`, and
`test_gym_membership.py` = `test_processor.py`.

## Bugs found by fuzzing (original code)
| Function | Crashing input (examples) | Exception | Fix |
|---|---|---|---|
| all three | `None` | AttributeError (`.split` on None) | Return None if input is not a string |
| `parse_plan` | `''`, `GOLD`, `A-B-C` | ValueError (unpacking) | Require exactly one `-` |
| `parse_plan` | `GOLD-x` | ValueError (`int`) | try/except around `int()` |
| `parse_plan` | `-12`, `GOLD-0` | wrong result (empty plan / 0 months) | Reject empty plan and months <= 0 |
| `calculate_bmi` | `8`, `1,2,3`, `a,b` | ValueError | Require exactly two numbers, try/except `float()` |
| `calculate_bmi` | `70,0`, `1,1e-200` | ZeroDivisionError | Reject height <= 0, catch division errors |
| `calculate_bmi` | `1,1e200` | OverflowError (`height ** 2`) | catch OverflowError |
| `calculate_bmi` | `70,nan`, `inf,1.7` | nonsense result | Reject non-finite numbers |
| `average_workout` | `''`, `'   '` | ZeroDivisionError (`len == 0`) | Return None for empty input |
| `average_workout` | `abc`, `4.5` | ValueError (`int`) | try/except around `int()` |
| `average_workout` | `-30 20` | wrong result | Reject negative minutes |

Fixed functions return `None` for invalid input instead of crashing; `main()` prints a
friendly "Invalid ..." message.

## Tests (`test_gym_membership.py`)
- 3 no-crash fuzz tests (`st.text() | st.none()`, 500 examples each) – the handout's required tests.
- 1 targeted fuzz test using only digits, `-`, `,`, `.`, spaces, `e`, `inf`, `nan`.
- 6 property tests: valid inputs give the correct answer; zero/negative values are rejected.

Run: `python3 -m pytest test_gym_membership.py`
