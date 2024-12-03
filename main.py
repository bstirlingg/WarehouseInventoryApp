import tkinter as tk
from InventoryManagement import InventoryManager

class WarehouseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Warehouse Management System")
        self.geometry("600x400")
        self.inventory_manager = InventoryManager()
        self.create_widgets()

    def create_widgets(self):
        # Example: Add section
        tk.Label(self, text="Add Section").pack()
        self.section_entry = tk.Entry(self)
        self.section_entry.pack()
        tk.Button(self, text="Add Section", command=self.add_section).pack()

        # Inventory overview
        self.inventory_text = tk.Text(self, height=10, width=50)
        self.inventory_text.pack()

    def add_section(self):
        section_name = self.section_entry.get()
        self.inventory_manager.add_section(section_name)
        self.update_inventory()

    def update_inventory(self):
        self.inventory_text.delete(1.0, tk.END)
        self.inventory_text.insert(tk.END, self.inventory_manager.get_inventory_overview())

if __name__ == "__main__":
    app = WarehouseApp()
    app.mainloop()
