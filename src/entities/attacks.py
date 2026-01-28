import random

class Attack():
    def __init__(self, name, bonus, accuracy):
        self.name = name
        self.bonus = bonus
        self.accuracy =  accuracy
    def roll_hit(self):
        return random.random() <= self.accuracy
