import random
import pygame
import json
import os

from abc import ABC, abstractmethod
from src.scenarios.world.movement import *
from src.entities.character import player, Enemy
from src.utils.paths import BATTLE_ASSETS, CHARACTER_ASSETS, ASSETS_DIR, SOUNDS_DIR
from src.context import context
from src.entities.sprites import entity_sprites
from src.scenarios.world.map import Map
from src.scenarios.world.movement import Walk
from src.entities.collision import entity_collision
from src.scenarios.battle.battle import BattleLogic
from src.scenarios.battle.battleui import BattleUI
from src.entities.inventory.inventory import Inventory
from src.scenarios.dialog import DialogMixin
from src.scenarios.text import TextMixin
from src.save import Save

class Scene(ABC):

    def __init__(self):
        self.id = random.randint(100000, 999999)

        # Debounce
        self._pressed = {"up": False, "down": False, "enter": False, "x": False, "F2": False, "space": False, "escape": False, "F3": False, "i": False}

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

class SceneWorld(Scene, DialogMixin, TextMixin):

    def __init__(self):
        super().__init__()
        self.inventory_index = 0
        context.add_music = SOUNDS_DIR / "world.mp3"

        # Estado da cena
        self.__active = False
        self.map = Map.get_map_by_name(player.map)
        self.enemy = None

        self.walk = Walk()

        # Elementos da tela
        self.coordinates = False
        self.message_queue = []

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
            text_surface = context.font_small.render(
                f"x = {int(player.position.x)} ({int(tileX)}) z = {int(player.position.y)} ({int(tileY)})",
                True, (255, 255, 255)
            )
            context.screen.blit(text_surface, (10, 10))

        # messagess
        if self.has_messages():
            context.screen.blit(pygame.image.load(ASSETS_DIR / "world/dialog_box.png"), (0, 0))
            self.render_text(self.message_queue[0], False, (30, 330), "medium", (0,0,0))
            self.render_text(self.message_queue[1], False, (30, 340), "medium", (0,0,0))
            self.render_text(self.message_queue[2], False, (30, 350), "medium", (0,0,0))

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

        if self.has_messages():
            return

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

        enter = self._edge("enter", keys[pygame.K_RETURN])
        if self.has_messages():
            if enter:
                self.next_message()
                self.next_message()
                self.next_message()
                if not self.has_messages():
                    self.switch_scene(SceneBattle(self.enemy))
            return

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
        for message in enemy.dialog:
            self.add_message(message)
            self.enemy = enemy

        if not self.has_messages():
            self.switch_scene(SceneBattle(enemy))

class SceneBattle(Scene):
    def __init__(self,enemy_battler):
        super().__init__()
        context.add_music = SOUNDS_DIR / "battle.wav"

        player.direction = "right"
        player.status = "idle" # Reseta animação para evitar bugs visuais
        # Define que o Inimigo olha para a Esquerda
        enemy_battler.direction = "left"
        enemy_battler.status = "idle"
        # Inicializa Lógica e UI separadamente
        self.logic = BattleLogic(player, enemy_battler)
        self.ui = BattleUI(self.logic)

        self.show_inventory = False
        self.inventory_index = 0
    def render(self):
        # desenho feito na UI
        self.ui.draw()

    def handle_input(self, keys):
        # Leitura dos Inputs básicos com debounce
        up = self._edge("up", keys[pygame.K_w])
        down = self._edge("down", keys[pygame.K_s])
        enter = self._edge("enter", keys[pygame.K_RETURN])
        f2 = self._edge("f2", keys[pygame.K_F2])

        # 1. Se houver mensagens na tela, ENTER avança mensagem
        if self.logic.has_messages():
            if enter:
                self.logic.next_message()
                self.logic.next_message_battle()
            return

        # 2. Se a batalha acabou, ENTER sai da cena
        if self.logic.turn in ["victory", "defeat", "runaway"]:
            if enter:
                if self.logic.turn == "defeat":
                    self.switch_scene(SceneGameOver())

                    context.add_music = "stop"
                    context.add_sound_effect = SOUNDS_DIR / "over.mp3"
                else:
                    context.add_sound_effect = SOUNDS_DIR / "battle_end.wav"
                    context.add_music = SOUNDS_DIR / "world.mp3"
                    if self.logic.turn == "victory" and self.logic.enemy.name == "Titã colossal":
                        self.switch_scene(SceneDialog())
                    else:
                        self.switch_scene(SceneWorld())
            return

        # 3. Navegação do Menu
        if up:
            self.ui.navigate(-1)
        if down:
            self.ui.navigate(1)

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
            self.ui.enter_bag_menu()
        elif selection == "Fugir":
            self.logic.run_away()
        elif selection == "Voltar":
            self.ui.enter_main_menu()
        # Seleção de Golpe (retornou um int)
        elif isinstance(selection, int):
            if self.ui.menu_mode == "fight":
                hit_type, is_over = self.logic.player_attack(selection)
                # Feedback Visual na UI baseado no resultado da Lógica
                if hit_type == "hit":
                    context.add_sound_effect = SOUNDS_DIR / "hit.mp3"
                self.ui.trigger_shake("enemy")
            elif self.ui.menu_mode == "bag":
                self.logic.player_use_item(selection)
            self.ui.enter_main_menu() # Reseta para menu principal após atacar

    def handle_event(self):
        pass

class SceneGameOver(Scene):

    def render(self):

        # Fundo preto
        context.screen.fill((0, 0, 0))

        # Game over na tela
        game_over = context.font_small.render("GAME OVER", True, (255, 255, 255))
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

        pygame.time.wait(5000)
        self.switch_scene(SceneWorld())

    def handle_input(self, keys):
        pass

    def handle_event(self):
        pass

    def __str__(self):
        return self.id


class SceneMainMenu(Scene, TextMixin):

    def __init__(self):
        super().__init__()
        self.selected = 0
        Save.load_saves()

    def render(self):

        # Fundo preto
        context.screen.fill((0, 0, 0))

        self.render_text("Trono de ossos", True, (0,-35), "medium")
        self.render_text("Escolha seu save", True, (0,-25), "medium")
        self.render_text("Aperte SPACE para começar", True, (0,45), "medium")

        self.render_text("Aperte z para excluir o save", True, (0,135), "medium")

        # Lista de saves
        for index in range(3):
            prefix = "- " if index == self.selected else ""
            self.render_text(f"{prefix}Save slot 0{index+1} - {Save.save_list[index]}", True, (0, -5 + 10 * (index+1)), "medium")
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
        selected_status = Save.select_save(self.selected)
        Save.load()
        if selected_status == "new":
            self.switch_scene(SceneDialog())
        else:
            self.switch_scene(SceneWorld())
            context.add_sound_effect = SOUNDS_DIR / "start_end.wav"
        player._learn_moves_for_current_level()

    def delete_save(self):
        Save.delete_save(self.selected)
        Save.load_saves()

    def __str__(self):
        return self.id

class SceneDialog(Scene, DialogMixin, TextMixin):
    def __init__(self):
        super().__init__()
        if Enemy.enemy_list["Titã colossal"].dead:
            self.message_queue = [
                "",
                "",
                "",
                "Com a queda do Tita Colossal, a terra treme e o silencio retorna.",
                "A corrupcao que sufocava a floresta e as cavernas comeca a se dissipar.",
                "O peso que dominava este mundo finalmente se rompe.",
                "As criaturas restantes caem ou fogem, livres da vontade imposta.",
                "A floresta respira novamente, mesmo marcada pelas cicatrizes.",
                "O mundo nao esta salvo, mas ganhou mais uma chance.",
                "",
                "Fim de jogo. Voce venceu!",
                "",
            ]

        else:
            self.message_queue = [
                "Apos o colapso dos reinos, a Floresta Sombria tornou-se o ultimo refugio.",
                "Voce desperta entre arvores antigas, sem memorias e com uma sensacao de urgencia.",
                "Criaturas corrompidas rondam a floresta, marcadas por uma forca desconhecida.",
                "Antigos simbolos nas arvores indicam que algo terrivel despertou.",
                "Sussurros falam de um Tita Colossal que avanca consumindo tudo.",
                "A floresta nao e apenas o inicio, mas a ultima linha de defesa.",
                "Para impedir a ruina, voce deve atravessar terras esquecidas.",
                "Cada batalha o aproxima da verdade por tras da destruicao.",
                "No centro do caos, o Tita Colossal guarda o destino do mundo."
            ]

    def render(self):
        context.screen.fill((0, 0, 0))
        if self.has_messages():
            self.render_text(self.message_queue[0], True, (0,-10), "medium")
            self.render_text(self.message_queue[1], True, (0,0), "medium")
            self.render_text(self.message_queue[2], True, (0,10), "medium")

    def handle_event(self):
        pass

    def handle_input(self, keys):
        enter = self._edge("enter", keys[pygame.K_RETURN])

        # Se houver mensagens na tela, ENTER avança mensagem
        if self.has_messages():
            if enter:
                self.next_message()
                self.next_message()
                self.next_message()
            return
        self.switch_scene(SceneWorld())
        context.add_sound_effect = SOUNDS_DIR / "start_end.wav"
