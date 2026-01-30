import random
import os
import json
from src.utils.paths import SRC_DIR

class Attack():
    list = {}

    def __init__(self, name, bonus, accuracy):
        self.name = name
        self.bonus = bonus
        self.accuracy =  accuracy
    def roll_hit(self):
        return random.random() <= self.accuracy

    @classmethod
    def load_attacks(cls):
        path = SRC_DIR / "entities/moves.json"

        with open(path, "r") as file:
            data = json.load(file)

        for key, value in data.items():
            cls.list[key] = Attack(
                name=value["name"],
                bonus=value["bonus"],
                accuracy=value["accuracy"]
            )
