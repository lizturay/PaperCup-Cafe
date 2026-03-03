# importing stuff we need from python
# dataclass = easy way to make "data objects" without writing loads of code
from dataclasses import dataclass

# typing = not required, but helps me remember what type things are (list, dict etc)
from typing import Dict, List, Optional, Tuple


# these are like settings / constants for the app
TEAM_NAME = "PaperCup"           # name that shows in the header
EMPLOYEE_PASSWORD = "password"   # simple password for employee stuff


# =========================
# DATA MODELS (the "shapes" of our data)
# =========================

# dataclass makes python auto-create __init__ for us (so we can do Product(...))
@dataclass
class Product:
    # this stores ONE product (like a menu item or a book)
    id: str                # like "D1" or "F2"
    category: str          # "drinks" or "food" or "books"
    name: str              # product name
    price: float           # how much it costs
    stock: int             # how many left in stock
    details: str           # extra info (ingredients / author / etc)
    delivery_eligible: bool = False  # only really used for books


@dataclass
class BasketItem:
    # this stores ONE line in the basket/order
    product_id: str        # links back to a Product id
    name: str              # name (we store it so we can print it easily)
    unit_price: float      # price per 1 item
    qty: int               # how many the customer wants


# =========================
# INVENTORY (all products)
# =========================

def seed_inventory() -> Dict[str, Product]:
    # this function makes our starting inventory
    # we return a dictionary where:
    # key = product id (like "D1")
    # value = Product object
    return {
        # DRINKS
        "D1": Product("D1", "drinks", "Flat White", 3.60, 30, "Espresso + steamed milk"),
        "D2": Product("D2", "drinks", "Matcha Latte", 4.10, 20, "Matcha + milk"),
        "D3": Product("D3", "drinks", "Iced Americano", 3.20, 25, "Espresso + water + ice"),
        "D4": Product("D4", "drinks", "Tea", 2.00, 10, "Tea + hot water"),
        "D5": Product("D5", "drinks", "Herbal Tea", 3.00, 15, "Tea + herbs + hot water"),

        # FOOD
        "F1": Product("F1", "food", "Chocolate Brownie", 2.90, 15, "Cocoa, butter, eggs, sugar, flour"),
        "F2": Product("F2", "food", "Carrot Cake Slice", 3.40, 10, "Carrot, cinnamon, cream cheese frosting"),
        "F3": Product("F3", "food", "Cheese Cake", 4.00, 10, "Cream cheese, digestive, vanilla"),
        "F4": Product("F4", "food", "Croissant", 3.00, 15, "Bread"),
        "F5": Product("F5", "food", "Cheese Bagel", 4.00, 7, "Cheese, Bread"),

        # BOOKS
        "B1": Product("B1", "books", "Atomic Habits", 12.99, 8,
                      "James Clear - Habit building", delivery_eligible=True),
        "B2": Product("B2", "books", "The Midnight Library", 9.99, 6,
                      "Matt Haig - Fiction", delivery_eligible=True),
        "B3": Product("B3", "books", "Deep Work", 11.50, 5,
                      "Cal Newport - Focus & productivity", delivery_eligible=True),
        "B4": Product("B4", "books", "Seven Habits of Highly Effective People", 14.99, 7,
                      "Steven Cohen - Habit building", delivery_eligible=True),
        "B5": Product("B5", "books", "Harry Potter", 14.99, 7,
                      "J K Rowling - Fiction", delivery_eligible=True),
    }


# =========================
# SMALL HELPER FUNCTIONS
# =========================

def money(x: float) -> str:
    # this just formats money nicely
    # example: 3.6 -> "£3.60"
    return f"£{x:.2f}"


def pause():
    # this pauses the program so the user has time to read the screen
    input("\nPress Enter to continue...")


def ask_int(prompt: str, min_v: int, max_v: int) -> int:
    # keeps asking until the user types a valid number
    while True:
        raw = input(prompt).strip()

        # .isdigit() checks if it is only numbers (no letters)
        if raw.isdigit():
            val = int(raw)

            # check the number is in the allowed range
            if min_v <= val <= max_v:
                return val

        print(f"Please enter a number between {min_v} and {max_v}.")


def ask_yes_no(prompt: str) -> bool:
    # keeps asking until the user types Y or N
    while True:
        raw = input(prompt + " (Y/N): ").strip().lower()

        # if user says yes
        if raw in ("y", "yes"):
            return True

        # if user says no
        if raw in ("n", "no"):
            return False

        print("Please type Y or N.")


# =========================
# SCREEN / UI FUNCTIONS (printing menus etc)
# =========================

def print_header(title: str):
    # makes a nice header so the app looks neat
    print("\n" + "=" * 60)
    print(f"{TEAM_NAME} — {title}")
    print("=" * 60)


def list_products(inventory: Dict[str, Product], category: str) -> List[Product]:
    # get all products in ONE category (drinks/food/books)
    # inventory.values() gives all Product objects
    return [p for p in inventory.values() if p.category == category]


def show_category(inventory: Dict[str, Product], category: str):
    # prints a category list like:
    # 1. Flat White — £3.60 (stock: 30)
    print_header(category.upper())

    products = list_products(inventory, category)

    # if there are none, show message and return (stop this function)
    if not products:
        print("No items found.")
        return

    # enumerate gives us numbers starting at 1
    for idx, p in enumerate(products, start=1):
        stock_note = f"(stock: {p.stock})"
        print(f"{idx}. {p.name} — {money(p.price)} {stock_note}")


def choose_product(inventory: Dict[str, Product], category: str) -> Optional[Product]:
    # lets the user choose ONE product from a category
    # returns a Product or returns None if they go back

    products = list_products(inventory, category)

    if not products:
        return None

    show_category(inventory, category)
    print("\n0. Back")

    # user chooses a number from the list
    choice = ask_int("Select an item number: ", 0, len(products))

    # 0 means they want to go back
    if choice == 0:
        return None

    # choice-1 because python lists start at 0
    return products[choice - 1]


# =========================
# BASKET / ORDER FUNCTIONS
# =========================

def show_product_details(product: Product):
    # prints extra details about the product
    print_header("DETAILS")
    print(f"Item: {product.name}")
    print(f"Price: {money(product.price)}")
    print(f"Stock: {product.stock}")
    print(f"Details: {product.details}")

    # only books have delivery info
    if product.category == "books":
        print(f"Delivery eligible: {'Yes' if product.delivery_eligible else 'No'}")


def add_to_basket(basket: List[BasketItem], product: Product, qty: int):
    # adds items to basket
    # if already there, just increase quantity

    for item in basket:
        if item.product_id == product.id:
            item.qty += qty
            return

    # if not already in basket, add a new BasketItem line
    basket.append(BasketItem(product.id, product.name, product.price, qty))


def basket_total(basket: List[BasketItem]) -> float:
    # adds up total price of basket
    # sum(...) adds up all the values
    return sum(i.unit_price * i.qty for i in basket)


def print_basket(basket: List[BasketItem]):
    # shows the basket like a mini receipt
    print_header("YOUR ORDER")

    if not basket:
        print("Basket is empty.")
        return

    for idx, item in enumerate(basket, start=1):
        line_total = item.unit_price * item.qty
        print(f"{idx}. {item.name} x{item.qty} — {money(item.unit_price)} each = {money(line_total)}")

    print("-" * 60)
    print(f"Total: {money(basket_total(basket))}")


def remove_from_basket(basket: List[BasketItem], inventory: Dict[str, Product]):
    # removes a whole line from the basket
    # IMPORTANT: we must give stock back when removing

    if not basket:
        return

    print_basket(basket)
    choice = ask_int("Remove which line? (0 to cancel): ", 0, len(basket))

    if choice == 0:
        return

    # pop removes and returns the item at that index
    removed = basket.pop(choice - 1)

    # give stock back into inventory (so it's available again)
    if removed.product_id in inventory:
        inventory[removed.product_id].stock += removed.qty

    print(f"Removed: {removed.name}")


def adjust_basket_qty(basket: List[BasketItem], inventory: Dict[str, Product]):
    # changes how many of something is in the basket
    # IMPORTANT: we must not let qty go above stock

    if not basket:
        return

    print_basket(basket)
    choice = ask_int("Adjust which line? (0 to cancel): ", 0, len(basket))

    if choice == 0:
        return

    item = basket[choice - 1]

    # if product id is missing somehow, just stop
    if item.product_id not in inventory:
        print("Sorry, that product no longer exists in inventory.")
        return

    product = inventory[item.product_id]

    old_qty = item.qty

    # key idea:
    # we already took old_qty from stock when we added to basket
    # so max we can go to = old_qty + whatever is left in stock
    max_allowed = old_qty + product.stock

    new_qty = ask_int(
        f"New quantity for {item.name} (1-{max_allowed}): ",
        1,
        max_allowed
    )

    # delta tells us how much we changed by
    # example: old 3 -> new 5 => delta = +2 (we need 2 more stock)
    # example: old 5 -> new 2 => delta = -3 (we return 3 stock)
    delta = new_qty - old_qty

    # update stock:
    # if delta is positive, this subtracts more stock
    # if delta is negative, subtracting a negative adds stock back
    product.stock -= delta

    # update basket quantity
    item.qty = new_qty

    print("Updated.")


def apply_discount(total: float) -> Tuple[float, float]:
    # this applies 10% off
    # returns: (new_total, discount_amount)

    discount_rate = 0.10
    discount_amount = total * discount_rate
    new_total = total - discount_amount
    return new_total, discount_amount


# =========================
# EMPLOYEE FUNCTIONS
# =========================

def employee_login() -> bool:
    # simple login check
    print_header("EMPLOYEE LOGIN")
    pw = input("Enter employee password: ").strip()
    return pw == EMPLOYEE_PASSWORD


def employee_add_item(inventory: Dict[str, Product]):
    # lets employee add a new product to the inventory
    print_header("ADD NEW ITEM")

    new_id = input("New ID (e.g. D4 / F3 / B9): ").strip().upper()

    # don't allow duplicate ids
    if new_id in inventory:
        print("That ID already exists.")
        return

    category = input("Category (drinks/food/books): ").strip().lower()
    if category not in ("drinks", "food", "books"):
        print("Invalid category.")
        return

    name = input("Name: ").strip()

    # NOTE: float(...) and int(...) can crash if user types letters
    # (but it's ok for now, could improve later)
    price = float(input("Price (e.g. 3.50): ").strip())
    stock = int(input("Stock (e.g. 10): ").strip())

    details = input("Details (ingredients/author/etc): ").strip()

    delivery_eligible = False
    if category == "books":
        delivery_eligible = ask_yes_no("Delivery eligible?")

    # actually add to inventory dict
    inventory[new_id] = Product(
        id=new_id,
        category=category,
        name=name,
        price=price,
        stock=stock,
        details=details,
        delivery_eligible=delivery_eligible,
    )

    print("Item added!")


def employee_update_stock(inventory: Dict[str, Product]):
    # lets employee change stock for a product
    print_header("UPDATE STOCK")

    pid = input("Enter product ID: ").strip().upper()
    if pid not in inventory:
        print("Not found.")
        return

    p = inventory[pid]
    print(f"Current: {p.name} stock={p.stock}")

    new_stock = int(input("New stock value: ").strip())
    p.stock = new_stock

    print("Stock updated.")


# =========================
# CUSTOMER FLOW (main ordering journey)
# =========================

def customer_flow(inventory: Dict[str, Product]):
    # basket starts empty
    basket: List[BasketItem] = []

    # discount flags
    discounted = False
    discount_amount = 0.0

    # main loop so the app keeps running until user exits
    while True:
        print_header("WELCOME TO PAPERCUP")
        print("What would you like to order today?")
        print("1. Drinks")
        print("2. Food")
        print("3. Books")
        print("4. Review order")
        print("5. Checkout")
        print("0. Exit")

        choice = ask_int("Select an option: ", 0, 5)

        # exit the customer journey
        if choice == 0:
            print("Thank you for visiting, hope to see you soon!")
            return

        # choose from categories
        if choice in (1, 2, 3):
            # using a dictionary to map menu choice -> category string
            category = {1: "drinks", 2: "food", 3: "books"}[choice]

            product = choose_product(inventory, category)
            if not product:
                continue  # goes back to the main menu

            # optional details screen
            if ask_yes_no("View additional details?"):
                show_product_details(product)
                pause()

            # don't allow ordering if stock is 0
            if product.stock <= 0:
                print("Sorry, out of stock.")
                pause()
                continue

            # only allow qty up to current stock
            qty = ask_int(f"How many '{product.name}'? ", 1, min(99, product.stock))

            # add to basket and reduce stock (so we "reserve" it)
            add_to_basket(basket, product, qty)
            product.stock -= qty

            print("Added to basket!")
            pause()
            continue

        # REVIEW ORDER
        if choice == 4:
            while True:
                print_basket(basket)
                print("\n1. Remove an item")
                print("2. Adjust quantity")
                print("0. Back")

                sub = ask_int("Select: ", 0, 2)

                if sub == 0:
                    break

                if sub == 1:
                    remove_from_basket(basket, inventory)
                    pause()

                elif sub == 2:
                    adjust_basket_qty(basket, inventory)
                    pause()

            continue

        # CHECKOUT
        if choice == 5:
            # can't checkout if basket empty
            if not basket:
                print("Basket is empty.")
                pause()
                continue

            print_basket(basket)
            total = basket_total(basket)

            # employee discount option
            if ask_yes_no("Are you an employee?"):
                if employee_login():
                    if not discounted and ask_yes_no("Apply 10% promotional discount?"):
                        new_total, disc = apply_discount(total)
                        discounted = True
                        discount_amount = disc
                        total = new_total
                        print(f"Discount applied: -{money(discount_amount)}")
                    else:
                        print("No discount applied.")
                else:
                    print("Incorrect password. Continuing as customer.")

            # delivery part (only if basket includes books)
            has_books = any(
                inventory.get(i.product_id, Product("", "", "", 0, 0, "")).category == "books"
                for i in basket
            )

            delivery = False
            if has_books:
                delivery = ask_yes_no("Do you want book delivery (where eligible)?")
                if delivery:
                    name = input("Delivery name: ").strip()
                    address = input("Delivery address: ").strip()
                    print(f"Delivery set for: {name}, {address}")

            print_header("CONFIRMATION")
            if discounted:
                print(f"Discount: -{money(discount_amount)}")
            print(f"Final total: {money(total)}")

            if ask_yes_no("Place order?"):
                print_header("STATUS")
                print("Preparing your order ☕📚")
                if delivery:
                    print("Your books will be delivered as requested.")
                print("Thank you!")
                pause()
                return
            else:
                print("Order not placed. Returning to menu.")
                pause()
                continue


# =========================
# EMPLOYEE PORTAL (admin menu)
# =========================

def employee_portal(inventory: Dict[str, Product]):
    # must login first
    if not employee_login():
        print("Access denied.")
        pause()
        return

    while True:
        print_header("EMPLOYEE PORTAL")
        print("1. Add new menu/book item")
        print("2. Update stock")
        print("3. View inventory")
        print("0. Back")

        choice = ask_int("Select: ", 0, 3)

        if choice == 0:
            return

        if choice == 1:
            employee_add_item(inventory)
            pause()

        elif choice == 2:
            employee_update_stock(inventory)
            pause()

        elif choice == 3:
            print_header("INVENTORY")
            for p in inventory.values():
                print(f"{p.id} | {p.category} | {p.name} | {money(p.price)} | stock={p.stock}")
            pause()


# =========================
# MAIN APP START
# =========================

def main():
    # get starting inventory
    inventory = seed_inventory()

    # home loop (choose customer or employee)
    while True:
        print_header("HOME")
        print("1. Customer ordering")
        print("2. Employee admin")
        print("0. Exit")

        choice = ask_int("Select: ", 0, 2)

        if choice == 0:
            print("Goodbye!")
            break

        elif choice == 1:
            customer_flow(inventory)

        elif choice == 2:
            employee_portal(inventory)


# this means: only run main() if we run this file directly
# if we imported this file somewhere else, it wouldn't auto run
if __name__ == "__main__":
    main()
