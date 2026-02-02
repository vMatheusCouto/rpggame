import random
import pygame
import json
import os

from abc import ABC, abstractmethod
from src.scenarios.world.movement import *
from src.entities.character import player, Enemy
from src.utils.paths import BATTLE_ASSETS, CHARACTER_ASSETS, ASSETS_DIR
from src.context import context
from src.entities.sprites import entity_sprites
from src.scenarios.world.map import Map
from src.scenarios.world.movement import Walk
from src.entities.collision import entity_collision

from src.save import Save

class Scene(ABC):

    def __init__(self):
        self.id = random.randint(100000, 999999)

        # Gerenciamento de fontes
        pygame.font.init()
        self.font = pygame.font.Font(ASSETS_DIR / "Pixeled.ttf", 5)
        self.font_big = pygame.font.Font(ASSETS_DIR / "Pixellari.ttf", 16)

        # Debounce
        self._pressed = {"up": False, "down": False, "enter": False, "x": False, "F2": False, "space": False}

    def switch_scene(self, scene):
        context.add_scene = scene
        Save.update_current_save()

    @abstractmethod
    def render():
        pass

    @abstractmethod
    def handle_input():
        pass

    def _edge(self, key_name: str, is_down: bool) -> bool:
        """True só no frame em que a tecla foi pressionada (debounce)."""
        if is_down and not self._pressed[key_name]:
            self._pressed[key_name] = True
            return True
        if not is_down:
            self._pressed[key_name] = False
        return False

    def __str__(self):
        return self.id

class SceneWorld(Scene):

    def __init__(self):
        super().__init__()

        # Estado da cena
        self.__active = False
        self.map = Map.get_map_by_name(player.map)

        self.walk = Walk()

        # Elementos da tela
        self.coordinates = False

        # Reinicializar player
        player.reset_status()

    def render(self):
        # Renderiza o background
        context.screen.blit(self.map.background, (0, 0))

        # Renderiza todos os inimigos do mapa atual
        for key, enemy in Enemy.enemy_list.items():
            if enemy.map == self.map.name:
                if not enemy.dead:
                    context.screen.blit(enemy.get_sprite(), (enemy.position[0] - 16, enemy.position[1] - 24))

        # Renderiza o player
        context.screen.blit(player.get_sprite(), (player.position.x - 16, player.position.y - 24))

        # Renderiza o top layer
        context.screen.blit(self.map.top_layer, (0, 0))

        # Renderiza as coordenadas
        if self.coordinates:
            (tileX, tileY) = player.get_tile_pos()
            text_surface = self.font.render(
                f"x = {int(player.position.x)} ({int(tileX)}) z = {int(player.position.y)} ({int(tileY)})",
                True, (255, 255, 255)
            )
            context.screen.blit(text_surface, (10, 10))

    def switch_map(self, new_map, position):
        player.map = new_map.name
        player.position = pygame.Vector2(position[0], position[1])

        # Nova cena criada com base no novo mapa atual do usuário
        self.switch_scene(SceneWorld())

    def move_back(self):
        if player.direction == "down":
            self.walk.up()
            self.walk.stopped("down")
        if player.direction == "up":
            self.walk.down()
            self.walk.stopped("up")
        if player.direction == "right":
            self.walk.left()
            self.walk.stopped("right")
        if player.direction == "left":
            self.walk.right()
            self.walk.stopped("left")

    def handle_event(self):

        # Iniciar batalha com inimigos pelo mapa
        for key, enemy in Enemy.enemy_list.items():
            if enemy.map == player.map:
                if entity_collision(player.position, enemy.position):
                    if not enemy.dead:
                        self.move_back()
                        self.start_battle(enemy)

        tile = self.map.get_tile_details(player.get_tile_pos())
        if tile:
            # Colisão com o mapa
            if tile["type"] == "block":
                self.move_back()

            # Trocar de mapa
            if tile["type"] == "event":
                event = self.map.get_event_details(tile["id"])
                if event["type"] == "mapevent":
                    self.switch_map(Map.get_map_by_name(event["subtype"]), event["pos"])

        # Encontrar inimigos ao andar caso esteja na caverna (mockado)
        if player.map == "cave":
            if player.status == "walking" or player.status == "running":
                if random.randint(1, 80) == 2:
                    if random.randint(1, 4) == 3:
                        self.start_battle(Enemy.enemy_list["Orc"])
                    else:
                        self.start_battle(Enemy.enemy_list["Skeleton"])

    def handle_input(self, keys):

        if self._edge("f2", keys[pygame.K_F2]):
            self.coordinates = not self.coordinates

        # Redefinir velocidade
        player.speed = 35

        # Correr
        if keys[pygame.K_LSHIFT]:
            running = True
            player.speed = 60

        if keys[pygame.K_w]:
            self.walk.up()

        elif keys[pygame.K_s]:
            self.walk.down()

        elif keys[pygame.K_a]:
            self.walk.left()

        elif keys[pygame.K_d]:
            self.walk.right()

        else:
            player.status = "idle"
            return

        # Animação definida após os botões para garantir que "running" sobreponha "walking"
        if keys[pygame.K_LSHIFT]:
            player.status = "running"

    def start_battle(self, enemy):
        self.switch_scene(SceneBattle(player, enemy))

class SceneBattle(Scene):
    def __init__(self, player_battler, enemy_battler):
        super().__init__()

        # Definições iniciais
        self.screen_w = context.screen.get_width()
        self.screen_h = context.screen.get_height()
        self.player_battler = player_battler
        self.enemy_battler = enemy_battler

        # Carregamento de imagens
        self.background_image = pygame.image.load(BATTLE_ASSETS / f"{player.map}/background.png")
        self.life_hud_img = pygame.image.load(BATTLE_ASSETS / "life_hud.png").convert_alpha()
        self.life_hud_img_inverted = pygame.image.load(BATTLE_ASSETS / "life_hud.png").convert_alpha()

        # Ajustes iniciais player e inimigo
        player.status = "idle"
        player.direction = "right"

        self.enemy_battler.dead = False
        self.enemy_battler.status = "idle"
        self.enemy_battler.direction = "left"
        self.enemy_battler.hp = self.enemy_battler.max_hp

        # Menu principal
        self.menu_items = ["Lutar", "Bolsa", "Fugir"]
        self.menu_index = 0

        # Submenu de golpes
        self.ui_mode = "main"
        self.fight_index = 0

        # Mensagens
        self.message_queue = []
        self.in_message = False

        # Controle de saída
        self.request_exit = False
        self.battle_over = False

        # Tremor (shake) quando toma hit
        self.player_hit_timer = 0
        self.enemy_hit_timer = 0
        self.shake_strength = 4   # pixels

        self.pending_enemy_attack = False

        # Posição do hud de entidade (boss mockado)
        if player.map == "death":
            self.hudBar = (92,105)
        else:
            self.hudBar = (92,75)
        self.enemyHudBar = (370,75)

    def _push_msg(self, text: str):
        self.message_queue.append(text)
        self.in_message = True

    def _next_msg(self):
        if self.message_queue:
            self.message_queue.pop(0)
            if player.status != "death":
                player.status = "idle"
        if not self.message_queue:
            self.in_message = False
        #contra ataque agendado
        if not self.message_queue and self.pending_enemy_attack and not self.battle_over:
            self.pending_enemy_attack = False
            move_name, dmg, hit = self.enemy_battler.use_random_move(self.player_battler)
            self._push_msg(f"{self.enemy_battler.name} usou {move_name}!")
            if hit:
                player.status = "hit"
                self._push_msg(f"Causou {dmg} de dano!")
                self.player_hit_timer = 10
            else:
                self._push_msg("Mas errou!")

                self.player_hit_timer = 10

            if self.player_battler.hp <= 0:
                player.status = "death"
                player.reset_sprite()
                self._push_msg("DERROTA...")
                self.player_battler.dead = True
                self.dead = True
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

    def _draw_text(self, screen, text, x, y, big=False):
        surf = (self.font_big if big else self.font).render(text, True, (255, 255, 255))
        context.screen.blit(surf, (x, y))

    def _draw_hp_box(self, screen, x, y, name, level, battler, box_w=240, box_h=64):
        box = pygame.Rect(x, y, box_w, box_h)

        self._draw_text(screen, f"{name}", x + 2, y - 25, big=True)
        if battler.name == "Heroi":
            self._draw_text(screen, f"Lv {level}", x + 45, y - 25)

        bar_x = x + 10
        bar_y = y + 32
        bar_w = 132
        bar_h = 9

        pygame.draw.rect(screen, (0, 0, 0), (x, y, bar_w, bar_h))

        ratio = self._hp_ratio(battler)
        fill_w = int(bar_w * ratio)

        color = (170, 0, 7)
        pygame.draw.rect(screen, color, (x, y, fill_w, bar_h))
        self._draw_text(screen, f"{battler.hp}/{battler.max_hp}", x + box_w - 140, y + 14)

    def _fight_items(self):
        move_names = [m.name for m in getattr(self.player_battler, "moves", [])]
        move_names = move_names[:4]
        return move_names + ["Voltar"]

    def handle_event(self):
        pass

    def handle_input(self, keys):
        up = self._edge("up", keys[pygame.K_w])
        down = self._edge("down", keys[pygame.K_s])
        enter = self._edge("enter", keys[pygame.K_RETURN])
        x = self._edge("x", keys[pygame.K_x])
        f2 = self._edge("f2", keys[pygame.K_F2])

        # AVALIAR: isso não deveria estar em um arquivo separado? keyActions deveria ser apenas os botões com chamadas de método
        if self.in_message:
            if enter:
                self._next_msg()
            return

        if self.battle_over:
            if enter:
                self.request_exit = True
                if player.dead:
                    self.switch_scene(SceneGameOver())
                else:
                    self.switch_scene(SceneWorld())
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

            if enter:
                choice = items[self.fight_index]

                if choice == "Voltar":
                    self.ui_mode = "main"
                    return

                move_index = self.fight_index
                move_name, damage, hit = self.player_battler.use_move(move_index, self.enemy_battler)

                self._push_msg(f"{self.player_battler.name} usou {move_name}!")

                if hit:
                    if move_name == "Corte rápido":
                        player.status = "pierce"
                    if move_name == "Fatiar":
                        player.status = "slice"
                    if move_name == "Foice da morte":
                        player.status = "slice2"
                    if move_name == "Investida":
                        player.status = "rush"
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

                    self.enemy_battler.status = "death"
                    self._push_msg("VITORIA!")
                    self.enemy_battler.dead = True
                    self.battle_over = True
                    self.ui_mode = "main"
                    return
                # agenda o contra-ataque
                self.pending_enemy_attack = True
                self.ui_mode = "main"
            return

        #Menu principal
        if up:
            self.menu_index = (self.menu_index - 1) % len(self.menu_items)
        if down:
            self.menu_index = (self.menu_index + 1) % len(self.menu_items)
        if f2:
            self.player_battler.take_xp(1000)
        if enter:
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
                self.ui_mode = "main"

    def render(self):
        context.screen.blit(self.background_image, (0, 0))
        # Sprites
        enemy_x = self.screen_w - 230
        enemy_y = 120
        dx, dy = self._shake_offset(self.enemy_hit_timer)

        enemy_frame = self.enemy_battler.get_sprite().convert_alpha()

        if player.map == "death":
            pass
        else:
            if self.enemy_battler.status == "death":
                enemy_sprite = pygame.transform.scale(enemy_frame, (192, 192))
                context.screen.blit(enemy_sprite, (enemy_x - 42, enemy_y - 80))
            else:
                enemy_sprite = pygame.transform.scale(enemy_frame, (96,96))
                context.screen.blit(enemy_sprite, (enemy_x + dx, enemy_y + dy))

        if player.map == "death":
            player_y = 150
        else:
            player_y = 120
        player_x = 130

        dx, dy = self._shake_offset(self.player_hit_timer)
        player_frame = player.get_sprite().convert_alpha()

        if player.status == "death" or player.status == "pierce" or player.status == "hit" or player.status == "slice" or player.status == "slice2" or player.status == "rush":
            player_frame = pygame.transform.scale(player_frame, (192, 192))
            context.screen.blit(player_frame, (player_x - 42, player_y - 50))
        else:
            player_frame = pygame.transform.scale(player_frame, (96, 96))
            context.screen.blit(player_frame, (player_x + dx, player_y + dy))

        if self.enemy_hit_timer > 0:
            self.enemy_hit_timer -= 1
        if self.player_hit_timer > 0:
            self.player_hit_timer -= 1

        # HUD inimigo
        if player.map != "death":
            self._draw_hp_box(
                context.screen,
                x=self.enemyHudBar[0] + 19,
                y=self.enemyHudBar[1] + 12,
                name=self.enemy_battler.name,
                level=3,
                battler=self.enemy_battler,
                box_w=240,
                box_h=64
            )

        # HUD player
        self._draw_hp_box(
            context.screen,
            x=self.hudBar[0] + 19,
            y=self.hudBar[1] + 12,
            name=self.player_battler.name,
            level=self.player_battler.level,
            battler=self.player_battler,
            box_w=240,
            box_h=64
        )

        context.screen.blit(self.life_hud_img, self.hudBar)

        if player.map == "death":
            pass
        else:
            context.screen.blit(self.life_hud_img_inverted, self.enemyHudBar)

        # Renderizar XP
        if player.map == "death":
            xpY = 57
        else:
            xpY = 26
        self._draw_text(
            context.screen,
            f"XP: {self.player_battler.xp}/100",
            x=self.enemyHudBar[0] - 260,
            y=self.enemyHudBar[1] + xpY,
        )

        # Renderizar mensagens e menus
        if self.in_message and self.message_queue:
            msg = self.message_queue[0]
            self._draw_text(context.screen, msg, 18, self.screen_h - 80, big=True)
            self._draw_text(context.screen, "ENTER: continuar", self.screen_w - 110, self.screen_h - 28)

        elif self.battle_over:

            self._draw_text(context.screen, "ENTER: voltar", self.screen_w - 95, self.screen_h - 28)
        else:
            start_x = self.screen_w - 240
            start_y = self.screen_h - 86

            if self.ui_mode == "main":
                # Menu principal
                for i, item in enumerate(self.menu_items):
                    y = start_y + i * 22
                    prefix = "> " if i == self.menu_index else "  "
                    self._draw_text(context.screen, prefix + item, start_x + 50, y, big=True)

            elif self.ui_mode == "fight":
                # Submenu de golpes
                items = self._fight_items()
                for i, item in enumerate(items):
                    y = start_y + i * 22
                    prefix = "> " if i == self.fight_index else "  "
                    self._draw_text(context.screen, prefix + item, start_x + 10, y, big=True)

class SceneGameOver(Scene):

    def render(self):

        # Fundo preto
        context.screen.fill((0, 0, 0))

        # Game over na tela
        game_over = self.font.render("GAME OVER", True, (255, 255, 255))
        rect = game_over.get_rect(
            center=(context.screen.get_width() / 2, context.screen.get_height() / 2)
        )
        context.screen.blit(game_over, rect)

        pygame.display.update()

        # Resetar player
        player.hp = player.max_hp
        player.reset_status()
        player.reset_sprite()

        # Respawn
        player.map = "spawn"
        player.position = pygame.Vector2(140,260)
        player.dead = False

        pygame.time.wait(3000)
        self.switch_scene(SceneWorld())

    def handle_input(self, keys):
        pass

    def handle_event(self):
        pass

    def __str__(self):
        return self.id


class SceneMainMenu(Scene):

    def __init__(self):
        super().__init__()
        self.selected = 0

    def render_text(self, text, center, position):
        surface = self.font.render(text, True, (255, 255, 255))
        position_center = (0,0)
        if center:
            position_center = (context.screen.get_width() / 2, context.screen.get_height() / 2)

            rect = surface.get_rect(
                center=(position_center[0] + position[0], position_center[1] + position[1])
            )
            context.screen.blit(surface, rect)
        else:
            context.screen.blit(surface, position)

    def render(self):

        # Fundo preto
        context.screen.fill((0, 0, 0))
        self.render_text("Trono de ossos", True, (0,-35))
        self.render_text("Escolha seu save", True, (0,-25))
        self.render_text("Aperte SPACE para começar", True, (0,45))

        self.render_text("Aperte z para excluir o save", True, (0,135))

        # Lista de saves
        for index in range(3):
            prefix = "- " if index == self.selected else ""
            self.render_text(f"{prefix}Save slot 0{index+1} - {Save.save_list[index]}", True, (0, -5 + 10 * (index+1)))
        pygame.display.update()

    def handle_input(self, keys):

        if self._edge("down", keys[pygame.K_s]):
            self.selected = (self.selected + 1) % 3

        if self._edge("up", keys[pygame.K_w]):
            self.selected = (self.selected - 1) % 3

        if self._edge("space", keys[pygame.K_SPACE]):
            self.load_save()

        if self._edge("z", keys[pygame.K_z]):
            self.delete_save()

    def handle_event(self):
        pass

    def load_save(self):
        Save.select_save(self.selected)
        Save.load()
        self.switch_scene(SceneWorld())

    def delete_save(self):
        Save.delete_save(self.selected)
        Save.load_saves()

    def __str__(self):
        return self.id
