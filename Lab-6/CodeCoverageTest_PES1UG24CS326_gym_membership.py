"""Code (line) coverage tests for gym_membership.py.

Goal: every line of gym_membership.py runs at least once.
Run:  coverage run -m pytest CodeCoverageTest_PES1UG24CS326_gym_membership.py
      coverage report -m
"""
import pytest
from gym_membership import membership_cost, can_enter, bmi_category


# ---------- membership_cost ----------
def test_monthly_plan():
    assert membership_cost("monthly", 30, False, False) == 1500


def test_unknown_plan_raises():
    with pytest.raises(ValueError, match="unknown plan"):
        membership_cost("weekly", 30, False, False)


def test_too_young_raises():
    with pytest.raises(ValueError, match="too young"):
        membership_cost("monthly", 10, False, False)


def test_senior_discount():
    # 25% off: 1500 - 375
    assert membership_cost("monthly", 65, False, False) == 1125


def test_student_discount():
    # 10% off: 4000 - 400
    assert membership_cost("quarterly", 20, True, False) == 3600


def test_yearly_with_trainer():
    # 12000 + 2000 trainer - 500 yearly trainer discount
    assert membership_cost("yearly", 30, False, True) == 13500


# ---------- can_enter ----------
def test_can_enter():
    assert can_enter(10, True, False, "M") is True


def test_inactive_plan_cannot_enter():
    assert can_enter(10, False, False, "M") is False


def test_outside_hours_cannot_enter():
    assert can_enter(3, True, False, "M") is False


def test_women_only_slot_female():
    assert can_enter(10, True, True, "F") is True


# ---------- bmi_category ----------
def test_invalid_height_raises():
    with pytest.raises(ValueError, match="invalid height"):
        bmi_category(70, 0)


def test_underweight():
    assert bmi_category(50, 1.75) == "underweight"


def test_normal():
    assert bmi_category(70, 1.75) == "normal"


def test_overweight():
    assert bmi_category(85, 1.75) == "overweight"


def test_obese():
    assert bmi_category(100, 1.75) == "obese"
