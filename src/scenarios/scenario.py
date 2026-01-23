from abc import ABC, abstractmethod
from src.scenarios.world.overworld.movement import *
from src.entities.character import Character, Player
from src.entities.enemy.enemies import Enemy
from src.utils.paths import BATTLE_ASSETS
import pygame
class Scenario(ABC):
    def __init__(self, imagePath):
        self.imagePath = imagePath

    @abstractmethod
    def keyActions():
        pass

class ScenarioOpenWorld(Scenario):
    def __init__(self, imagePath, blockedTiles, topLayerPath, spawn_position, eventTiles):
        super().__init__(imagePath)
        self.blockedTiles = blockedTiles
        self.events = []
        self.topLayerPath = topLayerPath
        self.spawn_position = spawn_position
        self.eventTiles = eventTiles

    def setSpawnPosition(self, position):
        self.spawn_position = position

    def keyActions(self, keys, blockedTiles, eventTiles):
        canMove = True
        event = None
        props.setSpeed(35)
        if keys[pygame.K_LSHIFT]:
            props.setSpeed(60)
        if keys[pygame.K_w] and canMove:
            event = walkUp(blockedTiles, eventTiles)
            canMove = False
        if keys[pygame.K_s] and canMove:
            event = walkDown(blockedTiles, eventTiles)
            canMove = False
        if keys[pygame.K_a] and canMove:
            event = walkLeft(blockedTiles, eventTiles)
            canMove = False
        if keys[pygame.K_d] and canMove:
            event = walkRight(blockedTiles, eventTiles)
            canMove = False
        return event

class ScenarioDialogue(Scenario):
    pass

class ScenarioBattle(Scenario):
    def __init__(self):
        super().__init__(BATTLE_ASSETS/"forest/background")
        self.player_battler = Player("Heroi", 100, 15)
        self.enemy_battler = Enemy("Goblin", 50, 5)
        self.can_attack = True
        print(f"Batalha: {self.player_battler.name} vs {self.enemy_battler.name}")

    def keyActions(self, keys):
        if not keys[pygame.K_z]:
            self.can_attack = True
        if keys[pygame.K_z] and self.can_attack:
            self.attack_turn()
            self.can_attack = False

    def attack_turn(self):
        if self.player_battler.hp > 0 and self.enemy_battler.hp > 0:
            damage = self.player_battler.attack(self.enemy_battler)
            print(f'VC causou {damage}! O inimigo tem {self.enemy_battler.hp} pontos de vida')
            if self.enemy_battler.hp <= 0:
                print(f"VITÓRIA!")
                return

            enemy_damage = self.enemy_battler.attack(self.player_battler)
            print(f"Goblin casou {enemy_damage}de dano! Seu HP: {self.player_battler.hp}")

            if self.player_battler.hp <= 0:
                print("DERROTA")
