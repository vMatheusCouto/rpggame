from abc import ABC, abstractmethod
from src.scenarios.world.overworld.movement import *
from src.entities.character import Character, Player, player
from src.entities.enemy.enemies import Enemy
from src.utils.paths import BATTLE_ASSETS, CHARACTER_ASSETS, ASSETS_DIR
from src.props import props
from src.entities.player.sprites import entitySprites
import pygame
class Scenario(ABC):
    def __init__(self, imagePath):
        self.imagePath = imagePath

    @abstractmethod
    def keyActions():
        pass

class ScenarioOpenWorld(Scenario):
    def __init__(self, name, imagePath, blockedTiles, topLayerPath, spawn_position, eventTiles, entities):
        super().__init__(imagePath)
        self.name = name
        self.blockedTiles = blockedTiles
        self.events = []
        self.topLayerPath = topLayerPath
        self.spawn_position = spawn_position
        self.eventTiles = eventTiles
        self.entities = entities

    def setSpawnPosition(self, position):
        self.spawn_position = position

    def keyActions(self, keys, blockedTiles, eventTiles):
        canMove = True
        event = None
        running = False
        props.setSpeed(35)
        if keys[pygame.K_LSHIFT]:
            props.setSpeed(60)
            running = True
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
        if not canMove and running:
            props.setStatus("running")
        return event

class ScenarioDialogue(Scenario):
    pass

class ScenarioBattle(Scenario):
    def __init__(self, player_battle, enemy_battle, backgroundName):
        super().__init__(BATTLE_ASSETS / f"{backgroundName}/background.png")
        from src.props import props
        self.life_hud_img = pygame.image.load(BATTLE_ASSETS / "life_hud.png").convert_alpha()
        self.life_hud_img_inverted = pygame.image.load(BATTLE_ASSETS / "life_hud.png").convert_alpha()
        self.hudBar = (92,90)
        self.enemyHudBar = (370,90)
        self.screen_w = props.getScreen().get_width()
        self.screen_h = props.getScreen().get_height()
        self.player_battler = player_battle
        self.enemy_battler = enemy_battle
        self.heroSprites = entitySprites(props)

        # Menu principal
        self.menu_items = ["Lutar", "Bolsa", "Fugir"]
        self.menu_index = 0

        # Submenu de golpes
        self.ui_mode = "main"
        self.fight_index = 0

        # Mensagens
        self.message_queue = []
        self.in_message = False

        # Debounce das teclas
        self._pressed = {"up": False, "down": False, "z": False, "x": False}

        # Controle de saída
        self.request_exit = False
        self.battle_over = False
        # Tremor (shake) quando toma hit
        self.player_hit_timer = 0
        self.enemy_hit_timer = 0
        self.shake_strength = 4   # pixels
        self.pending_enemy_attack = False

        # Fonts
        pygame.font.init()
        self.font = pygame.font.Font(ASSETS_DIR / "Pixeled.ttf", 5)
        self.font_big = pygame.font.Font(ASSETS_DIR / "Pixellari.ttf", 16)

    def _edge(self, key_name: str, is_down: bool) -> bool:
        """True só no frame em que a tecla foi pressionada (debounce)."""
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
        #contra ataque agendado
        if not self.message_queue and self.pending_enemy_attack and not self.battle_over:
            self.pending_enemy_attack = False
            move_name, dmg, hit = self.enemy_battler.use_random_move(self.player_battler)
            self._push_msg(f"{self.enemy_battler.name} usou {move_name}!")
            if hit:
                self._push_msg(f"Causou {dmg} de dano!")
                self.player_hit_timer = 10
            else:
                self._push_msg("Mas errou!")

                self.player_hit_timer = 10

            if self.player_battler.hp <= 0:
                self._push_msg("DERROTA...")
                self.battle_over = True

    def _hp_ratio(self, battler):
        if battler.max_hp <= 0:
            return 0
        return max(0, min(1, battler.hp / battler.max_hp))

    def _shake_offset(self, timer: int):
        if timer <= 0:
            return 0, 0
        dx = self.shake_strength if (timer % 2 == 0) else -self.shake_strength
        return dx, 0

    def _draw_panel(self, screen, rect, border=2):
        pygame.draw.rect(screen, (128, 128, 128), rect, border_radius=6)
        pygame.draw.rect(screen, (245, 245, 245), rect, width=border, border_radius=6)

    def _draw_text(self, screen, text, x, y, big=False):
        surf = (self.font_big if big else self.font).render(text, True, (255, 255, 255))
        screen.blit(surf, (x, y))

    def _draw_hp_box(self, screen, x, y, name, level, battler, box_w=240, box_h=64):
        box = pygame.Rect(x, y, box_w, box_h)

        self._draw_text(screen, f"{name}", x + 2, y - 25, big=True)
        # self._draw_text(screen, f"Lv {level}", x + 98, y - 25)

        bar_x = x + 10
        bar_y = y + 32
        bar_w = 132
        bar_h = 6

        pygame.draw.rect(screen, (0, 0, 0), (x, y, bar_w, bar_h))

        ratio = self._hp_ratio(battler)
        fill_w = int(bar_w * ratio)
        print(f"f{bar_w}")

        color = (210, 14, 16)
        pygame.draw.rect(screen, color, (x, y, fill_w, bar_h))
        self._draw_text(screen, f"{battler.hp}/{battler.max_hp}", x + box_w - 140, y + 8)

    def _fight_items(self):
        move_names = [m.name for m in getattr(self.player_battler, "moves", [])]
        move_names = move_names[:4]
        return move_names + ["Voltar"]

    def keyActions(self, keys):
        up = self._edge("up", keys[pygame.K_w])
        down = self._edge("down", keys[pygame.K_s])
        z = self._edge("z", keys[pygame.K_RETURN])
        x = self._edge("x", keys[pygame.K_x])

        if self.in_message:
            if z:
                self._next_msg()
            return

        if self.battle_over:
            if z:
                self.request_exit = True
            return

        # Submenu de golpes
        if self.ui_mode == "fight":
            items = self._fight_items()

            if up:
                self.fight_index = (self.fight_index - 1) % len(items)
            if down:
                self.fight_index = (self.fight_index + 1) % len(items)

            if x:
                self.ui_mode = "main"
                return

            if z:
                choice = items[self.fight_index]

                if choice == "Voltar":
                    self.ui_mode = "main"
                    return

                move_index = self.fight_index
                move_name, damage, hit = self.player_battler.use_move(move_index, self.enemy_battler)

                self._push_msg(f"{self.player_battler.name} usou {move_name}!")

                if hit:
                    self._push_msg(f"Causou {damage} de dano!")
                    self.enemy_hit_timer = 10
                else:
                    self._push_msg("Mas errou!")


                if self.enemy_battler.hp <= 0:
                    self._push_msg("Inimigo derrotado!")

                    xp = self.enemy_battler.drop_xp
                    lvl_before = self.player_battler.level
                    self.player_battler.take_xp(xp)
                    self._push_msg(f"Voce ganhou {xp} XP!")

                    if self.player_battler.level > lvl_before:
                        self._push_msg(f"SUBIU PARA O NIVEL {self.player_battler.level}!")

                    self._push_msg("VITORIA!")
                    self.battle_over = True
                    self.ui_mode = "main"
                    return
                # agenda o contra-ataque
                self.pending_enemy_attack = True

                if self.player_battler.hp <= 0:
                    self._push_msg("DERROTA...")
                    self.player_battle.hp = self.player_battle.max_hp
                    self.battle_over = True

                self.ui_mode = "main"
            return

        #Menu principal
        if up:
            self.menu_index = (self.menu_index - 1) % len(self.menu_items)
        if down:
            self.menu_index = (self.menu_index + 1) % len(self.menu_items)

        if z:
            choice = self.menu_items[self.menu_index]

            if choice == "Lutar":
                self.ui_mode = "fight"
                self.fight_index = 0

            elif choice == "Bolsa":
                if hasattr(self.player_battler, "potions") and self.player_battler.potions > 0:
                    self.player_battler.potions -= 1
                    self.player_battler.hp += 30
                    self._push_msg("Voce usou uma pocao! +30 HP")
                else:
                    self._push_msg("Sem pocoes!")

            elif choice == "Fugir":
                self._push_msg("Voce fugiu da batalha!")
                self.battle_over = True

    def render(self, screen):
        # Sprites
        enemy_x = self.screen_w - 230
        enemy_y = 120
        dx, dy = self._shake_offset(self.enemy_hit_timer)

        enemy_frame = self.enemy_battler.getSprite().convert_alpha()
        enemy_sprite = pygame.transform.scale(enemy_frame, (96, 96))

        screen.blit(enemy_sprite, (enemy_x + dx, enemy_y + dy))

        player_x = 130
        player_y = 120
        props.setStatus("idle")
        props.setDirection("right")

        player_frame = self.heroSprites.getSprite().convert_alpha()
        player_frame = pygame.transform.scale(player_frame, (96, 96))

        dx, dy = self._shake_offset(self.player_hit_timer)
        screen.blit(player_frame, (player_x + dx, player_y + dy))


        if self.enemy_hit_timer > 0:
            self.enemy_hit_timer -= 1
        if self.player_hit_timer > 0:
            self.player_hit_timer -= 1

        # HUD inimigo
        self._draw_hp_box(
            screen,
            x=self.enemyHudBar[0] + 21,
            y=self.enemyHudBar[1] + 13,
            name=self.enemy_battler.name,
            level=3,
            battler=self.enemy_battler,
            box_w=240,
            box_h=64
        )
        # HUD player
        self._draw_hp_box(
            screen,
            x=self.hudBar[0] + 21,
            y=self.hudBar[1] + 13,
            name=self.player_battler.name,
            level=self.player_battler.level,
            battler=self.player_battler,
            box_w=240,
            box_h=64
        )

        screen.blit(self.life_hud_img, self.hudBar)
        screen.blit(self.life_hud_img_inverted, self.enemyHudBar)

        # Mostrar XP
        self._draw_text(
            screen,
            f"XP: {self.player_battler.xp}/100",
            x=self.enemyHudBar[0] - 260,
            y=self.enemyHudBar[1] + 26,
        )
        # Mensagens ou menus
        if self.in_message and self.message_queue:
            msg = self.message_queue[0]
            self._draw_text(screen, msg, 18, self.screen_h - 80, big=True)
            self._draw_text(screen, "ENTER: continuar", self.screen_w - 110, self.screen_h - 28)

        elif self.battle_over:
            self._draw_text(screen, "ENTER: voltar", self.screen_w - 95, self.screen_h - 28)

        else:
            start_x = self.screen_w - 240
            start_y = self.screen_h - 86

            if self.ui_mode == "main":
                # Menu principal
                for i, item in enumerate(self.menu_items):
                    y = start_y + i * 22
                    prefix = "> " if i == self.menu_index else "  "
                    self._draw_text(screen, prefix + item, start_x + 50, y, big=True)

            elif self.ui_mode == "fight":
                # Submenu de golpes
                items = self._fight_items()
                for i, item in enumerate(items):
                    y = start_y + i * 22
                    prefix = "> " if i == self.fight_index else "  "
                    self._draw_text(screen, prefix + item, start_x + 10, y, big=True)

