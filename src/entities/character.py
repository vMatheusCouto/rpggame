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
        dano_total = max(1, self.damage + random.randint(-2, 2))
        target.hp -= dano_total
        return dano_total


class Player(Character):
    def __init__(self, name, hp, damage):
        super().__init__(name, hp, damage)
        self.level = 1
        self.xp = 0
        self.potions = 1
        self.moves = []
        self.learnset = [
            (1, {"name": "Investida", "bonus": 0, "accuracy": 1}),
            (5, {"name": "Golpe Rapido", "bonus": 3, "accuracy": 0.9}),
            (8, {"name": "Corte", "bonus": 6, "accuracy": 0.75}),
            (10, {"name": "Furia", "bonus": 10, "accuracy": 0.5}),
        ]

        self._learn_moves_for_current_level()

    def _learn_moves_for_current_level(self):
        for lvl_req, move in self.learnset:
            if self.level >= lvl_req and not self.has_move(move["name"]):
                if len(self.moves) < 4:
                    self.moves.append(move)

    def has_move(self, move_name: str) -> bool:
        return any(m["name"] == move_name for m in self.moves)

    def use_move(self, move_index: int, target):
        move = self.moves[move_index]
        bonus = move["bonus"]
        accuracy = move.get("accuracy", 1.0)

        if random.random() > accuracy:
            return move["name"], 0, False

        dano_total = max(1, self.damage + bonus + random.randint(-2, 2))
        target.hp -= dano_total
        return move["name"], dano_total, True

    def take_xp(self, xp):
        self.xp += xp
        while self.xp >= 100:
            self.xp -= 100
            self.level += 1
            self.damage += 5
            self.max_hp += 20
            self.hp += 20
            self._learn_moves_for_current_level()


player = Player("Heroi", 100, 15)
