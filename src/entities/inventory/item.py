from abc import ABC, abstractmethod
class Item(ABC):

    @abstractmethod
    def use(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

class Potion(Item):
    def __init__(self, type, name, display_name, description, heal_value):
        self.type = type
        self._name = name
        self.display_name = display_name
        self._description = description
        self.heal_value = heal_value

    def use(self, target):
        target.hp += self.heal_value

    def __str__(self):
        return f"{self.display_name}"
