"""Branch coverage tests for gym_membership.py.

Goal: every if / elif / else decision goes both the True and the False way,
plus the boundary values where each decision flips.
Run:  coverage run --branch -m pytest BranchCoverageTest_PES1UG24CS326_gym_membership.py
      coverage report -m
"""
import pytest
from gym_membership import membership_cost, can_enter, bmi_category


# ---------- membership_cost ----------
@pytest.mark.parametrize("plan", ["daily", "", "Monthly"])
def test_unknown_plan_raises(plan):
    # plan not in PLAN_PRICE -> True branch
    with pytest.raises(ValueError, match="unknown plan"):
        membership_cost(plan, 30, False, False)


def test_age_13_too_young():
    # age < 14 -> True branch (just below boundary)
    with pytest.raises(ValueError, match="too young"):
        membership_cost("monthly", 13, False, False)


def test_age_14_allowed():
    # age < 14 -> False branch (exact boundary)
    assert membership_cost("monthly", 14, False, False) == 1500


def test_age_59_no_senior_discount():
    # age >= 60 False, is_student False -> no discount
    assert membership_cost("monthly", 59, False, False) == 1500


def test_age_60_senior_discount():
    # age >= 60 True (exact boundary): 1500 - 375
    assert membership_cost("monthly", 60, False, False) == 1125


def test_senior_student_gets_only_senior_discount():
    # age >= 60 True, so the elif is_student branch is skipped
    assert membership_cost("monthly", 70, True, False) == 1125


def test_student_discount():
    # age >= 60 False, is_student True: 4000 - 400
    assert membership_cost("quarterly", 20, True, False) == 3600


def test_no_trainer():
    # with_trainer False branch
    assert membership_cost("quarterly", 30, False, False) == 4000


def test_trainer_non_yearly():
    # with_trainer True, plan == "yearly" False: 1500 + 2000
    assert membership_cost("monthly", 30, False, True) == 3500


def test_trainer_yearly():
    # with_trainer True, plan == "yearly" True: 12000 + 2000 - 500
    assert membership_cost("yearly", 30, False, True) == 13500


def test_all_discounts_combined():
    # senior yearly with trainer: 12000 - 3000 + 2000 - 500
    assert membership_cost("yearly", 65, False, True) == 10500


# ---------- can_enter ----------
def test_inactive_plan():
    # not plan_active -> True branch
    assert can_enter(10, False, False, "M") is False


@pytest.mark.parametrize("hour", [4, 23])
def test_outside_hours(hour):
    # hour < 5 True (4) and hour > 22 True (23)
    assert can_enter(hour, True, False, "M") is False


@pytest.mark.parametrize("hour", [5, 22])
def test_boundary_hours_allowed(hour):
    # both hour conditions False at the exact boundaries
    assert can_enter(hour, True, False, "M") is True


def test_women_only_slot_female():
    # is_women_only_slot True, gender == "F" True
    assert can_enter(10, True, True, "F") is True


def test_women_only_slot_male():
    # is_women_only_slot True, gender == "F" False
    assert can_enter(10, True, True, "M") is False


def test_regular_slot_any_gender():
    # is_women_only_slot False
    assert can_enter(10, True, False, "F") is True


# ---------- bmi_category ----------
@pytest.mark.parametrize("height", [0, -1.7])
def test_invalid_height(height):
    # height_m <= 0 True (zero and negative)
    with pytest.raises(ValueError, match="invalid height"):
        bmi_category(70, height)


@pytest.mark.parametrize("weight, expected", [
    (18.4, "underweight"),   # bmi < 18.5 True
    (18.5, "normal"),        # boundary: bmi < 18.5 False, < 25 True
    (24.9, "normal"),
    (25, "overweight"),      # boundary: bmi < 25 False, < 30 True
    (29.9, "overweight"),
    (30, "obese"),           # boundary: bmi < 30 False
    (45, "obese"),
])
def test_bmi_categories_and_boundaries(weight, expected):
    # height 1 m makes bmi == weight, so boundaries are exact
    assert bmi_category(weight, 1) == expected
