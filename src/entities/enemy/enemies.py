from src.entities.character import Character
from src.utils.paths import SRC_DIR
from src.entities.player.sprites import entitySprites
import random
from src.entities.attacks import Attack
import os
import json

# Tirar isso daqui: deve ser junto de character.py; transformar pasta "enemies" na pasta "enemy", substituindo-as.

class Enemy(Character):
    enemyList = []
    def __init__(self, name, hp, damage, drop_xp, path, mapName, position, direction="left", moves=[]):
        super().__init__(name, hp, damage)
        self.enemy_path = path
        self.drop_xp = drop_xp
        self.path = path
        self.status = "idle"
        self.direction = direction
        self.sprites = None
        self.mapName = mapName
        self.position = position
        self.moves = moves
        self.defeated = False

    @classmethod
    def load_enemies(cls):
        enemiesFolder = SRC_DIR / "entities/enemy/enemies/"
        entries = os.listdir(enemiesFolder)
        for enemy in sorted(entries):
            try:
                with open(enemiesFolder / enemy, 'r') as file:
                    data = json.load(file)
                    moves = []
                    for move in data["moves"]:
                        moves.append(Attack.list[move])
                    currentEnemy = Enemy(
                        name=data["name"],
                        hp=data["hp"],
                        damage=data["damage"],
                        drop_xp=data["drop_xp"],
                        path=f'enemies/{data["path"]}',
                        mapName=data["map"],
                        position=(data["position"][0], data["position"][1]),
                        moves=moves
                    )
                    enemySprite = entitySprites(currentEnemy)
                    currentEnemy.setSprites(enemySprite)
                    cls.enemyList.append(currentEnemy)

            except FileNotFoundError:
                print("File", enemy, "not found.")
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")

            for index, item in enumerate(Enemy.enemyList):
                print(f"{index} - {item.name}")

    def use_random_move(self, target):
        move = random.choice(self.moves)
        if not move.roll_hit():
            return move.name, 0, False
        dano_total = max(1, self.damage + move.bonus + random.randint(-2, 2))
        target.hp -= dano_total
        return move.name, dano_total, True

    def setSprites(self, sprite):
        self.sprites = sprite

    def getSprite(self):
        return self.sprites.getSprite()

    def getStatus(self):
        return self.status

    def getDirection(self):
        return self.direction

    def setStatus(self, status):
        self.status = status

    def setDirection(self, direction):
        self.direction = direction
