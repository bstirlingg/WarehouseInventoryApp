import customtkinter as ctk
from InventoryManagement import InventoryManager


class WarehouseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Warehouse Management System")
        self.geometry("900x700")
        self.inventory_manager = InventoryManager()

        # Configure grid layout for the main window
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_widgets()

    def create_widgets(self):
        """Create and organize UI components."""
        # Add Section Frame
        section_frame = self.create_frame("Add Section", 0, 0)
        self.section_entry = self.create_entry(section_frame, "Enter section name", 1, 0)
        self.create_button(section_frame, "Add Section", self.add_section, 1, 1)

        # Add Item Frame
        item_frame = self.create_frame("Add Item", 1, 0)
        self.item_name_entry = self.create_entry(item_frame, "Item Name", 1, 0)
        self.item_quantity_entry = self.create_entry(item_frame, "Quantity", 2, 0)
        self.item_expiry_entry = self.create_entry(item_frame, "Expiry Date (optional)", 3, 0)
        self.create_button(item_frame, "Add Item", self.add_item, 4, 0, columnspan=2)

        # Manage Stock Frame
        stock_frame = self.create_frame("Manage Stock", 0, 1)
        self.stock_item_name_entry = self.create_entry(stock_frame, "Item Name", 1, 0)
        self.stock_quantity_entry = self.create_entry(stock_frame, "Quantity", 2, 0)
        self.create_button(stock_frame, "Add Stock", self.add_stock, 3, 0)
        self.create_button(stock_frame, "Remove Stock", self.remove_stock, 3, 1)

        # Move Item Frame
        move_frame = self.create_frame("Move Item", 1, 1)
        self.from_section_entry = self.create_entry(move_frame, "From Section", 1, 0)
        self.to_section_entry = self.create_entry(move_frame, "To Section", 2, 0)
        self.move_item_name_entry = self.create_entry(move_frame, "Item Name", 3, 0)
        self.move_quantity_entry = self.create_entry(move_frame, "Quantity", 4, 0)
        self.create_button(move_frame, "Move Item", self.move_item, 5, 0, columnspan=2)

        # Inventory Overview Frame
        inventory_frame = ctk.CTkFrame(self, corner_radius=10)
        inventory_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(inventory_frame, text="Inventory Overview", font=("Arial", 18)).grid(row=0, column=0, pady=5)
        self.inventory_text = ctk.CTkTextbox(inventory_frame, width=850, height=200)
        self.inventory_text.grid(row=1, column=0, padx=10, pady=5)

    def create_frame(self, title, row, column):
        """Create a titled frame."""
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(frame, text=title, font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=5)
        return frame

    def create_entry(self, frame, placeholder, row, column):
        """Create an entry widget."""
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder, width=200)
        entry.grid(row=row, column=column, padx=10, pady=5)
        return entry

    def create_button(self, frame, text, command, row, column, columnspan=1):
        """Create a button widget."""
        button = ctk.CTkButton(frame, text=text, command=command)
        button.grid(row=row, column=column, columnspan=columnspan, padx=10, pady=5)

    # Add Section Functionality
    def add_section(self):
        section_name = self.section_entry.get()
        if section_name:
            self.inventory_manager.add_section(section_name)
            self.update_inventory()

    # Add Item Functionality
    def add_item(self):
        section_name = self.section_entry.get()
        item_name = self.item_name_entry.get()
        quantity = self.item_quantity_entry.get()
        expiry_date = self.item_expiry_entry.get()

        if section_name and item_name and quantity.isdigit():
            self.inventory_manager.add_item(section_name, item_name, int(quantity), expiry_date or None)
            self.update_inventory()

    # Add Stock Functionality
    def add_stock(self):
        section_name = self.section_entry.get()
        item_name = self.stock_item_name_entry.get()
        quantity = self.stock_quantity_entry.get()

        if section_name and item_name and quantity.isdigit():
            self.inventory_manager.add_item(section_name, item_name, int(quantity))
            self.update_inventory()

    # Remove Stock Functionality
    def remove_stock(self):
        section_name = self.section_entry.get()
        item_name = self.stock_item_name_entry.get()
        quantity = self.stock_quantity_entry.get()

        if section_name and item_name and quantity.isdigit():
            self.inventory_manager.remove_item(section_name, item_name, int(quantity))
            self.update_inventory()

    # Move Item Functionality
    def move_item(self):
        from_section = self.from_section_entry.get()
        to_section = self.to_section_entry.get()
        item_name = self.move_item_name_entry.get()
        quantity = self.move_quantity_entry.get()

        if from_section and to_section and item_name and quantity.isdigit():
            self.inventory_manager.move_item(from_section, to_section, item_name, int(quantity))
            self.update_inventory()

    # Update Inventory Display
    def update_inventory(self):
        self.inventory_text.delete("1.0", "end")
        self.inventory_text.insert("end", self.inventory_manager.get_inventory_overview())


if __name__ == "__main__":
    app = WarehouseApp()
    app.mainloop()
