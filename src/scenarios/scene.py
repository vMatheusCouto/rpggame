import pygame
import random

from abc import ABC, abstractmethod
from src.scenarios.world.movement import *
from src.entities.character import player, Enemy
from src.utils.paths import BATTLE_ASSETS, CHARACTER_ASSETS, ASSETS_DIR
from src.context import context
from src.entities.sprites import entity_sprites
from src.scenarios.world.map import Map
from src.scenarios.world.movement import Walk
from src.entities.collision import entity_collision

class Scene(ABC):

    def __init__(self):
        self.id = rand.randint(100000, 999999)

    def start():
        pass

    def __end():
        pass

    def switch_scene(self, scene):
        context.add_scene = scene

    @classmethod
    def render():
        pass

    @abstractmethod
    def handle_input():
        pass

    def __str__(self):
        return self.id

class SceneWorld(Scene):

    def __init__(self):

        # Estado da cena
        self.__active = False
        self.map = Map.get_map_by_name(player.map)

        self.walk = Walk()

        # Elementos da tela
        self.coordinates = False

        player.position.x = self.map.spawn_position[0]
        player.position.y = self.map.spawn_position[1]

        self.start()

    def render(self):
        if self.__active:
            # Renderiza o background
            print("mapbg:",self.map.background)
            context.screen.blit(self.map.background, (0, 0))

            # Renderiza todos os inimigos do mapa atual
            for key, enemy in Enemy.enemy_list.items():
                print("enemy")
                print(enemy.map)
                print(self.map.name)
                if enemy.map == self.map.name:
                    if not enemy.dead:
                        print((enemy.position[0] - 16, enemy.position[1] - 24))
                        context.screen.blit(enemy.get_sprite(), (enemy.position[0] - 16, enemy.position[1] - 24))

            # Renderiza o player
            print(player.position.x)
            print(player.position.y)
            context.screen.blit(player.get_sprite(), (player.position.x - 16, player.position.y - 24))

            # Renderiza o top layer
            context.screen.blit(self.map.top_layer, (0, 0))

            # Renderiza as coordenadas
            if self.coordinates:
                (tileX, tileY) = player.tiles
                text_surface = font.render(
                    f"x = {int(player.position.x)} ({int(tileX)}) z = {int(player.position.y)} ({int(tileY)})",
                    True, (255, 255, 255)
                )

    def start(self):
        player.reset_status()
        self.map = self.map
        self.__active = True

    def switch_map(self, new_map, position):
        player.map = new_map.name
        new_scene = SceneWorld()
        context.add_scene = new_scene
        new_scene.start()
        player.position = pygame.Vector2(position[0], position[1])

    def switch_scene(self, scene):
        self.map.spawn_position = (player.position.x, player.position.y)
        super().switch_scene(scene)

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
                        self.switch_scene(SceneBattle(player, enemy, self.map.name))

        tile = self.map.get_tile_details(player.get_tile_pos())
        print(tile)
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
                        self.switch_scene(SceneBattle(player, Enemy.enemy_list["Orc"], self.map.name))
                    else:
                        self.switch_scene(SceneBattle(player, Enemy.enemy_list["Skeleton"], self.map.name))


    def handle_input(self, keys):
        event = None
        running = False
        player.speed = 35

        if keys[pygame.K_q]:
            context.stop_running()

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

        if running:
            player.status = "running"

    def start_battle(self, enemy):
        self.end()

class SceneBattle(Scene):
    def __init__(self, player_battle, enemy_battle, backgroundName):
        from src.context import context
        # Corrigir nomes, ordem e inicialização

        # Ideia: pegar tudo que desenha na tela e colocar em Scene ou em uma classe chamada Screen;
        self.life_hud_img = pygame.image.load(BATTLE_ASSETS / "life_hud.png").convert_alpha()
        self.life_hud_img_inverted = pygame.image.load(BATTLE_ASSETS / "life_hud.png").convert_alpha()
        self.background_image = pygame.image.load(BATTLE_ASSETS / f"{player.map}/background.png")
        if backgroundName == "death":
            self.hudBar = (92,105)
        else:
            self.hudBar = (92,75)
        self.enemyHudBar = (370,75)
        self.screen_w = context.screen.get_width()
        self.screen_h = context.screen.get_height()
        self.player_battler = player_battle
        self.enemy_battler = enemy_battle

        # Corrigir quando Player for refatorado
        self.backgroundName = backgroundName
        self.dead = False
        player.status = "idle"
        player.direction = "right"
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

        # Debounce das teclas
        self._pressed = {"up": False, "down": False, "z": False, "x": False}

        # Controle de saída
        self.request_exit = False
        self.battle_over = False
        # Tremor (shake) quando toma hit

        # CORRIGIR: só vai ser executado quando o golpe for acertado
        self.player_hit_timer = 0
        self.enemy_hit_timer = 0
        self.shake_strength = 4   # pixels
        self.pending_enemy_attack = False

        # Critérios visuais
        self.enemy_battler.dead = False
        self.enemy_battler.status = "idle"
        # Fonts
        pygame.font.init() # avaliar: tem como puxar esse init direto do context?
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
                player.reset_sprite(8)
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
        z = self._edge("z", keys[pygame.K_RETURN])
        x = self._edge("x", keys[pygame.K_x])
        f2 = self._edge("f2", keys[pygame.K_F2])

        # AVALIAR: isso não deveria estar em um arquivo separado? keyActions deveria ser apenas os botões com chamadas de método
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
                self.ui_mode = "main"

    def render(self):
        context.screen.blit(self.background_image, (0, 0))
        # Sprites
        enemy_x = self.screen_w - 230
        enemy_y = 120
        dx, dy = self._shake_offset(self.enemy_hit_timer)

        enemy_frame = self.enemy_battler.get_sprite().convert_alpha()

        if self.backgroundName == "death":
            pass
        else:
            if self.enemy_battler.getStatus() == "death":
                enemy_sprite = pygame.transform.scale(enemy_frame, (192, 192))
                context.screen.blit(enemy_sprite, (enemy_x - 42, enemy_y - 80))
            else:
                enemy_sprite = pygame.transform.scale(enemy_frame, (96,96))
                print("enemy_x:",enemy_x)
                print("enemy_y:",enemy_y)
                context.screen.blit(enemy_sprite, (enemy_x + dx, enemy_y + dy))

        if self.backgroundName == "death":
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
        if self.backgroundName != "death":
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

        if self.backgroundName == "death":
            pass
        else:
            context.screen.blit(self.life_hud_img_inverted, self.enemyHudBar)

        # Renderizar XP
        if self.backgroundName == "death":
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
            self.switch_scene(SceneWorld())
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

