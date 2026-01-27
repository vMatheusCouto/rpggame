from abc import ABC, abstractmethod
from src.scenarios.world.overworld.movement import *
from src.entities.character import Character, Player, player
from src.entities.enemy.enemies import Enemy
from src.utils.paths import BATTLE_ASSETS, CHARACTER_ASSETS
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
    def __init__(self, player_battle):
        super().__init__(BATTLE_ASSETS/"forest/background2")

        from src.props import props
        self.screen_w = props.getScreen().get_width()
        self.screen_h = props.getScreen().get_height()

        self.player_battler = player
        self.enemy_battler = Enemy("Goblin", 100, 15, 30)
        self.player_sprite = pygame.image.load(
        CHARACTER_ASSETS/"idle/up/characterbase1.png"
)       .convert_alpha()
        self.enemy_sprite = pygame.image.load(
        BATTLE_ASSETS/"enemy/enemy.png"
        ).convert_alpha()
        self.player_sprite = pygame.transform.scale(self.player_sprite, (96, 96))
        self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (96, 96))

        self.menu_items = ["Lutar", "Bolsa", "Fugir"]
        self.menu_index = 0

        self.message_queue = []
        self.in_message = False

        self._pressed = {"up": False, "down": False, "z": False, "x": False}

        self.request_exit = False
        self.battle_over = False

        pygame.font.init()
        self.font = pygame.font.Font(None, 18)
        self.font_big = pygame.font.Font(None, 20)

    def _edge(self, key_name: str, is_down: bool) -> bool:
        if is_down and not self._pressed[key_name]:
            self._pressed[key_name] = True
            return True
        if not is_down:
            self._pressed[key_name] = False
        return False

    def _push_msg(self, text: str):
        self.message_queue.append(text)
        self.in_message = True

    def _next_msg(self):
        if self.message_queue:
            self.message_queue.pop(0)
        if not self.message_queue:
            self.in_message = False

    def _hp_ratio(self, battler):
        if battler.max_hp <= 0:
            return 0
        return max(0, min(1, battler.hp / battler.max_hp))

    def _draw_panel(self, screen, rect, border=2):
        pygame.draw.rect(screen, (128,128,128), rect, border_radius=6)
        pygame.draw.rect(screen, (245, 245, 245), rect, width=border, border_radius=6)

    def _draw_text(self, screen, text, x, y, big=False):
        surf = (self.font_big if big else self.font).render(text, True, (255, 255, 255))
        screen.blit(surf, (x, y))

    def _draw_hp_box(self, screen, x, y, name, level, battler, box_w=220, box_h=64):
        box = pygame.Rect(x, y, box_w, box_h)
        self._draw_panel(screen, box)

        self._draw_text(screen, f"{name}", x + 10, y + 8, big=True)
        self._draw_text(screen, f"Lv {level}", x + box_w - 55, y + 10)

        bar_x = x + 10
        bar_y = y + 32
        bar_w = box_w - 20
        bar_h = 10

        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_w, bar_h))
        ratio = self._hp_ratio(battler)
        fill_w = int(bar_w * ratio)

        if ratio > 0.5:
            color = (60, 200, 80)
        elif ratio > 0.2:
            color = (220, 200, 60)
        else:
            color = (220, 70, 70)

        pygame.draw.rect(screen, color, (bar_x, bar_y, fill_w, bar_h))

        self._draw_text(screen, f"{battler.hp}/{battler.max_hp}", x + box_w - 95, y + 46)

    def keyActions(self, keys):
        up = self._edge("up", keys[pygame.K_w])
        down = self._edge("down", keys[pygame.K_s])
        z = self._edge("z", keys[pygame.K_z])
        x = self._edge("x", keys[pygame.K_x])

        if self.in_message:
            if z:
                self._next_msg()
            return

        if self.battle_over:
            if z:
                self.request_exit = True
            return

        if up:
            self.menu_index = (self.menu_index - 1) % len(self.menu_items)
        if down:
            self.menu_index = (self.menu_index + 1) % len(self.menu_items)

        if z:
            choice = self.menu_items[self.menu_index]
            if choice == "Lutar":
                self.attack_turn()
            elif choice == "Bolsa":
                self._push_msg("Voce abriu a Bolsa...")
            elif choice == "Fugir":
                self._push_msg("Voce fugiu da batalha!")
                self.battle_over = True

        if x:
            pass

    def attack_turn(self):
        if self.player_battler.hp <= 0 or self.enemy_battler.hp <= 0:
            return

        damage = self.player_battler.attack(self.enemy_battler)
        self._push_msg(f"Voce causou {damage} de dano!")

        if self.enemy_battler.hp <= 0:
            self._push_msg("Inimigo derrotado!")
            self._push_msg("VITORIA!")
            xp = self.enemy_battler.drop_xp
            self.player_battler.take_xp(xp)
            self._push_msg(f"Você ganhou {xp} pontos de experiencia")
            self.battle_over = True
            return

        enemy_damage = self.enemy_battler.attack(self.player_battler)
        self._push_msg(f"{self.enemy_battler.name} causou {enemy_damage}!")

        if self.player_battler.hp <= 0:
            self._push_msg("DERROTA...")
            self.battle_over = True

    def render(self, screen):

        enemy_x = self.screen_w - 190
        enemy_y = 70
        screen.blit(self.enemy_sprite, (enemy_x, enemy_y))

        player_x = 90
        player_y = self.screen_h - 210
        screen.blit(self.player_sprite, (player_x, player_y))

        self._draw_hp_box(
            screen,
            x=self.screen_w - 260,
            y=20,
            name=self.enemy_battler.name,
            level=3,
            battler=self.enemy_battler,
            box_w=240,
            box_h=64
        )

        self._draw_hp_box(
            screen,
            x=20,
            y=self.screen_h - 150,
            name=self.player_battler.name,
            level=self.player_battler.level,
            battler=self.player_battler,
            box_w=240,
            box_h=72
        )
        self._draw_text(
            screen,
            f"XP: {self.player_battler.xp}/100",
            30,
            self.screen_h - 58
        )

        box = pygame.Rect(0, self.screen_h - 96, self.screen_w, 96)
        self._draw_panel(screen, box, border=3)

        if self.in_message and self.message_queue:
            msg = self.message_queue[0]
            self._draw_text(screen, msg, 18, self.screen_h - 80, big=True)
            self._draw_text(screen, "Z: continuar", self.screen_w - 110, self.screen_h - 28)
        elif self.battle_over:
            self._draw_text(screen, "Z: voltar", self.screen_w - 95, self.screen_h - 28)
        else:
            start_x = self.screen_w - 190
            start_y = self.screen_h - 86
            for i, item in enumerate(self.menu_items):
                y = start_y + i * 22
                prefix = "▶ " if i == self.menu_index else "  "
                self._draw_text(screen, prefix + item, start_x, y, big=True)

