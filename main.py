import customtkinter as ctk
from PIL import Image  # for loading the logo image

# ---------------------------
# INVENTORY MANAGER LOGIC
# ---------------------------
class InventoryManager:
    def __init__(self):
        self.sections = {}

    def add_section(self, name):
        """Add a new section if it doesn't already exist."""
        if name not in self.sections:
            self.sections[name] = {}

    def add_item(self, section_name, item_name, quantity, expiry_date=None):
        """Add or increase quantity of an item in the given section."""
        if section_name not in self.sections:
            raise ValueError(f"Section '{section_name}' not found.")
        if item_name in self.sections[section_name]:
            self.sections[section_name][item_name]["quantity"] += quantity
        else:
            self.sections[section_name][item_name] = {
                "quantity": quantity,
                "expiry_date": expiry_date,
            }

    def modify_item_quantity(self, section_name, item_name, new_quantity):
        """Set an item's quantity in a section to a new value."""
        if section_name not in self.sections:
            raise ValueError(f"Section '{section_name}' not found.")
        if item_name not in self.sections[section_name]:
            raise ValueError(f"Item '{item_name}' not found in section '{section_name}'.")
        self.sections[section_name][item_name]["quantity"] = new_quantity

    def get_inventory_data(self):
        """Return a list of dictionaries for displaying in the UI."""
        data = []
        for section, items in self.sections.items():
            for item_name, details in items.items():
                data.append({
                    "Section Name": section,
                    "Item Name": item_name,
                    "Quantity": details["quantity"],
                    "Expiry Date": details["expiry_date"] or "N/A",
                })
        return data

    def get_section_names(self):
        """For dropdowns: return all section names."""
        return list(self.sections.keys())

    def get_item_names_in_section(self, section_name):
        """For dropdowns: return all item names in the given section."""
        if section_name in self.sections:
            return list(self.sections[section_name].keys())
        return []


# ---------------------------
# WELCOME SCREEN
# ---------------------------
class WelcomeScreen(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("600x400")
        self.title("Welcome")

        self.grab_set()
        self.lift(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        welcome_frame = ctk.CTkFrame(self)
        welcome_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        img = Image.open("Assets/light_logo.png")
        self.logo_image = ctk.CTkImage(light_image=img, size=(500, 200))  # Example: setting size to 200x200

        # Label for the logo
        logo_label = ctk.CTkLabel(welcome_frame, text="", image=self.logo_image)
        logo_label.pack(pady=10)

        # Welcome Text
        ctk.CTkLabel(
            welcome_frame,
            text="Welcome to Light Logistics Inventory Management System",
            font=("Arial", 16, "bold"),
            wraplength=400,
            justify="center"
        ).pack(pady=20)

        # Enter Button
        ctk.CTkButton(
            welcome_frame,
            text="Enter",
            command=self.close_screen,
            width=150
        ).pack(pady=20)

    def close_screen(self):
        self.destroy()


# ---------------------------
# MAIN APP WINDOW
# ---------------------------
class WarehouseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Light Logistics Inventory Management")
        self.geometry("1000x700")

        self.inventory_manager = InventoryManager()

        # Main layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Overview Frame
        self.inventory_overview_frame = InventoryOverviewFrame(self, self.inventory_manager)
        self.inventory_overview_frame.grid(row=0, column=0, sticky="nsew")

        # Buttons at the bottom
        button_frame = ctk.CTkFrame(self.inventory_overview_frame)
        button_frame.grid(row=2, column=0, pady=(10, 20), sticky="s")

        ctk.CTkButton(
            button_frame,
            text="Manage Inventory",
            command=self.open_manage_inventory_modal,
            width=150
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            button_frame,
            text="Move Inventory",
            command=self.open_move_inventory_modal,
            width=150
        ).grid(row=0, column=1, padx=10)

    def open_manage_inventory_modal(self):
        ManageInventoryModal(self, self.inventory_manager, self.inventory_overview_frame).grab_set()

    def open_move_inventory_modal(self):
        MoveInventoryModal(self, self.inventory_manager, self.inventory_overview_frame).grab_set()


# ---------------------------
# INVENTORY OVERVIEW FRAME
# ---------------------------
class InventoryOverviewFrame(ctk.CTkFrame):
    def __init__(self, parent, inventory_manager):
        super().__init__(parent)
        self.inventory_manager = inventory_manager

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Title
        ctk.CTkLabel(
            self,
            text="Inventory Overview",
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0, pady=10)

        # Table Frame (dark background for contrast)
        self.table_frame = ctk.CTkFrame(
            self,
            corner_radius=8,
            fg_color="#333333",
            border_width=2,
            border_color="gray"
        )
        self.table_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.table_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Table Headers
        headers = ["Section Name", "Item Name", "Quantity", "Expiry Date"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                self.table_frame,
                text=header,
                font=("Arial", 14, "bold"),
                text_color="white"
            ).grid(row=0, column=col, padx=10, pady=5, sticky="ew")

        # Header divider
        ctk.CTkFrame(self.table_frame, fg_color="gray", height=2).grid(
            row=1, column=0, columnspan=4, sticky="ew", padx=5, pady=(0, 5)
        )

        # Data rows
        self.rows = []
        self.update_inventory()

    def update_inventory(self):
        # Clear old row widgets
        for row in self.rows:
            for widget in row:
                widget.destroy()
        self.rows.clear()

        # Load current data
        inventory_data = self.inventory_manager.get_inventory_data()
        for row_idx, item in enumerate(inventory_data, start=1):
            row_widgets = []
            values = [
                item["Section Name"],
                item["Item Name"],
                item["Quantity"],
                item["Expiry Date"] or "N/A",
            ]
            for col_idx, val in enumerate(values):
                label = ctk.CTkLabel(
                    self.table_frame,
                    text=val,
                    font=("Arial", 12),
                    text_color="white",
                    anchor="center",
                )
                label.grid(row=row_idx * 2, column=col_idx, padx=10, pady=5, sticky="ew")
                row_widgets.append(label)

            # Divider
            divider = ctk.CTkFrame(self.table_frame, fg_color="gray", height=2)
            divider.grid(row=row_idx * 2 + 1, column=0, columnspan=4, sticky="ew", padx=0, pady=(0, 0))

            self.rows.append(row_widgets)


# ---------------------------
# MANAGE INVENTORY MODAL
# ---------------------------
class ManageInventoryModal(ctk.CTkToplevel):
    """
    A single modal to add or update inventory.
    """
    def __init__(self, parent, inventory_manager, overview_frame):
        super().__init__(parent)
        self.title("Manage Inventory")
        self.geometry("450x450")

        self.inventory_manager = inventory_manager
        self.overview_frame = overview_frame

        self.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(self, text="Manage Inventory", font=("Arial", 18, "bold")).grid(
            row=0, column=0, pady=(20, 10)
        )

        # Error feedback
        self.feedback_label = ctk.CTkLabel(self, text="", text_color="red")
        self.feedback_label.grid(row=1, column=0, pady=5)

        # Section
        ctk.CTkLabel(self, text="Select or Enter Section:", font=("Arial", 12)).grid(
            row=2, column=0, padx=20, pady=(10, 0), sticky="w"
        )
        self.section_var = ctk.StringVar()
        sections = self.inventory_manager.get_section_names()
        if sections:
            self.section_var.set(sections[0])

        self.section_optionmenu = ctk.CTkOptionMenu(
            self, variable=self.section_var, values=sections, command=self.on_section_changed
        )
        self.section_optionmenu.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        self.new_section_entry = ctk.CTkEntry(self, placeholder_text="Or type new section name", width=300)
        self.new_section_entry.grid(row=4, column=0, padx=20, pady=5)

        # Item
        ctk.CTkLabel(self, text="Select or Enter Item:", font=("Arial", 12)).grid(
            row=5, column=0, padx=20, pady=(10, 0), sticky="w"
        )
        self.item_var = ctk.StringVar()
        self.item_optionmenu = ctk.CTkOptionMenu(self, variable=self.item_var, values=[])
        self.item_optionmenu.grid(row=6, column=0, padx=20, pady=5, sticky="ew")

        self.new_item_entry = ctk.CTkEntry(self, placeholder_text="Or type new item name", width=300)
        self.new_item_entry.grid(row=7, column=0, padx=20, pady=5)

        # Quantity
        self.quantity_entry = ctk.CTkEntry(self, placeholder_text="Quantity to add or set", width=300)
        self.quantity_entry.grid(row=8, column=0, padx=20, pady=10)

        # Expiry (optional)
        self.expiry_entry = ctk.CTkEntry(self, placeholder_text="Expiry Date (optional)", width=300)
        self.expiry_entry.grid(row=9, column=0, padx=20, pady=10)

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=10, column=0, pady=(20, 10))
        ctk.CTkButton(button_frame, text="Submit", command=self.submit_action, width=100).grid(row=0, column=0, padx=10)
        ctk.CTkButton(button_frame, text="Cancel", command=self.destroy, width=100).grid(row=0, column=1, padx=10)

        # Initialize item dropdown for the first section
        self.on_section_changed(self.section_var.get() if sections else "")

    def on_section_changed(self, selected_section):
        """Update item dropdown whenever user picks a different existing section."""
        if not selected_section:
            self.item_optionmenu.configure(values=[])
            self.item_var.set("")
            return
        items = self.inventory_manager.get_item_names_in_section(selected_section)
        self.item_optionmenu.configure(values=items)
        if items:
            self.item_var.set(items[0])
        else:
            self.item_var.set("")

    def submit_action(self):
        """Validate user input and apply changes."""
        self.feedback_label.configure(text="")

        # Final section name
        section_name = self.new_section_entry.get().strip() or self.section_var.get().strip()
        if not section_name:
            self.feedback_label.configure(text="Error: Section name is required.")
            return

        # Final item name
        item_name = self.new_item_entry.get().strip() or self.item_var.get().strip()
        if not item_name:
            self.feedback_label.configure(text="Error: Item name is required.")
            return

        # Quantity
        quantity_str = self.quantity_entry.get().strip()
        if not quantity_str.isdigit():
            self.feedback_label.configure(text="Error: Quantity must be a positive integer.")
            return
        quantity = int(quantity_str)
        if quantity <= 0:
            self.feedback_label.configure(text="Error: Quantity must be greater than zero.")
            return

        expiry = self.expiry_entry.get().strip() or None

        try:
            self.inventory_manager.add_section(section_name)
            existing_items = self.inventory_manager.get_item_names_in_section(section_name)
            if item_name in existing_items:
                # Add to existing quantity
                curr_qty = self.inventory_manager.sections[section_name][item_name]["quantity"]
                new_total = curr_qty + quantity
                self.inventory_manager.modify_item_quantity(section_name, item_name, new_total)
            else:
                # Create new item
                self.inventory_manager.add_item(section_name, item_name, quantity, expiry)

            self.overview_frame.update_inventory()
            self.destroy()

        except ValueError as e:
            self.feedback_label.configure(text=f"Error: {e}")


# ---------------------------
# MOVE INVENTORY MODAL
# ---------------------------
class MoveInventoryModal(ctk.CTkToplevel):
    def __init__(self, parent, inventory_manager, overview_frame):
        super().__init__(parent)
        self.title("Move Inventory")
        self.geometry("400x400")

        self.inventory_manager = inventory_manager
        self.overview_frame = overview_frame

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="Move Inventory", font=("Arial", 18, "bold")).grid(
            row=0, column=0, pady=(20, 10)
        )
        self.feedback_label = ctk.CTkLabel(self, text="", text_color="red")
        self.feedback_label.grid(row=1, column=0, pady=5)

        # Source Section
        ctk.CTkLabel(self, text="Source Section:", font=("Arial", 12)).grid(
            row=2, column=0, padx=20, pady=(10, 0), sticky="w"
        )
        self.source_section_var = ctk.StringVar()
        section_list = self.inventory_manager.get_section_names()
        if section_list:
            self.source_section_var.set(section_list[0])
        self.source_section_menu = ctk.CTkOptionMenu(
            self,
            variable=self.source_section_var,
            values=section_list,
            command=self.on_source_section_changed
        )
        self.source_section_menu.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        # Source Item
        ctk.CTkLabel(self, text="Item to Move:", font=("Arial", 12)).grid(
            row=4, column=0, padx=20, pady=(10, 0), sticky="w"
        )
        self.source_item_var = ctk.StringVar()
        self.source_item_menu = ctk.CTkOptionMenu(self, variable=self.source_item_var, values=[])
        self.source_item_menu.grid(row=5, column=0, padx=20, pady=5, sticky="ew")

        # Target Section
        ctk.CTkLabel(self, text="Target Section:", font=("Arial", 12)).grid(
            row=6, column=0, padx=20, pady=(10, 0), sticky="w"
        )
        self.target_section_var = ctk.StringVar()
        self.target_section_menu = ctk.CTkOptionMenu(self, variable=self.target_section_var, values=section_list)
        if section_list:
            self.target_section_var.set(section_list[0])
        self.target_section_menu.grid(row=7, column=0, padx=20, pady=5, sticky="ew")

        # Quantity
        self.quantity_entry = ctk.CTkEntry(self, placeholder_text="Quantity to Move", width=300)
        self.quantity_entry.grid(row=8, column=0, padx=20, pady=10)

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=9, column=0, pady=(20, 10))

        ctk.CTkButton(button_frame, text="Move", command=self.move_inventory, width=100).grid(row=0, column=0, padx=10)
        ctk.CTkButton(button_frame, text="Cancel", command=self.destroy, width=100).grid(row=0, column=1, padx=10)

        self.on_source_section_changed(self.source_section_var.get() if section_list else "")

    def on_source_section_changed(self, selected_section):
        if not selected_section:
            self.source_item_menu.configure(values=[])
            self.source_item_var.set("")
            return
        items = self.inventory_manager.get_item_names_in_section(selected_section)
        self.source_item_menu.configure(values=items)
        if items:
            self.source_item_var.set(items[0])
        else:
            self.source_item_var.set("")

    def move_inventory(self):
        self.feedback_label.configure(text="")

        source_section = self.source_section_var.get().strip()
        target_section = self.target_section_var.get().strip()
        item_name = self.source_item_var.get().strip()
        qty_str = self.quantity_entry.get().strip()

        if not source_section or not target_section:
            self.feedback_label.configure(text="Error: Both source and target sections are required.")
            return
        if not item_name:
            self.feedback_label.configure(text="Error: Please select an item to move.")
            return
        if not qty_str.isdigit():
            self.feedback_label.configure(text="Error: Quantity must be a positive integer.")
            return

        quantity = int(qty_str)
        if quantity <= 0:
            self.feedback_label.configure(text="Error: Quantity must be greater than zero.")
            return

        try:
            self.inventory_manager.add_section(target_section)

            current_qty = self.inventory_manager.sections[source_section][item_name]["quantity"]
            new_source_qty = current_qty - quantity
            if new_source_qty < 0:
                raise ValueError("Not enough stock to move.")
            self.inventory_manager.modify_item_quantity(source_section, item_name, new_source_qty)

            if item_name in self.inventory_manager.sections[target_section]:
                target_qty = self.inventory_manager.sections[target_section][item_name]["quantity"]
                new_target_qty = target_qty + quantity
                self.inventory_manager.modify_item_quantity(target_section, item_name, new_target_qty)
            else:
                expiry = self.inventory_manager.sections[source_section][item_name]["expiry_date"]
                self.inventory_manager.add_item(target_section, item_name, quantity, expiry)

            self.overview_frame.update_inventory()
            self.destroy()

        except ValueError as e:
            self.feedback_label.configure(text=f"Error: {e}")


# ---------------------------
# APP ENTRY POINT
# ---------------------------
if __name__ == "__main__":
    # Optional: set a dark theme
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    app = WarehouseApp()
    app.withdraw()

    # Show the welcome screen as a Toplevel
    welcome_screen = WelcomeScreen(app)
    welcome_screen.wait_window()  # Wait until closed

    # Reveal the main app
    app.deiconify()
    app.mainloop()
