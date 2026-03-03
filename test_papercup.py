import unittest
import sys
import os

# make sure we can import from the parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import (
    Product, BasketItem,
    seed_inventory,
    money,
    list_products,
    add_to_basket,
    basket_total,
    remove_from_basket,
    adjust_basket_qty,
    apply_discount,
)


class TestMoneyFormatter(unittest.TestCase):

    def test_formats_to_two_decimal_places(self):
        self.assertEqual(money(3.6), "£3.60")

    def test_formats_whole_number(self):
        self.assertEqual(money(5.0), "£5.00")

    def test_formats_already_two_dp(self):
        self.assertEqual(money(12.99), "£12.99")


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.inventory = seed_inventory()

    def test_inventory_is_not_empty(self):
        self.assertGreater(len(self.inventory), 0)

    def test_contains_drinks(self):
        drinks = list_products(self.inventory, "drinks")
        self.assertGreater(len(drinks), 0)

    def test_contains_food(self):
        food = list_products(self.inventory, "food")
        self.assertGreater(len(food), 0)

    def test_contains_books(self):
        books = list_products(self.inventory, "books")
        self.assertGreater(len(books), 0)

    def test_books_are_delivery_eligible(self):
        books = list_products(self.inventory, "books")
        for book in books:
            self.assertTrue(book.delivery_eligible)

    def test_drinks_not_delivery_eligible(self):
        drinks = list_products(self.inventory, "drinks")
        for drink in drinks:
            self.assertFalse(drink.delivery_eligible)

    def test_all_products_have_positive_price(self):
        for product in self.inventory.values():
            self.assertGreater(product.price, 0)

    def test_all_products_have_positive_stock(self):
        for product in self.inventory.values():
            self.assertGreater(product.stock, 0)


class TestBasket(unittest.TestCase):

    def setUp(self):
        self.inventory = seed_inventory()
        self.basket = []

    def _get_product(self, pid):
        return self.inventory[pid]

    def test_add_new_item_to_basket(self):
        p = self._get_product("D1")
        add_to_basket(self.basket, p, 2)
        self.assertEqual(len(self.basket), 1)
        self.assertEqual(self.basket[0].qty, 2)

    def test_adding_same_item_increases_qty(self):
        p = self._get_product("D1")
        add_to_basket(self.basket, p, 1)
        add_to_basket(self.basket, p, 3)
        self.assertEqual(len(self.basket), 1)
        self.assertEqual(self.basket[0].qty, 4)

    def test_basket_total_is_correct(self):
        p1 = self._get_product("D1")  # £3.60
        p2 = self._get_product("F1")  # £2.90
        add_to_basket(self.basket, p1, 2)  # 7.20
        add_to_basket(self.basket, p2, 1)  # 2.90
        self.assertAlmostEqual(basket_total(self.basket), 10.10, places=2)

    def test_empty_basket_total_is_zero(self):
        self.assertEqual(basket_total(self.basket), 0.0)

    def test_remove_from_basket_restores_stock(self):
        p = self._get_product("D1")
        original_stock = p.stock
        add_to_basket(self.basket, p, 3)
        p.stock -= 3  # simulate stock deduction

        # manually remove (simulating user choosing line 1)
        removed = self.basket.pop(0)
        self.inventory[removed.product_id].stock += removed.qty

        self.assertEqual(p.stock, original_stock)
        self.assertEqual(len(self.basket), 0)

    def test_basket_stores_correct_unit_price(self):
        p = self._get_product("B1")  # Atomic Habits £12.99
        add_to_basket(self.basket, p, 1)
        self.assertAlmostEqual(self.basket[0].unit_price, 12.99, places=2)


class TestDiscount(unittest.TestCase):

    def test_10_percent_discount(self):
        new_total, disc = apply_discount(100.0)
        self.assertAlmostEqual(new_total, 90.0, places=2)
        self.assertAlmostEqual(disc, 10.0, places=2)

    def test_discount_on_small_amount(self):
        new_total, disc = apply_discount(3.60)
        self.assertAlmostEqual(new_total, 3.24, places=2)
        self.assertAlmostEqual(disc, 0.36, places=2)

    def test_discount_on_zero(self):
        new_total, disc = apply_discount(0.0)
        self.assertEqual(new_total, 0.0)
        self.assertEqual(disc, 0.0)


class TestListProducts(unittest.TestCase):

    def setUp(self):
        self.inventory = seed_inventory()

    def test_returns_only_drinks(self):
        result = list_products(self.inventory, "drinks")
        for p in result:
            self.assertEqual(p.category, "drinks")

    def test_returns_only_food(self):
        result = list_products(self.inventory, "food")
        for p in result:
            self.assertEqual(p.category, "food")

    def test_unknown_category_returns_empty(self):
        result = list_products(self.inventory, "nonexistent")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
