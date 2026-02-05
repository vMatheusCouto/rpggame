import pygame
import random
import json
import os

from src.context import context
from src.entities.sprites import entity_sprites
from src.entities.moves.moves import Move
from src.utils.paths import SRC_DIR

class Character():
    def __init__(self, name, hp, damage, path, moves, map="null", position=(0,0)):

        # Atributos de combate
        self.name = name
        self.__hp = hp
        self.max_hp = hp
        self.damage = damage

        self.moves = moves
        self.dead = False

        # Atributos de mapa/sprites
        self.path = path
        self.status = "idle"
        self.direction = "right"
        self.position = position
        self.map = map

        self.sprites = entity_sprites(self)

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

    def get_tile_pos(self):
        tileX = int(self.position.x / (640/80))
        tileY = int(self.position.y / (384/48))
        return (tileX, tileY)

    def reset_status(self):
        self.status = "idle"

    def get_sprite(self):
        return self.sprites.get_sprite()

    def reset_sprite(self, number=0):
        self.sprites.reset_sprite(number)

class Player(Character):
    def __init__(self, name, hp, damage):
        super().__init__(name, hp, damage, "player", [], "spawn", pygame.Vector2(150,250))
        # Progresso
        self.level = 1
        self.xp = 0
        # Poções (temporário)
        self.potions = 1
        self.moves: list[Move] = []
        self.learnset = [
            (1,  Move.moves_list["investida"]),
            (5,  Move.moves_list["fatiar"]),
            (8,  Move.moves_list["corte_rapido"]),
            (10, Move.moves_list["foice_da_morte"]),
        ]
        self._learn_moves_for_current_level()

        # Valores iniciais de movimentação
        self.moving = False
        self.speed = 35

    def _learn_moves_for_current_level(self):
        for lvl_req, move in self.learnset:
            if self.level >= lvl_req and not self.has_move(move.name):
                if len(self.moves) < 4:
                    self.moves.append(move)

    def has_move(self, move_name: str) -> bool:
        return any(m.name == move_name for m in self.moves)

    def use_move(self, move_index: int, target):
        move = self.moves[move_index]

        if not move.roll_hit():
            return move.name, 0, False

        dano_total = max(1, self.damage + move.bonus + random.randint(-2, 2))
        target.hp -= dano_total
        return move.name, dano_total, True

    def xp_to_next(self):
        return int(100 * (1.35 * (self.level - 1)))

    def take_xp(self, xp):
        self.xp += xp
        while self.xp >= self.xp_to_next():
            self.xp -= self.xp_to_next()
            self.level += 1
            self.damage += int(2 + self.level * 0.6)
            hp_gain = 20 + int(2 * self.level * 0.45)
            self.max_hp += hp_gain
            self.hp += hp_gain
            self._learn_moves_for_current_level()

    def reset(self):
        self.__init__("Heroi", 100, 15)

class Enemy(Character):
    enemy_list = {}
    def __init__(self, name, hp, damage, drop_xp, path, map_name, position, moves=[], dialog=[]):
        super().__init__(name, hp, damage, path, moves, map_name, position)
        self.drop_xp = drop_xp
        self.dialog = dialog

    @classmethod
    def load_enemies(cls):
        enemiesFolder = SRC_DIR / "entities/enemies/"
        entries = os.listdir(enemiesFolder)
        for enemy in sorted(entries):
            with open(enemiesFolder / enemy, 'r') as file:
                data = json.load(file)
                current_moves = []
                for move in data["moves"]:
                    current_moves.append(Move.moves_list[move])
                current_enemy = Enemy(
                    name=data["name"],
                    hp=data["hp"],
                    damage=data["damage"],
                    drop_xp=data["drop_xp"],
                    path=f'enemies/{data["path"]}',
                    map_name=data["map"],
                    position=(data["position"][0], data["position"][1]),
                    moves=current_moves,
                    dialog=data["dialog"]
                )
                cls.enemy_list[data["name"]] = current_enemy

    def use_random_move(self, target):
        move = random.choice(self.moves)
        if not move.roll_hit():
            return move.name, 0, False
        dano_total = max(1, self.damage + move.bonus + random.randint(-2, 2))
        target.hp -= dano_total
        return move.name, dano_total, True

player = Player("Heroi", 100, 15)
