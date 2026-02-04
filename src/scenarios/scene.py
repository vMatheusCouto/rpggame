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
from src.scenarios.battle.battle import BattleLogic
from src.scenarios.battle.battleui import BattleUI

from src.save import Save

class Scene(ABC):

    def __init__(self):
        self.id = random.randint(100000, 999999)

        # Gerenciamento de fontes
        pygame.font.init()
        self.font = pygame.font.Font(ASSETS_DIR / "Pixeled.ttf", 5)
        self.font_big = pygame.font.Font(ASSETS_DIR / "Pixellari.ttf", 16)

        # Debounce
        self._pressed = {"up": False, "down": False, "enter": False, "x": False, "F2": False, "space": False, "escape": False}

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

        # Menu
        if self._edge("esc", keys[pygame.K_ESCAPE]):
            self.switch_scene(SceneMainMenu())

        # Redefinir velocidade
        player.speed = 35

        # Correr
        if keys[pygame.K_LSHIFT]:
            running = True
            player.speed = 60

        # Aumentar velocidade para a apresentação
        if keys[pygame.K_RSHIFT]:
            running = True
            player.speed = 180

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
        self.switch_scene(SceneBattle(enemy))

class SceneBattle(Scene):
    def __init__(self,enemy_battler):
        super().__init__()
        player.direction = "right"
        player.status = "idle" # Reseta animação para evitar bugs visuais
        # Define que o Inimigo olha para a Esquerda
        enemy_battler.direction = "left"
        enemy_battler.status = "idle"
        # Inicializa Lógica e UI separadamente
        self.logic = BattleLogic(player, enemy_battler)
        self.ui = BattleUI(self.logic)

    def render(self):
        # desenho feito na UI
        self.ui.draw()

    def handle_input(self, keys):
        # Leitura dos Inputs básicos com debounce
        up = self._edge("up", keys[pygame.K_w])
        down = self._edge("down", keys[pygame.K_s])
        enter = self._edge("enter", keys[pygame.K_RETURN])
        x_key = self._edge("x", keys[pygame.K_x])
        f2 = self._edge("f2", keys[pygame.K_F2])

        # 1. Se houver mensagens na tela, ENTER avança mensagem
        if self.logic.has_messages():
            if enter:
                self.logic.next_message()
            return

        # 2. Se a batalha acabou, ENTER sai da cena
        if self.logic.turn in ["victory", "defeat", "runaway"]:
            if enter:
                if self.logic.turn == "defeat":
                    self.switch_scene(SceneGameOver())
                else:
                    self.switch_scene(SceneWorld())
            return

        # 3. Navegação do Menu
        if up:
            self.ui.navigate(-1)
        if down:
            self.ui.navigate(1)

        # 4. Seleção e Voltar
        if x_key and self.ui.menu_mode == "fight":
            self.ui.enter_main_menu()
            return

        if enter:
            selection = self.ui.get_selection()
            self._process_selection(selection)
        if f2:
            player.take_xp(2000)

    def _process_selection(self, selection):
        # Processa o que foi escolhido no menu
        # Menu Principal
        if selection == "Lutar":
            self.ui.enter_fight_menu()
        elif selection == "Bolsa":
            self.logic.use_potion()
        elif selection == "Fugir":
            self.logic.run_away()
        elif selection == "Voltar":
            self.ui.enter_main_menu()
        # Seleção de Golpe (retornou um int)
        elif isinstance(selection, int):
            hit_type, is_over = self.logic.player_attack(selection)
            # Feedback Visual na UI baseado no resultado da Lógica
            if hit_type == "hit":
                self.ui.trigger_shake("enemy")
            self.ui.enter_main_menu() # Reseta para menu principal após atacar

    def handle_event(self):
        pass

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
        Save.load_saves()

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
        player._learn_moves_for_current_level()

    def delete_save(self):
        Save.delete_save(self.selected)
        Save.load_saves()

    def __str__(self):
        return self.id
