# 💰 Smart Expense Tracker Pro

A professional, console-based personal expense tracker built in clean,
modular Python. Built as a learning/portfolio project to demonstrate
solid Python fundamentals: functions, classes, file I/O, JSON
persistence, input validation, and error handling.

---

## ✨ Features

- 🧾 **Add, view, search, edit, and delete** expenses
- 🔑 **Automatic unique Expense IDs** (`EXP001`, `EXP002`, ...)
- 🕒 **Automatic timestamping** of every expense
- 📁 **Fixed categories**: Food, Transport, Shopping, Bills, Education,
  Health, Entertainment, Other
- 💾 **Persistent JSON storage** — your data is automatically loaded
  when the app starts and saved as you go
- 🔍 **Search** by Expense ID or Name (partial match)
- ↕️ **Sort** by Amount (High→Low / Low→High) or Date (Newest/Oldest)
- 📊 **Statistics dashboard**:
  - Total expenses & total amount spent
  - Average, highest, and lowest expense
  - Remaining budget & over-budget warnings
  - Category-wise totals and percentages with a visual bar
- 🧮 **Input validation** everywhere (no negative amounts, no blank
  names, no invalid menu choices)
- 🛡️ **Robust error handling** via try/except throughout
- 🧾 **Professional exit receipt** summarizing your session
- 🎨 Clean, bordered, color-enhanced console UI (gracefully degrades
  to plain text if `colorama` isn't installed)

---

## 📂 Project Structure

```
smart_expense_tracker_pro/
│
├── main.py              # Entry point — menu loop & app flow
├── tracker.py            # ExpenseTracker class — all business logic
├── ui.py                  # Console presentation: colors, tables, banners
├── utils.py                # Input validation & helper functions
├── requirements.txt         # Optional dependencies
├── README.md                 # This file
└── data/
    └── expenses.json          # Auto-created — stores your saved data
```

This separation keeps **data logic**, **presentation**, and **input
validation** decoupled — each file has a single, clear responsibility.

---

## 🚀 Getting Started

### 1. Requirements

- Python 3.7+
- (Optional) `colorama` for colored output

### 2. Installation

```bash
# Clone or download the project folder, then:
cd smart_expense_tracker_pro

# (Optional) install colorama for a nicer, colored UI
pip install -r requirements.txt
```

> The app works perfectly fine **without** installing anything —
> `colorama` is purely cosmetic and the app auto-detects if it's
> missing.

### 3. Run the app

```bash
python main.py
```

---

## 🕹️ Usage

On first run, you'll be asked for your **name** and **monthly
budget**. After that you'll see the main menu:

```
1. Add Expense
2. View All Expenses
3. Search Expense
4. Edit Expense
5. Delete Expense
6. View Statistics
7. Sort Expenses
8. Save Data
9. Exit
```

Simply type the number of the option you want and follow the prompts.
All data is saved automatically to `data/expenses.json` after every
change, and reloaded automatically the next time you launch the app.

When you choose **Exit**, you'll see a professional receipt
summarizing your session (total expenses, total amount, remaining
budget, and a thank-you message).

---

## 📸 Sample Output

```
==============================================================================
                                 📋  MAIN MENU
==============================================================================
   1. Add Expense
   2. View All Expenses
   3. Search Expense
   4. Edit Expense
   5. Delete Expense
   6. View Statistics
   7. Sort Expenses
   8. Save Data
   9. Exit
------------------------------------------------------------------------------
Enter your choice (1-9): 2

==============================================================================
                               📄  ALL EXPENSES
==============================================================================
ID      Name                Category      Amount      Date & Time
------------------------------------------------------------------------
EXP001  Groceries           Food          Rs.1500.00  2026-07-14 09:37:29
EXP002  Cab Ride            Transport     Rs.300.00   2026-07-14 09:37:29
EXP003  New Laptop          Shopping      Rs.45000.00 2026-07-14 09:37:29
------------------------------------------------------------------------
Total records: 3
```

```
==============================================================================
                            📊  EXPENSE STATISTICS
==============================================================================
   Total Number of Expenses : 3
   Total Amount Spent       : Rs.46800.00
   Average Expense          : Rs.15600.00
   Highest Expense          : Rs.45000.00 (New Laptop - Shopping)
   Lowest Expense           : Rs.300.00 (Cab Ride - Transport)
------------------------------------------------------------------------------
   Monthly Budget           : Rs.5000.00
   Budget Exceeded By       : Rs.41800.00
⚠️  You have exceeded your monthly budget!
------------------------------------------------------------------------------
   Category-wise Breakdown
   Food           Rs.   1500.00     3.2%
   Transport      Rs.    300.00     0.6%
   Shopping       Rs.  45000.00    96.2%  ███████████████████
```

```
******************************************************************************
                          SMART EXPENSE TRACKER PRO
                           OFFICIAL SESSION RECEIPT
******************************************************************************
   Customer Name        : Areeba
   Date & Time          : 2026-07-14 09:40:12
------------------------------------------------------------------------------
   Total Expenses Logged: 3
   Total Amount Spent   : Rs.46800.00
   Monthly Budget       : Rs.5000.00
   Over Budget By       : Rs.41800.00
------------------------------------------------------------------------------
                Thank you for using Smart Expense Tracker Pro!
                        Keep tracking, keep saving! 💰
******************************************************************************
```

---

## 🧠 Design Notes / What This Project Demonstrates

- **Modular architecture** — logic split across `main.py`, `tracker.py`,
  `ui.py`, and `utils.py` instead of one giant script.
- **Object-oriented design** — `ExpenseTracker` class encapsulates all
  state and behavior for expenses.
- **JSON persistence** — human-readable storage using Python's built-in
  `json` module; no database required.
- **Defensive programming** — every user-input point and every file
  operation is wrapped in `try/except` blocks so the app never crashes
  unexpectedly.
- **Reusable validation helpers** (`get_valid_float`, `get_valid_int_choice`,
  etc.) to avoid duplicated validation logic.
- **Graceful degradation** — the app works with or without the optional
  `colorama` dependency installed.

---

## 📄 License

This project was built for personal learning and portfolio purposes.
Feel free to use, modify, and extend it.
