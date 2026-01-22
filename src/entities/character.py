import random
class Character():
    def __init__(self, name, hp, damage):
        self.name = name
        self.__hp = hp
        self.max_hp = hp
        self.damage = damage
    @property
    def hp(self):
        return self.__hp
    @hp.setter
    def hp(self, new_value):
        if new_value < 0:
            self.__hp = 0
        elif new_value > self.max_hp:
             self.__hp = self.max_hp
        else:
            self.__hp = new_value
    def attack(self, target):
        dano_total = self.damage + random.randint(-2, 2)
        target.hp -= dano_total
        return dano_total

class Player(Character):
    def __init__(self, name, hp, damage, inventory):
        super().__init__(name, hp, damage)
        self.level = 1
        self.inventory = inventory
        self.potions = 1



