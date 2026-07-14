"""
main.py
-------
Entry point for Smart Expense Tracker Pro.

Run this file to start the application:
    python main.py

This module wires together ui.py (presentation), utils.py (validation
helpers) and tracker.py (business logic / data) into a menu-driven
console application.
"""

import os
import sys

import ui
import utils
from tracker import ExpenseTracker

# Data is stored relative to this script so it works regardless of the
# current working directory the user launches it from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "expenses.json")


def handle_menu_choice(choice: int, tracker: ExpenseTracker) -> bool:
    """
    Execute the action corresponding to the user's menu choice.
    Returns False if the program should exit, True otherwise.
    """
    if choice == 1:
        tracker.add_expense()
    elif choice == 2:
        tracker.view_expenses()
    elif choice == 3:
        tracker.search_expense()
    elif choice == 4:
        tracker.edit_expense()
    elif choice == 5:
        tracker.delete_expense()
    elif choice == 6:
        tracker.view_statistics()
    elif choice == 7:
        tracker.sort_expenses()
    elif choice == 8:
        tracker.save_data()
        ui.print_success("Data saved successfully!")
    elif choice == 9:
        return False

    return True


def main() -> None:
    ui.print_welcome_banner()

    tracker = ExpenseTracker(DATA_FILE)

    try:
        found_previous_data = tracker.load_data()
        if found_previous_data:
            ui.print_info("Previous session data loaded successfully.")
        tracker.setup_profile()

        # Main application loop.
        running = True
        while running:
            try:
                ui.print_main_menu()
                choice = utils.get_valid_int_choice("Enter your choice (1-9): ", range(1, 10))
                running = handle_menu_choice(choice, tracker)
            except (KeyboardInterrupt, EOFError):
                # Allow Ctrl+C / Ctrl+D to trigger a graceful exit too.
                print()
                ui.print_warning("Interrupted by user. Exiting gracefully...")
                running = False
            except Exception as error:
                # Catch-all so a single unexpected error never crashes the app.
                ui.print_error(f"An unexpected error occurred: {error}")

        # Final save + receipt before closing.
        tracker.save_data()
        stats = tracker.compute_statistics()
        ui.print_receipt(
            user_name=tracker.user_name or "Guest",
            timestamp=utils.get_current_datetime(),
            expense_count=stats["count"],
            total_amount=stats["total"],
            budget=tracker.monthly_budget,
        )

    except (KeyboardInterrupt, EOFError):
        print()
        ui.print_warning("Program interrupted before setup completed. Goodbye!")
        sys.exit(0)
    except Exception as error:
        ui.print_error(f"A fatal error occurred: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()