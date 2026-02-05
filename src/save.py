from src.entities.character import player, Enemy, Player
from src.scenarios.world.map import Map
from src.utils.paths import SAVES_DIR
from datetime import datetime
import json
import os

class Save():
    save_list = []
    __selected = None

    def __init__(self, exist, path):
        self.exist = exist
        self.data = {}
        self.path = path

    @classmethod
    def load_saves(self):
        self.save_list = []

        # Carrega todos os saves e identifica se existem ou não
        for index in range(3):
            try:
                with open(SAVES_DIR / f"save_{index+1}.json", 'r') as file:
                    current_save = Save(True, SAVES_DIR / f"save_{index+1}.json")
                    current_save.data = json.load(file)
                    Save.save_list.append(current_save)
            except FileNotFoundError:
                Save.save_list.append(Save(False, SAVES_DIR / f"save_{index+1}.json"))

    @classmethod
    def select_save(cls, index):
        player.reset()
        Enemy.load_enemies()
        cls.__selected = cls.save_list[index]
        if not cls.__selected.exist:
            cls.update_current_save()
            return "new"
        return "old"

    @classmethod
    def update_current_save(cls):

        # Pegar a lista de inimigos derrotados
        defeated_enemies = []
        for key, enemy in Enemy.enemy_list.items():
            if enemy.dead:
                defeated_enemies.append(key)

        # Atualizar o save atual com informações novas
        cls.__selected.data = {
            "player": {
                "hp": player.hp,
                "max_hp": player.max_hp,
                "damage": player.damage,
                "lvl": player.level,
                "xp": player.xp,
                "position": [player.position.x, player.position.y],
                "map": player.map,
            },
            "defeated_enemies": defeated_enemies,
            "last_updated": str(datetime.now())
        }

        # Atualizar o arquivo de save
        with open(cls.__selected.path, 'w', encoding='utf-8') as file:
            json.dump(cls.__selected.data, file, indent=4)

    @classmethod
    def delete_save(cls, index):
        selected_save = cls.save_list[index]
        if selected_save.exist:
            selected_save.exist = False
            if os.path.exists(selected_save.path):
                os.remove(selected_save.path)

    @classmethod
    def load(cls):

        if not cls.__selected.exist:
            cls.update_current_save()
        else:
            data = cls.__selected.data
            player_data = data["player"]

            # Atualização do player
            player.max_hp = player_data["max_hp"]
            player.hp = player_data["hp"]
            player.damage = player_data["damage"]
            player.level = player_data["lvl"]
            player.xp = player_data["xp"]

            player.position.x = player_data["position"][0]
            player.position.y = player_data["position"][1]
            player.map = player_data["map"]

            # Atualização dos inimigos
            for enemy in data["defeated_enemies"]:
                Enemy.enemy_list[enemy].dead = True

    def __str__(self):
        if self.exist:
            return f"LvL {self.data["player"]["lvl"]} - Último salvamento: {self.data["last_updated"]}"
        else:
            return "Vazio"
