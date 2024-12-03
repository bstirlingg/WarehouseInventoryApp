class InventoryItem:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def add_stock(self, amount):
        raise NotImplementedError("Subclasses must implement add_stock method.")

    def remove_stock(self, amount):
        raise NotImplementedError("Subclasses must implement remove_stock method.")

    def __str__(self):
        return f"{self.name}: {self.quantity}"