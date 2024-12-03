from RegularItems import RegularItem, PerishableItem

class InventorySection:
    def __init__(self, name):
        self.name = name
        self.items = {}

    def add_item(self, item):
        self.items[item.name] = item

    def get_item(self, name):
        return self.items.get(name)

    def add_stock(self, name, amount, expiry_date=None):
        item = self.get_item(name)
        if item:
            item.add_stock(amount)
        else:
            if expiry_date:
                item = PerishableItem(name, amount, expiry_date)
            else:
                item = RegularItem(name, amount)
            self.add_item(item)

    def remove_stock(self, name, amount):
        item = self.get_item(name)
        if item:
            item.remove_stock(amount)
        else:
            raise ValueError("Item not found")

    def __str__(self):
        return f"Section: {self.name}\n" + "\n".join(str(item) for item in self.items.values())
