# ☕📚 PaperCup

A command-line ordering system for a bookshop and cafe. Built in Python as part of a team learning project.

---

## What it does

PaperCup lets customers browse and order drinks, food, and books from a terminal interface. It also includes a basic employee portal for managing stock and adding new items.

**Customer features:**
- Browse drinks, food, and books by category
- View product details before ordering
- Add items to a basket, adjust quantities, or remove items
- Book delivery option at checkout (for eligible titles)
- Clean receipt-style order summary

**Employee features:**
- Password-protected portal
- Add new products to the menu/inventory
- Update stock levels
- View full inventory list
- Apply a 10% promotional discount at checkout

---

## Project structure

```
papercup/
├── main.py          # All app logic lives here
├── README.md        # This file
├── .gitignore       # Files to exclude from git
└── tests/
    └── test_papercup.py   # Unit tests
```

---

## Getting started

**Requirements:** Python 3.7 or higher (uses dataclasses and type hints).

No external libraries needed — this runs on the Python standard library only.

**Clone and run:**

```bash
git clone https://github.com/lizturay/papercup.git
cd papercup
python main.py
```

**Run the tests:**

```bash
python -m pytest tests/
```

Or without pytest:

```bash
python -m unittest tests/test_papercup.py
```

---

## How to use it

When you run `main.py`, you'll see a home menu:

```
============================================================
PaperCup — HOME
============================================================
1. Customer ordering
2. Employee admin
0. Exit
```

Select `1` to start a customer order, or `2` to access the employee portal.

**Employee password:** `password`  
(This is intentionally simple for a learning project. In a real app, you would never hardcode a password.)

---

## Key design decisions

- **Dataclasses** are used for `Product` and `BasketItem` so Python auto-generates `__init__` without boilerplate.
- **Stock is reserved at add-to-basket time**, not at checkout. Removing items from the basket returns stock correctly.
- **Quantity adjustment** uses a delta approach: it calculates the difference between old and new quantities and adjusts stock accordingly, which avoids double-counting.
- **No external dependencies** keeps the app simple and portable.

---

## Known limitations / future improvements

- Passwords are hardcoded (not secure for real use)
- No data persistence: inventory resets every time the app restarts
- `float()` and `int()` input in employee add-item can crash on bad input
- No receipt/order history
- Tests only cover core logic functions, not the full interactive flow

---

## Team

Built by the Generations 'PaperCup' team as a Python learning project.
