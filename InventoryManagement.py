class InventoryManager:
    def __init__(self):
        self.sections = {}

    def add_section(self, name):
        if name not in self.sections:
            self.sections[name] = {}

    def add_item(self, section_name, item_name, quantity, expiry_date=None):
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
        if section_name not in self.sections:
            raise ValueError(f"Section '{section_name}' not found.")
        if item_name not in self.sections[section_name]:
            raise ValueError(f"Item '{item_name}' not found in section '{section_name}'.")
        self.sections[section_name][item_name]["quantity"] = new_quantity

    def get_inventory_data(self):
        data = []
        for section, items in self.sections.items():
            for item, details in items.items():
                data.append({
                    "Section Name": section,
                    "Item Name": item,
                    "Quantity": details["quantity"],
                    "Expiry Date": details["expiry_date"] or "N/A",
                })
        return data

    # ---- NEW METHODS FOR DROPDOWNS ----
    def get_section_names(self):
        """Return a list of all existing section names."""
        return list(self.sections.keys())

    def get_item_names_in_section(self, section_name):
        """Return a list of item names for the given section."""
        if section_name in self.sections:
            return list(self.sections[section_name].keys())
        return []
