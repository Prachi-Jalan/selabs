"""Hypothesis fuzz tests for gym_membership.py.

1. No-crash tests: random text / None must never raise an exception.
2. Property tests: valid generated inputs must give the correct answer.
"""
from hypothesis import given, settings, strategies as st
from gym_membership import parse_plan, calculate_bmi, average_workout


# ---------- 1. Fuzz: must never crash ----------
@settings(max_examples=500)
@given(st.text() | st.none())
def test_parse_plan_no_crash(s):
    try:
        parse_plan(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"parse_plan crashed on {s!r} with: {e!r}"


@settings(max_examples=500)
@given(st.text() | st.none())
def test_calculate_bmi_no_crash(s):
    try:
        calculate_bmi(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"calculate_bmi crashed on {s!r} with: {e!r}"


@settings(max_examples=500)
@given(st.text() | st.none())
def test_average_workout_no_crash(s):
    try:
        average_workout(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"average_workout crashed on {s!r} with: {e!r}"


# Targeted fuzzing: strings built from the characters these parsers care
# about, so Hypothesis hits commas, dashes, digits and spaces far more often.
@settings(max_examples=500)
@given(st.text(alphabet="0123456789-,. eEinfa", max_size=12))
def test_all_functions_no_crash_on_numeric_like_text(s):
    for func in (parse_plan, calculate_bmi, average_workout):
        try:
            func(s)
        except Exception as e:  # pylint: disable=broad-except
            assert False, f"{func.__name__} crashed on {s!r} with: {e!r}"


# ---------- 2. Properties on valid input ----------
@given(st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
               min_size=1, max_size=10),
       st.integers(min_value=1, max_value=120))
def test_parse_plan_valid(plan, months):
    assert parse_plan(f"{plan}-{months}") == (plan.upper(), months)


@given(st.integers(max_value=0))
def test_parse_plan_rejects_non_positive_months(months):
    assert parse_plan(f"GOLD-{months}") is None


@given(st.floats(min_value=20, max_value=300),
       st.floats(min_value=0.5, max_value=2.5))
def test_calculate_bmi_valid(weight, height):
    bmi = calculate_bmi(f"{weight},{height}")
    assert bmi is not None
    assert abs(bmi - weight / height ** 2) <= 0.05 + 1e-9


@given(st.floats(max_value=0) | st.just(0.0))
def test_calculate_bmi_rejects_non_positive_height(height):
    assert calculate_bmi(f"70,{height}") is None


@given(st.lists(st.integers(min_value=0, max_value=600), min_size=1))
def test_average_workout_valid(values):
    avg = average_workout(" ".join(map(str, values)))
    assert avg == sum(values) // len(values)
    assert min(values) <= avg <= max(values)


@given(st.just("") | st.text(alphabet=" \t\n"))
def test_average_workout_empty_input(s):
    assert average_workout(s) is None
