from Sections import InventorySection

class InventoryManager:
    def __init__(self):
        self.sections = {}

    def add_section(self, name):
        """Add a new section to the inventory if it doesn't already exist."""
        # Validate that the section name is not empty or whitespace-only
        if not name.strip():
            raise ValueError("Section name cannot be empty.")
        # Check for duplicate section names
        if name in self.sections:
            raise ValueError(f"Section '{name}' already exists.")
        # Add the new section to the inventory
        self.sections[name] = InventorySection(name)

    def get_section(self, name):
        return self.sections.get(name)

    def add_item(self, section_name, name, amount, expiry_date=None):
        """Add an item to a section, raising an error for invalid inputs."""
        if amount < 0:  # Validate that the amount is non-negative
            raise ValueError("Quantity cannot be negative.")
        section = self.get_section(section_name)
        if section:
            section.add_stock(name, amount, expiry_date)
        else:
            raise ValueError(f"Section '{section_name}' not found.")

    def remove_item(self, section_name, name, amount):
        section = self.get_section(section_name)
        if section:
            section.remove_stock(name, amount)
        else:
            raise ValueError("Section not found")

    def move_item(self, source_section, dest_section, name, amount):
        source = self.get_section(source_section)
        dest = self.get_section(dest_section)
        if source and dest:
            item = source.get_item(name)
            if item and item.quantity >= amount:
                source.remove_stock(name, amount)
                dest.add_stock(name, amount)
            else:
                raise ValueError("Not enough stock or item not found")
        else:
            raise ValueError("Section not found")

    def get_inventory_overview(self):
        return "\n".join(str(section) for section in self.sections.values())
