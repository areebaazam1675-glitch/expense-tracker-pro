"""
ui.py
-----
All console presentation logic lives here: colors, headers, menus,
tables, statistics display, and the final receipt.

Keeping display code separate from business logic (tracker.py) makes
the project easier to read, test, and extend (e.g. swapping this for
a GUI later would only require changing this file).
"""

# ------------------------------------------------------------------
# Optional color support (colorama). The program must work perfectly
# even if colorama is not installed, so we fail gracefully.
# ------------------------------------------------------------------
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLOR_ENABLED = True
except ImportError:
    COLOR_ENABLED = False

    # Dummy fallback objects so the rest of the code can reference
    # Fore.XXX / Style.XXX safely even without colorama installed.
    class _DummyColor:
        def __getattr__(self, name):
            return ""

    Fore = _DummyColor()
    Style = _DummyColor()


# Shorthand color aliases used throughout the UI.
TITLE = Fore.CYAN + Style.BRIGHT
SUCCESS = Fore.GREEN + Style.BRIGHT
ERROR = Fore.RED + Style.BRIGHT
WARNING = Fore.YELLOW + Style.BRIGHT
INFO = Fore.BLUE + Style.BRIGHT
RESET = Style.RESET_ALL
HEADER_BG = Fore.MAGENTA + Style.BRIGHT

WIDTH = 78  # standard console width used for borders


# ------------------------------------------------------------------
# Generic helpers
# ------------------------------------------------------------------

def print_header(title: str) -> None:
    """Print a decorative section header."""
    print("\n" + TITLE + "=" * WIDTH + RESET)
    print(TITLE + title.center(WIDTH) + RESET)
    print(TITLE + "=" * WIDTH + RESET)


def print_divider() -> None:
    print(Fore.WHITE + "-" * WIDTH + RESET)


def print_success(message: str) -> None:
    print(SUCCESS + f"✅ {message}" + RESET)


def print_error(message: str) -> None:
    print(ERROR + f"❌ {message}" + RESET)


def print_warning(message: str) -> None:
    print(WARNING + f"⚠️  {message}" + RESET)


def print_info(message: str) -> None:
    print(INFO + f"ℹ️  {message}" + RESET)


# ------------------------------------------------------------------
# Welcome / Menu
# ------------------------------------------------------------------

def print_welcome_banner() -> None:
    banner = r"""
   _____                       _     ______                                  ____
  / ____|                     | |   |  ____|                                |  _ \
 | (___  _ __ ___   __ _ _ __ | |_  | |__  __  ___ __   ___ _ __  ___  ___  | |_) | _ __ ___
  \___ \| '_ ` _ \ / _` | '__|| __| |  __| \ \/ / '_ \ / _ \ '_ \/ __|/ _ \ |  __/ | '__/ _ \
  ____) | | | | | | (_| | |   | |_  | |____ >  <| |_) |  __/ | | \__ \  __/ | |    | | | (_) |
 |_____/|_| |_| |_|\__,_|_|    \__| |______/_/\_\ .__/ \___|_| |_|___/\___| |_|    |_|  \___/
                                                 | |
                                                 |_|            T R A C K E R   P R O
"""
    print(TITLE + banner + RESET)
    print(TITLE + "Your Personal Finance Companion".center(WIDTH) + RESET)
    print_divider()


def print_main_menu() -> None:
    print_header("📋  MAIN MENU")
    menu_items = [
        "1. Add Expense",
        "2. View All Expenses",
        "3. Search Expense",
        "4. Edit Expense",
        "5. Delete Expense",
        "6. View Statistics",
        "7. Sort Expenses",
        "8. Save Data",
        "9. Exit",
    ]
    for item in menu_items:
        print(f"   {Fore.WHITE}{item}{RESET}")
    print_divider()


# ------------------------------------------------------------------
# Table display
# ------------------------------------------------------------------

def print_expense_table(expenses: list) -> None:
    """
    Print a neatly formatted, fixed-width table of expenses.
    Handles the empty-list case gracefully.
    """
    if not expenses:
        print_warning("No expenses to display.")
        return

    # Column widths
    col_id, col_name, col_cat, col_amt, col_date = 8, 20, 14, 12, 20

    header = (
        f"{'ID':<{col_id}}{'Name':<{col_name}}{'Category':<{col_cat}}"
        f"{'Amount':<{col_amt}}{'Date & Time':<{col_date}}"
    )
    print(HEADER_BG + header + RESET)
    print(Fore.WHITE + "-" * (col_id + col_name + col_cat + col_amt + col_date) + RESET)

    for expense in expenses:
        name = expense["name"] if len(expense["name"]) <= col_name - 2 else expense["name"][:col_name - 5] + "..."
        row = (
            f"{expense['id']:<{col_id}}"
            f"{name:<{col_name}}"
            f"{expense['category']:<{col_cat}}"
            f"Rs.{expense['amount']:<{col_amt - 3}.2f}"
            f"{expense['date']:<{col_date}}"
        )
        print(row)

    print(Fore.WHITE + "-" * (col_id + col_name + col_cat + col_amt + col_date) + RESET)
    print(f"Total records: {len(expenses)}")


# ------------------------------------------------------------------
# Statistics display
# ------------------------------------------------------------------

def print_statistics(stats: dict, budget: float) -> None:
    print_header("📊  EXPENSE STATISTICS")

    print(f"   Total Number of Expenses : {stats['count']}")
    print(f"   Total Amount Spent       : Rs.{stats['total']:.2f}")
    print(f"   Average Expense          : Rs.{stats['average']:.2f}")

    if stats["highest"] is not None:
        print(f"   Highest Expense          : Rs.{stats['highest']['amount']:.2f} "
              f"({stats['highest']['name']} - {stats['highest']['category']})")
        print(f"   Lowest Expense           : Rs.{stats['lowest']['amount']:.2f} "
              f"({stats['lowest']['name']} - {stats['lowest']['category']})")
    else:
        print("   Highest / Lowest Expense : N/A (no expenses yet)")

    print_divider()

    # Budget section
    remaining = budget - stats["total"]
    print(f"   Monthly Budget           : Rs.{budget:.2f}")
    if remaining >= 0:
        print(SUCCESS + f"   Remaining Budget         : Rs.{remaining:.2f}" + RESET)
    else:
        print(ERROR + f"   Budget Exceeded By       : Rs.{abs(remaining):.2f}" + RESET)
        print_warning("You have exceeded your monthly budget!")

    print_divider()

    # Category-wise breakdown
    if stats["category_totals"]:
        print(TITLE + "   Category-wise Breakdown" + RESET)
        for category, amount in stats["category_totals"].items():
            percentage = (amount / stats["total"] * 100) if stats["total"] > 0 else 0
            bar_length = int(percentage / 5)  # simple text progress bar (max 20 chars)
            bar = "█" * bar_length
            print(f"   {category:<15}Rs.{amount:>10.2f}   {percentage:>5.1f}%  {Fore.CYAN}{bar}{RESET}")
    else:
        print_warning("No category data available yet.")


# ------------------------------------------------------------------
# Receipt display (on exit)
# ------------------------------------------------------------------

def print_receipt(user_name: str, timestamp: str, expense_count: int,
                   total_amount: float, budget: float) -> None:
    remaining = budget - total_amount

    print("\n" + TITLE + "*" * WIDTH + RESET)
    print(TITLE + "SMART EXPENSE TRACKER PRO".center(WIDTH) + RESET)
    print(TITLE + "OFFICIAL SESSION RECEIPT".center(WIDTH) + RESET)
    print(TITLE + "*" * WIDTH + RESET)
    print(f"   Customer Name        : {user_name}")
    print(f"   Date & Time          : {timestamp}")
    print_divider()
    print(f"   Total Expenses Logged: {expense_count}")
    print(f"   Total Amount Spent   : Rs.{total_amount:.2f}")
    print(f"   Monthly Budget       : Rs.{budget:.2f}")
    if remaining >= 0:
        print(SUCCESS + f"   Remaining Budget     : Rs.{remaining:.2f}" + RESET)
    else:
        print(ERROR + f"   Over Budget By       : Rs.{abs(remaining):.2f}" + RESET)
    print_divider()
    print(TITLE + "Thank you for using Smart Expense Tracker Pro!".center(WIDTH) + RESET)
    print(TITLE + "Keep tracking, keep saving! 💰".center(WIDTH) + RESET)
    print(TITLE + "*" * WIDTH + RESET + "\n")