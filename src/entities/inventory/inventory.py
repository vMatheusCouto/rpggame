import json
import os
from src.utils.paths import SRC_DIR
from src.entities.inventory.item import Item, Potion

class Inventory:
    items = {}

    def __init__(self):
        self.items_list = []

    @classmethod
    def load_items(cls):
        path = SRC_DIR / "entities/inventory/items.json"

        with open(path, "r") as file:
            data = json.load(file)

        for key, value in data.items():
            if value["type"] == "cura":
                cls.items[key] = Potion(
                    type=value["type"],
                    name=value["name"],
                    display_name=value["display_name"],
                    description=value["description"],
                    heal_value=value["heal_value"]
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
