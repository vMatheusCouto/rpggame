from src.entities.inventory.catalogue import CATALOGUE_ITEM
from src.entities.inventory.item import Item, Potion

class Inventory:
    items = {}

    def __init__(self):
        self.items_list = []

    @classmethod
    def load_items(cls):
        for key, data in CATALOGUE_ITEM.items():
            if data["type"] == "cura":
                cls.items[key] = Potion(
                    type=data["type"],
                    name=data["name"],
                    display_name=data["display_name"],
                    description=data["description"],
                    heal_value=data["heal_value"]
                )

    def add_item(self, item):
        if hasattr(item, "use"):
            self.items_list.append(item)

    def use_item(self, item, target):
        if item in self.items_list:
            item.use(target)
            self.items_list.remove(item)

    def list_items(self):
        items = []
        for item in list(set(self.items_list)):
            items.append((item, self.items_list.count(item)))
        return items
