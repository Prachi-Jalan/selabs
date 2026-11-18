"""Gym membership input parsers, hardened after fuzz testing.

Each function returns None for any input it cannot handle, instead of
crashing. Bugs found by Hypothesis are noted next to each fix.
"""
import math


def parse_plan(code):
    """'GOLD-12' -> ('GOLD', 12). Returns None for invalid input."""
    if not isinstance(code, str):           # None / non-string -> AttributeError
        return None
    parts = code.strip().split('-')
    if len(parts) != 2:                     # '' or 'GOLD' or 'A-B-C' -> unpack ValueError
        return None
    plan, months = parts[0].strip(), parts[1].strip()
    if not plan:                            # '-12' -> empty plan name
        return None
    try:
        months = int(months)                # 'GOLD-x' -> ValueError
    except ValueError:
        return None
    if months <= 0:                         # 'GOLD-0', 'GOLD--5'
        return None
    return plan.upper(), months


def calculate_bmi(data):
    """'70,1.75' -> 22.9. Returns None for invalid input."""
    if not isinstance(data, str):           # None -> AttributeError
        return None
    parts = data.split(',')
    if len(parts) != 2:                     # '' or '70' or '1,2,3' -> unpack ValueError
        return None
    try:
        weight, height = float(parts[0]), float(parts[1])   # 'a,b' -> ValueError
    except ValueError:
        return None
    if not (math.isfinite(weight) and math.isfinite(height)):  # 'nan', 'inf'
        return None
    if weight <= 0 or height <= 0:          # '70,0' -> ZeroDivisionError
        return None
    try:
        bmi = weight / (height ** 2)        # '1,1e200' -> OverflowError
    except (OverflowError, ZeroDivisionError):  # '1,1e-200' -> height**2 == 0.0
        return None
    if not math.isfinite(bmi):              # '1e308,1e-10' -> inf
        return None
    return round(bmi, 1)


def average_workout(minutes):
    """'45 60 30' -> 45. Returns None for invalid input."""
    if not isinstance(minutes, str):        # None -> AttributeError
        return None
    try:
        values = [int(m) for m in minutes.split()]   # 'abc' -> ValueError
    except ValueError:
        return None
    if not values:                          # '' or '   ' -> ZeroDivisionError
        return None
    if any(v < 0 for v in values):          # negative workout minutes
        return None
    return sum(values) // len(values)


def main():
    """Ask for each input and print the result, or an error message."""
    print("==== Running parse_plan ====")
    user_input = input("Enter a plan code (e.g. GOLD-12): ")
    result = parse_plan(user_input)
    print("Plan and Months:", result if result else "Invalid plan code")

    print("\n==== Running calculate_bmi ====")
    user_input = input("Enter weight and height (e.g. 70,1.75): ")
    result = calculate_bmi(user_input)
    print("BMI:", result if result is not None else "Invalid weight/height")

    print("\n==== Running average_workout ====")
    user_input = input("Enter workout minutes separated by spaces (e.g. 45 60 30): ")
    result = average_workout(user_input)
    print("Average Minutes:", result if result is not None else "Invalid minutes")


if __name__ == "__main__":
    main()
