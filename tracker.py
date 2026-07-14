"""
tracker.py
----------
Core business logic for Smart Expense Tracker Pro.

The ExpenseTracker class is responsible for:
    - Loading and saving data to a JSON file
    - Managing the user's profile (name, monthly budget)
    - Adding, viewing, searching, editing, and deleting expenses
    - Computing statistics
    - Sorting expenses

This module intentionally contains NO print()-heavy UI code beyond
light interactive prompts for gathering input - actual formatted
display is delegated to ui.py to keep concerns separated.
"""

import json
import os

import ui
import utils


class ExpenseTracker:
    """Manages all expense data and operations for a single user session."""

    def __init__(self, data_file: str):
        self.data_file = data_file
        self.user_name = ""
        self.monthly_budget = 0.0
        self.expenses = []  # list of dicts: id, name, category, amount, date

    # ----------------------------------------------------------------
    # Persistence
    # ----------------------------------------------------------------

    def load_data(self) -> bool:
        """
        Load previously saved data from the JSON file, if it exists.
        Returns True if existing data was successfully loaded.
        """
        if not os.path.exists(self.data_file):
            return False

        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.user_name = data.get("user_name", "")
                self.monthly_budget = data.get("monthly_budget", 0.0)
                self.expenses = data.get("expenses", [])
                return True
        except (json.JSONDecodeError, OSError) as error:
            ui.print_error(f"Could not read existing data file ({error}). Starting fresh.")
            return False
        except Exception as error:
            ui.print_error(f"Unexpected error while loading data: {error}")
            return False

    def save_data(self) -> None:
        """Persist the current state (profile + expenses) to the JSON file."""
        try:
            # Ensure the target directory exists before writing.
            directory = os.path.dirname(self.data_file)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            data = {
                "user_name": self.user_name,
                "monthly_budget": self.monthly_budget,
                "expenses": self.expenses,
            }
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except OSError as error:
            ui.print_error(f"Failed to save data to disk: {error}")
        except Exception as error:
            ui.print_error(f"Unexpected error while saving data: {error}")

    # ----------------------------------------------------------------
    # Profile setup
    # ----------------------------------------------------------------

    def setup_profile(self) -> None:
        """
        Ask the user for their name and monthly budget if not already
        loaded from a previous session (or let them start a fresh one).
        """
        if self.user_name and self.monthly_budget:
            ui.print_info(f"Welcome back, {self.user_name}!")
            if utils.get_yes_no("Would you like to start a NEW session (reset name/budget)? (y/n): "):
                self._ask_profile_details()
        else:
            self._ask_profile_details()

    def _ask_profile_details(self) -> None:
        self.user_name = utils.get_valid_string("Enter your name: ")
        self.monthly_budget = utils.get_valid_float(
            "Enter your monthly budget (Rs.): ", allow_zero=True
        )
        ui.print_success(f"Profile set up for {self.user_name} with a budget of Rs.{self.monthly_budget:.2f}")

    # ----------------------------------------------------------------
    # CRUD operations
    # ----------------------------------------------------------------

    def add_expense(self) -> None:
        ui.print_header("➕  ADD NEW EXPENSE")
        try:
            name = utils.get_valid_string("Enter expense name: ")
            category = utils.choose_category()
            amount = utils.get_valid_float("Enter amount (Rs.): ")

            expense = {
                "id": utils.generate_expense_id(self.expenses),
                "name": name,
                "category": category,
                "amount": amount,
                "date": utils.get_current_datetime(),
            }
            self.expenses.append(expense)
            self.save_data()
            ui.print_success(f"Expense '{name}' added successfully with ID {expense['id']}!")

            # Warn immediately if this expense pushes the user over budget.
            total = self.get_total_amount()
            if total > self.monthly_budget:
                ui.print_warning(
                    f"You have now exceeded your monthly budget by Rs.{total - self.monthly_budget:.2f}!"
                )
        except (KeyboardInterrupt, EOFError):
            raise
        except Exception as error:
            ui.print_error(f"Could not add expense: {error}")

    def view_expenses(self) -> None:
        ui.print_header("📄  ALL EXPENSES")
        ui.print_expense_table(self.expenses)

    def find_expense_by_id(self, expense_id: str):
        """Return the expense dict matching the given ID, or None."""
        for expense in self.expenses:
            if expense["id"].lower() == expense_id.lower():
                return expense
        return None

    def search_expense(self) -> None:
        ui.print_header("🔍  SEARCH EXPENSE")
        try:
            print("Search by:")
            print("   1. Expense ID")
            print("   2. Expense Name")
            choice = utils.get_valid_int_choice("Enter choice: ", range(1, 3))

            if choice == 1:
                expense_id = utils.get_valid_string("Enter Expense ID: ")
                result = self.find_expense_by_id(expense_id)
                results = [result] if result else []
            else:
                keyword = utils.get_valid_string("Enter name (or part of it): ").lower()
                results = [e for e in self.expenses if keyword in e["name"].lower()]

            if results:
                ui.print_success(f"Found {len(results)} matching expense(s):")
                ui.print_expense_table(results)
            else:
                ui.print_warning("No matching expenses found.")
        except (KeyboardInterrupt, EOFError):
            raise
        except Exception as error:
            ui.print_error(f"Search failed: {error}")

    def edit_expense(self) -> None:
        ui.print_header("✏️  EDIT EXPENSE")
        try:
            if not self.expenses:
                ui.print_warning("There are no expenses to edit.")
                return

            expense_id = utils.get_valid_string("Enter the Expense ID to edit: ")
            expense = self.find_expense_by_id(expense_id)

            if not expense:
                ui.print_error(f"No expense found with ID '{expense_id}'.")
                return

            ui.print_info("Current details:")
            ui.print_expense_table([expense])

            print("\nLeave a field blank to keep it unchanged.")

            new_name = input(f"New name [{expense['name']}]: ").strip()
            if new_name:
                expense["name"] = new_name

            if utils.get_yes_no("Change category? (y/n): "):
                expense["category"] = utils.choose_category()

            new_amount_raw = input(f"New amount [{expense['amount']:.2f}] (blank to keep): ").strip()
            if new_amount_raw:
                try:
                    new_amount = float(new_amount_raw)
                    if new_amount < 0:
                        ui.print_warning("Negative amount not allowed. Amount unchanged.")
                    else:
                        expense["amount"] = round(new_amount, 2)
                except ValueError:
                    ui.print_warning("Invalid number entered. Amount unchanged.")

            self.save_data()
            ui.print_success(f"Expense {expense_id} updated successfully!")
        except (KeyboardInterrupt, EOFError):
            raise
        except Exception as error:
            ui.print_error(f"Could not edit expense: {error}")

    def delete_expense(self) -> None:
        ui.print_header("🗑️  DELETE EXPENSE")
        try:
            if not self.expenses:
                ui.print_warning("There are no expenses to delete.")
                return

            expense_id = utils.get_valid_string("Enter the Expense ID to delete: ")
            expense = self.find_expense_by_id(expense_id)

            if not expense:
                ui.print_error(f"No expense found with ID '{expense_id}'.")
                return

            ui.print_expense_table([expense])
            confirm = utils.get_yes_no(f"Are you sure you want to delete '{expense['name']}'? (y/n): ")

            if confirm:
                self.expenses = [e for e in self.expenses if e["id"] != expense["id"]]
                self.save_data()
                ui.print_success(f"Expense {expense_id} deleted successfully!")
            else:
                ui.print_info("Deletion cancelled.")
        except (KeyboardInterrupt, EOFError):
            raise
        except Exception as error:
            ui.print_error(f"Could not delete expense: {error}")

    # ----------------------------------------------------------------
    # Sorting
    # ----------------------------------------------------------------

    def sort_expenses(self) -> None:
        ui.print_header("↕️  SORT EXPENSES")
        try:
            if not self.expenses:
                ui.print_warning("There are no expenses to sort.")
                return

            print("Sort by:")
            print("   1. Amount (High to Low)")
            print("   2. Amount (Low to High)")
            print("   3. Date (Newest First)")
            print("   4. Date (Oldest First)")
            choice = utils.get_valid_int_choice("Enter choice: ", range(1, 5))

            if choice == 1:
                self.expenses.sort(key=lambda e: e["amount"], reverse=True)
            elif choice == 2:
                self.expenses.sort(key=lambda e: e["amount"], reverse=False)
            elif choice == 3:
                self.expenses.sort(key=lambda e: e["date"], reverse=True)
            elif choice == 4:
                self.expenses.sort(key=lambda e: e["date"], reverse=False)

            self.save_data()
            ui.print_success("Expenses sorted successfully!")
            ui.print_expense_table(self.expenses)
        except (KeyboardInterrupt, EOFError):
            raise
        except Exception as error:
            ui.print_error(f"Could not sort expenses: {error}")

    # ----------------------------------------------------------------
    # Statistics
    # ----------------------------------------------------------------

    def get_total_amount(self) -> float:
        return round(sum(e["amount"] for e in self.expenses), 2)

    def compute_statistics(self) -> dict:
        """Compute and return a dictionary of overall statistics."""
        count = len(self.expenses)
        total = self.get_total_amount()
        average = round(total / count, 2) if count > 0 else 0.0

        highest = max(self.expenses, key=lambda e: e["amount"]) if self.expenses else None
        lowest = min(self.expenses, key=lambda e: e["amount"]) if self.expenses else None

        # Category-wise totals
        category_totals = {}
        for expense in self.expenses:
            category = expense["category"]
            category_totals[category] = round(
                category_totals.get(category, 0.0) + expense["amount"], 2
            )

        return {
            "count": count,
            "total": total,
            "average": average,
            "highest": highest,
            "lowest": lowest,
            "category_totals": category_totals,
        }

    def view_statistics(self) -> None:
        try:
            stats = self.compute_statistics()
            ui.print_statistics(stats, self.monthly_budget)
        except Exception as error:
            ui.print_error(f"Could not compute statistics: {error}")