from src.entities.character import Character
from src.utils.paths import SRC_DIR
import os
import json
class Enemy(Character):
    enemyList = []
    def __init__(self, name, hp, damage, drop_xp, path):
        super().__init__(name, hp, damage)
        self.enemy_path = path
        self.drop_xp = drop_xp

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
                path=data["path"]
            )
            Enemy.enemyList.append(currentEnemy)

    except FileNotFoundError:
        print("Error: The file", enemy, "was not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from the file: {e}")

for index, item in enumerate(Enemy.enemyList):
    print(f"{index} - {item.name}")
