from src.entities.character import Character

class Enemy(Character):
    def __init__(self, name, hp, damage):
        super().__init__(name, hp, damage)
        self.enemy_path = "Goblin"

