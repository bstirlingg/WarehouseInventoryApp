import unittest
from InventoryManagement import InventoryManager

class TestWarehouseApp(unittest.TestCase):

    def setUp(self):
        self.inventory_manager = InventoryManager()

    # Test Add Section Feature
    def test_add_section(self):
        self.inventory_manager.add_section("Electronics")
        self.assertIn("Electronics", self.inventory_manager.sections)

    def test_add_empty_section(self):
        with self.assertRaises(ValueError):
            self.inventory_manager.add_section("")

    def test_add_duplicate_section(self):
        self.inventory_manager.add_section("Electronics")
        with self.assertRaises(ValueError):
            self.inventory_manager.add_section("Electronics")

    # Test Add Item Feature
    def test_add_item(self):
        self.inventory_manager.add_section("Fruits")
        self.inventory_manager.add_item("Fruits", "Apple", 10)
        section = self.inventory_manager.sections["Fruits"]
        self.assertIn("Apple", section.items)

    def test_add_item_to_non_existent_section(self):
        with self.assertRaises(ValueError):
            self.inventory_manager.add_item("NonExistentSection", "Apple", 5)

    def test_add_item_negative_quantity(self):
        self.inventory_manager.add_section("Fruits")
        with self.assertRaises(ValueError):
            self.inventory_manager.add_item("Fruits", "Apple", -5)

    # Test Add Stock Feature
    def test_add_stock(self):
        self.inventory_manager.add_section("Fruits")
        self.inventory_manager.add_item("Fruits", "Apple", 10)
        self.inventory_manager.add_item("Fruits", "Apple", 5)
        self.assertEqual(self.inventory_manager.sections["Fruits"].items["Apple"].quantity, 15)

    # Test Remove Stock Feature
    def test_remove_stock(self):
        self.inventory_manager.add_section("Fruits")
        self.inventory_manager.add_item("Fruits", "Apple", 10)
        self.inventory_manager.remove_item("Fruits", "Apple", 5)
        self.assertEqual(self.inventory_manager.sections["Fruits"].items["Apple"].quantity, 5)

    def test_remove_more_stock_than_available(self):
        self.inventory_manager.add_section("Fruits")
        self.inventory_manager.add_item("Fruits", "Apple", 3)
        with self.assertRaises(ValueError):
            self.inventory_manager.remove_item("Fruits", "Apple", 5)

    # Test Move Item Feature
    def test_move_item(self):
        self.inventory_manager.add_section("Fruits")
        self.inventory_manager.add_section("Vegetables")
        self.inventory_manager.add_item("Fruits", "Apple", 10)
        self.inventory_manager.move_item("Fruits", "Vegetables", "Apple", 5)
        self.assertEqual(self.inventory_manager.sections["Fruits"].items["Apple"].quantity, 5)
        self.assertEqual(self.inventory_manager.sections["Vegetables"].items["Apple"].quantity, 5)

    def test_move_item_non_existent_section(self):
        self.inventory_manager.add_section("Fruits")
        self.inventory_manager.add_item("Fruits", "Apple", 10)
        with self.assertRaises(ValueError):
            self.inventory_manager.move_item("Fruits", "NonExistentSection", "Apple", 5)

if __name__ == '__main__':
    unittest.main()
