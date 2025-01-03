import unittest
from InventoryManagement import InventoryManager

class TestInventoryManager(unittest.TestCase):

    def setUp(self):
        self.inventory_manager = InventoryManager()

    def test_add_section(self):
        self.inventory_manager.add_section("Electronics")
        self.assertIn("Electronics", self.inventory_manager.sections)

    def test_add_item(self):
        self.inventory_manager.add_section("Fruits")
        self.inventory_manager.add_item("Fruits", "Apple", 10)
        self.assertIn("Apple", self.inventory_manager.sections["Fruits"])
        self.assertEqual(
            self.inventory_manager.sections["Fruits"]["Apple"]["quantity"],
            10
        )

    def test_add_item_to_nonexistent_section(self):
        with self.assertRaises(ValueError):
            self.inventory_manager.add_item("NonExistent", "Apple", 5)

    def test_modify_item_quantity(self):
        self.inventory_manager.add_section("Fruits")
        self.inventory_manager.add_item("Fruits", "Apple", 10)
        self.inventory_manager.modify_item_quantity("Fruits", "Apple", 5)
        self.assertEqual(
            self.inventory_manager.sections["Fruits"]["Apple"]["quantity"],
            5
        )

    def test_modify_item_quantity_nonexistent_section(self):
        with self.assertRaises(ValueError):
            self.inventory_manager.modify_item_quantity("FakeSection", "Apple", 5)

    def test_modify_item_quantity_nonexistent_item(self):
        self.inventory_manager.add_section("Fruits")
        with self.assertRaises(ValueError):
            self.inventory_manager.modify_item_quantity("Fruits", "Banana", 5)

    def test_get_inventory_data(self):
        self.inventory_manager.add_section("Fruits")
        self.inventory_manager.add_item("Fruits", "Apple", 10, "2025-01-01")
        data = self.inventory_manager.get_inventory_data()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["Section Name"], "Fruits")
        self.assertEqual(data[0]["Item Name"], "Apple")
        self.assertEqual(data[0]["Quantity"], 10)
        self.assertEqual(data[0]["Expiry Date"], "2025-01-01")

if __name__ == "__main__":
    unittest.main()
