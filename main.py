import tkinter as tk
from InventoryManagement import InventoryManager

class WarehouseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Warehouse Management System")
        self.geometry("800x600")
        self.inventory_manager = InventoryManager()
        self.create_widgets()

    def create_widgets(self):
        # Add Section
        tk.Label(self, text="Add Section").grid(row=0, column=0, padx=5, pady=5)
        self.section_entry = tk.Entry(self)
        self.section_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text="Add Section", command=self.add_section).grid(row=0, column=2, padx=5, pady=5)

        # Add Item
        tk.Label(self, text="Item Name").grid(row=1, column=0, padx=5, pady=5)
        self.item_name_entry = tk.Entry(self)
        self.item_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Quantity").grid(row=2, column=0, padx=5, pady=5)
        self.item_quantity_entry = tk.Entry(self)
        self.item_quantity_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="Expiry Date (optional)").grid(row=3, column=0, padx=5, pady=5)
        self.item_expiry_entry = tk.Entry(self)
        self.item_expiry_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self, text="Add Item", command=self.add_item).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Manage Stock
        tk.Label(self, text="Manage Stock").grid(row=5, column=0, padx=5, pady=5)
        tk.Label(self, text="Item Name").grid(row=6, column=0, padx=5, pady=5)
        self.stock_item_name_entry = tk.Entry(self)
        self.stock_item_name_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self, text="Quantity").grid(row=7, column=0, padx=5, pady=5)
        self.stock_quantity_entry = tk.Entry(self)
        self.stock_quantity_entry.grid(row=7, column=1, padx=5, pady=5)

        tk.Button(self, text="Add Stock", command=self.add_stock).grid(row=8, column=0, padx=5, pady=5)
        tk.Button(self, text="Remove Stock", command=self.remove_stock).grid(row=8, column=1, padx=5, pady=5)

        # Move Item
        tk.Label(self, text="Move Item").grid(row=9, column=0, padx=5, pady=5)
        tk.Label(self, text="From Section").grid(row=10, column=0, padx=5, pady=5)
        self.from_section_entry = tk.Entry(self)
        self.from_section_entry.grid(row=10, column=1, padx=5, pady=5)

        tk.Label(self, text="To Section").grid(row=11, column=0, padx=5, pady=5)
        self.to_section_entry = tk.Entry(self)
        self.to_section_entry.grid(row=11, column=1, padx=5, pady=5)

        tk.Label(self, text="Item Name").grid(row=12, column=0, padx=5, pady=5)
        self.move_item_name_entry = tk.Entry(self)
        self.move_item_name_entry.grid(row=12, column=1, padx=5, pady=5)

        tk.Label(self, text="Quantity").grid(row=13, column=0, padx=5, pady=5)
        self.move_quantity_entry = tk.Entry(self)
        self.move_quantity_entry.grid(row=13, column=1, padx=5, pady=5)

        tk.Button(self, text="Move Item", command=self.move_item).grid(row=14, column=0, columnspan=2, padx=5, pady=5)

        # Inventory Overview
        self.inventory_text = tk.Text(self, height=15, width=70)
        self.inventory_text.grid(row=15, column=0, columnspan=3, padx=5, pady=5)

    # Add Section
    def add_section(self):
        section_name = self.section_entry.get()
        self.inventory_manager.add_section(section_name)
        self.update_inventory()

    # Add Item
    def add_item(self):
        section_name = self.section_entry.get()
        item_name = self.item_name_entry.get()
        quantity = int(self.item_quantity_entry.get())
        expiry_date = self.item_expiry_entry.get()

        try:
            self.inventory_manager.add_item(section_name, item_name, quantity, expiry_date if expiry_date else None)
            self.update_inventory()
        except ValueError as e:
            print(f"Error: {e}")

    # Manage Stock
    def add_stock(self):
        section_name = self.section_entry.get()
        item_name = self.stock_item_name_entry.get()
        quantity = int(self.stock_quantity_entry.get())

        try:
            self.inventory_manager.add_item(section_name, item_name, quantity)
            self.update_inventory()
        except ValueError as e:
            print(f"Error: {e}")

    def remove_stock(self):
        section_name = self.section_entry.get()
        item_name = self.stock_item_name_entry.get()
        quantity = int(self.stock_quantity_entry.get())

        try:
            self.inventory_manager.remove_item(section_name, item_name, quantity)
            self.update_inventory()
        except ValueError as e:
            print(f"Error: {e}")

    # Move Item
    def move_item(self):
        from_section = self.from_section_entry.get()
        to_section = self.to_section_entry.get()
        item_name = self.move_item_name_entry.get()
        quantity = int(self.move_quantity_entry.get())

        try:
            self.inventory_manager.move_item(from_section, to_section, item_name, quantity)
            self.update_inventory()
        except ValueError as e:
            print(f"Error: {e}")

    # Update Inventory Display
    def update_inventory(self):
        self.inventory_text.delete(1.0, tk.END)
        self.inventory_text.insert(tk.END, self.inventory_manager.get_inventory_overview())


if __name__ == "__main__":
    app = WarehouseApp()
    app.mainloop()
