from src.entities.character import Character
from src.utils.paths import SRC_DIR
from src.entities.player.sprites import entitySprites
import os
import json
class Enemy(Character):
    enemyList = []
    def __init__(self, name, hp, damage, drop_xp, path,position):
        super().__init__(name, hp, damage)
        self.enemy_path = path
        self.drop_xp = drop_xp
        self.path = path
        self.status = "idle"
        self.direction = "left"
        self.sprites = None
        self.position = position

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

enemiesFolder = SRC_DIR / "entities/enemy/enemies/"
entries = os.listdir(enemiesFolder)
for enemy in sorted(entries):
    try:
        with open(enemiesFolder / enemy, 'r') as file:
            data = json.load(file)
            currentEnemy = Enemy(
                name=data["name"],
                hp=data["hp"],
                damage=data["damage"],
                drop_xp=data["drop_xp"],
                path=f"enemies/{data["path"]}",
                position=(140,180)
            )
            enemySprite = entitySprites(currentEnemy)
            currentEnemy.setSprites(enemySprite)
            Enemy.enemyList.append(currentEnemy)

    except FileNotFoundError:
        print("Error: The file", enemy, "was not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from the file: {e}")

for index, item in enumerate(Enemy.enemyList):
    print(f"{index} - {item.name}")
