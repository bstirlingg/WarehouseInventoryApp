import customtkinter as ctk
from InventoryManagement import InventoryManager

class WarehouseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Warehouse Management System")
        self.geometry("900x700")
        self.inventory_manager = InventoryManager()
        self.create_widgets()

    def create_widgets(self):
        # Configure grid layout
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(15, weight=1)

        # Add Section
        section_label = ctk.CTkLabel(self, text="Add Section", font=("Helvetica", 16))
        section_label.grid(row=0, column=0, padx=10, pady=10)

        self.section_entry = ctk.CTkEntry(self, placeholder_text="Enter section name")
        self.section_entry.grid(row=0, column=1, padx=10, pady=10)

        add_section_button = ctk.CTkButton(self, text="Add Section", command=self.add_section)
        add_section_button.grid(row=0, column=2, padx=10, pady=10)

        # Add Item
        item_label = ctk.CTkLabel(self, text="Add Item", font=("Helvetica", 16))
        item_label.grid(row=1, column=0, padx=10, pady=10)

        self.item_name_entry = ctk.CTkEntry(self, placeholder_text="Item Name")
        self.item_name_entry.grid(row=2, column=0, padx=10, pady=10)

        self.item_quantity_entry = ctk.CTkEntry(self, placeholder_text="Quantity")
        self.item_quantity_entry.grid(row=2, column=1, padx=10, pady=10)

        self.item_expiry_entry = ctk.CTkEntry(self, placeholder_text="Expiry Date (optional)")
        self.item_expiry_entry.grid(row=2, column=2, padx=10, pady=10)

        add_item_button = ctk.CTkButton(self, text="Add Item", command=self.add_item)
        add_item_button.grid(row=3, column=0, columnspan=3, pady=10)

        # Manage Stock
        stock_label = ctk.CTkLabel(self, text="Manage Stock", font=("Helvetica", 16))
        stock_label.grid(row=4, column=0, padx=10, pady=10)

        self.stock_item_name_entry = ctk.CTkEntry(self, placeholder_text="Item Name")
        self.stock_item_name_entry.grid(row=5, column=0, padx=10, pady=10)

        self.stock_quantity_entry = ctk.CTkEntry(self, placeholder_text="Quantity")
        self.stock_quantity_entry.grid(row=5, column=1, padx=10, pady=10)

        add_stock_button = ctk.CTkButton(self, text="Add Stock", command=self.add_stock)
        add_stock_button.grid(row=6, column=0, padx=10, pady=10)

        remove_stock_button = ctk.CTkButton(self, text="Remove Stock", command=self.remove_stock)
        remove_stock_button.grid(row=6, column=1, padx=10, pady=10)

        # Move Item
        move_label = ctk.CTkLabel(self, text="Move Item", font=("Helvetica", 16))
        move_label.grid(row=7, column=0, padx=10, pady=10)

        self.from_section_entry = ctk.CTkEntry(self, placeholder_text="From Section")
        self.from_section_entry.grid(row=8, column=0, padx=10, pady=10)

        self.to_section_entry = ctk.CTkEntry(self, placeholder_text="To Section")
        self.to_section_entry.grid(row=8, column=1, padx=10, pady=10)

        self.move_item_name_entry = ctk.CTkEntry(self, placeholder_text="Item Name")
        self.move_item_name_entry.grid(row=8, column=2, padx=10, pady=10)

        self.move_quantity_entry = ctk.CTkEntry(self, placeholder_text="Quantity")
        self.move_quantity_entry.grid(row=9, column=0, padx=10, pady=10)

        move_item_button = ctk.CTkButton(self, text="Move Item", command=self.move_item)
        move_item_button.grid(row=9, column=1, columnspan=2, pady=10)

        # Inventory Overview
        self.inventory_text = ctk.CTkTextbox(self, width=600, height=300)
        self.inventory_text.grid(row=10, column=0, columnspan=3, padx=10, pady=10)

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
        self.inventory_text.delete("0.0", "end")
        self.inventory_text.insert("0.0", self.inventory_manager.get_inventory_overview())


if __name__ == "__main__":
    app = WarehouseApp()
    app.mainloop()
