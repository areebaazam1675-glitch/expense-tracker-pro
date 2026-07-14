"""
utils.py
--------
Utility/helper functions for Smart Expense Tracker Pro.

This module contains:
    - Input validation helpers (strings, floats, choices, yes/no)
    - Category definitions
    - Expense ID generation
    - Date/time helpers

Keeping these in a separate module keeps the rest of the codebase
clean and avoids duplicating validation logic everywhere.
"""

from datetime import datetime

# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------

# Fixed list of allowed expense categories.
CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Education",
    "Health",
    "Entertainment",
    "Other",
]


# ----------------------------------------------------------------------
# Input validation helpers
# ----------------------------------------------------------------------

def get_valid_string(prompt: str, allow_empty: bool = False) -> str:
    """
    Ask the user for a string and keep asking until a valid
    (non-empty, unless allowed) string is provided.
    """
    while True:
        try:
            value = input(prompt).strip()
            if not value and not allow_empty:
                print("⚠️  This field cannot be empty. Please try again.")
                continue
            return value
        except (KeyboardInterrupt, EOFError):
            # Re-raise so the main loop can handle a graceful exit.
            raise
        except Exception as error:
            print(f"⚠️  Unexpected input error: {error}. Please try again.")


def get_valid_float(prompt: str, allow_zero: bool = False) -> float:
    """
    Ask the user for a positive float (e.g. an amount / budget).
    Rejects negative numbers, non-numeric input, and (optionally) zero.
    """
    while True:
        try:
            raw_value = input(prompt).strip()
            value = float(raw_value)

            if value < 0:
                print("⚠️  Negative amounts are not allowed. Please enter a positive number.")
                continue
            if value == 0 and not allow_zero:
                print("⚠️  Amount must be greater than zero.")
                continue

            return round(value, 2)
        except ValueError:
            print("⚠️  Invalid number. Please enter a numeric value (e.g. 250.50).")
        except (KeyboardInterrupt, EOFError):
            raise
        except Exception as error:
            print(f"⚠️  Unexpected input error: {error}. Please try again.")


def get_valid_int_choice(prompt: str, valid_range: range) -> int:
    """
    Ask the user to pick a menu option and validate it falls
    within the allowed range of integers.
    """
    while True:
        try:
            raw_value = input(prompt).strip()
            value = int(raw_value)
            if value not in valid_range:
                print(f"⚠️  Please enter a number between {valid_range.start} and {valid_range.stop - 1}.")
                continue
            return value
        except ValueError:
            print("⚠️  Invalid input. Please enter a whole number.")
        except (KeyboardInterrupt, EOFError):
            raise
        except Exception as error:
            print(f"⚠️  Unexpected input error: {error}. Please try again.")


def get_yes_no(prompt: str) -> bool:
    """
    Ask a yes/no question and return True for yes, False for no.
    Accepts y/n/yes/no (case-insensitive).
    """
    while True:
        try:
            answer = input(prompt).strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            print("⚠️  Please answer with 'y' or 'n'.")
        except (KeyboardInterrupt, EOFError):
            raise
        except Exception as error:
            print(f"⚠️  Unexpected input error: {error}. Please try again.")


def choose_category() -> str:
    """
    Display the fixed list of categories and let the user pick one
    by number. Returns the chosen category name.
    """
    print("\nSelect a category:")
    for index, category in enumerate(CATEGORIES, start=1):
        print(f"   {index}. {category}")

    choice = get_valid_int_choice(
        "Enter category number: ", range(1, len(CATEGORIES) + 1)
    )
    return CATEGORIES[choice - 1]


# ----------------------------------------------------------------------
# ID / Date helpers
# ----------------------------------------------------------------------

def generate_expense_id(expenses: list) -> str:
    """
    Generate a new unique Expense ID in the form EXP001, EXP002, ...
    based on the highest existing numeric suffix currently in use.
    """
    max_number = 0
    for expense in expenses:
        expense_id = expense.get("id", "")
        # Expected format: EXP<digits>. Safely parse the numeric part.
        if expense_id.startswith("EXP"):
            number_part = expense_id[3:]
            if number_part.isdigit():
                max_number = max(max_number, int(number_part))

    new_number = max_number + 1
    return f"EXP{new_number:03d}"


def get_current_datetime() -> str:
    """Return the current date & time as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")