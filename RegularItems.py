from BaseInventoryItem import InventoryItem

class RegularItem(InventoryItem):
    """A non-perishable item with basic stock management."""
    def add_stock(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        self.quantity += amount

    def remove_stock(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if amount > self.quantity:
            raise ValueError("Not enough stock.")
        self.quantity -= amount

    def __str__(self):
        return f"{self.name}: {self.quantity}"

class PerishableItem(InventoryItem):
    """A perishable item with an expiry date."""
    def __init__(self, name, quantity, expiry_date):
        super().__init__(name, quantity)
        self.expiry_date = expiry_date

    def add_stock(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        self.quantity += amount

    def remove_stock(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if amount > self.quantity:
            raise ValueError("Not enough stock.")
        self.quantity -= amount

    def __str__(self):
        return f"{self.name} (Expires: {self.expiry_date}): {self.quantity}"






