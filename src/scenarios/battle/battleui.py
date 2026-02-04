import pygame
from src.utils.paths import BATTLE_ASSETS, ASSETS_DIR
from src.context import context

class BattleUI:
    def __init__(self, logic):
        self.logic = logic

        # Fontes
        self.font = pygame.font.Font(ASSETS_DIR / "Pixeled.ttf", 5)
        self.font_big = pygame.font.Font(ASSETS_DIR / "Pixellari.ttf", 16)

        # Imagens
        current_map = self.logic.player.map
        self.background_image = pygame.image.load(BATTLE_ASSETS / f"{current_map}/background.png")
        self.life_hud_img = pygame.image.load(BATTLE_ASSETS / "life_hud.png").convert_alpha()
        self.life_hud_boss_img = pygame.image.load(BATTLE_ASSETS / "life_hud_boss.png").convert_alpha()

        # Timers visuais (Shake)
        self.shake_timer_player = 0
        self.shake_timer_enemy = 0
        self.shake_strength = 4

        # Menu State
        self.menu_mode = "main" # main, fight
        self.menu_index = 0
        self.fight_index = 0
        self.menu_items = ["Lutar", "Bolsa", "Fugir"]

        # Layout positions
        self.screen_w = context.screen.get_width()
        self.screen_h = context.screen.get_height()

        if current_map == "death":
            self.hud_pos_player = (92, 105)
            self.hud_pos_enemy = (370, 75) # Mock boss
        else:
            self.hud_pos_player = (92, 75)
            self.hud_pos_enemy = (370, 75)

    def trigger_shake(self, target):
        if target == "player": self.shake_timer_player = 10
        if target == "enemy": self.shake_timer_enemy = 10

    def navigate(self, direction):
        # Movimenta cursor nos menus
        if self.menu_mode == "main":
            self.menu_index = (self.menu_index + direction) % len(self.menu_items)
        elif self.menu_mode == "fight":
            moves_count = len(self.logic.player.moves) + 1 # +1 para "Voltar"
            self.fight_index = (self.fight_index + direction) % moves_count

    def get_selection(self):
        # Retorna o que foi selecionado
        if self.menu_mode == "main":
            return self.menu_items[self.menu_index]
        elif self.menu_mode == "fight":
            # Retorna indice do golpe ou "Voltar"
            moves = self.logic.player.moves
            if self.fight_index < len(moves):
                return self.fight_index
            return "Voltar"

    def enter_fight_menu(self):
        self.menu_mode = "fight"
        self.fight_index = 0

    def enter_main_menu(self):
        self.menu_mode = "main"

    def draw(self):
        screen = context.screen
        screen.blit(self.background_image, (0, 0))

        # 1. Sprites com Shake
        self._draw_entity(screen, self.logic.enemy, is_player=False)
        self._draw_entity(screen, self.logic.player, is_player=True)

        # 2. HUDs
        self._draw_hud(screen, self.logic.player, self.hud_pos_player)
        if self.logic.player.map != "death":
            self._draw_hud(screen, self.logic.enemy, self.hud_pos_enemy)
        else:
            self._draw_hud(screen, self.logic.enemy, (25, 35))
        # 3. Interface (Menus ou Mensagens)
        if self.logic.has_messages():
            self._draw_message_box(screen)
        elif self.logic.turn in ["victory", "defeat", "runaway"]:
            self._draw_text(screen, "ENTER: sair", self.screen_w - 95, self.screen_h - 28)
        else:
            self._draw_menus(screen)

        # Decrementa timers visuais
        if self.shake_timer_player > 0: self.shake_timer_player -= 1
        if self.shake_timer_enemy > 0: self.shake_timer_enemy -= 1

    def _draw_entity(self, screen, entity, is_player):
        sprite = entity.get_sprite().convert_alpha()

        # Lógica de escala e posição
        scale = 192 if entity.status in ["death", "pierce", "hit", "slice", "slice2", "rush"] else 96
        sprite = pygame.transform.scale(sprite, (scale, scale))

        # Shake
        timer = self.shake_timer_player if is_player else self.shake_timer_enemy
        dx = self.shake_strength if (timer % 2 == 0 and timer > 0) else -self.shake_strength if timer > 0 else 0

        # Posições fixas
        x = 130 if is_player else self.screen_w - 230
        y = (150 if self.logic.player.map == "death" else 120) if is_player else 120

        if scale == 192:
            x -= 42
            y -= (50 if is_player else 80)

        screen.blit(sprite, (x + dx, y))

    def _draw_hud(self, screen, entity, pos):
        # Desenha a barra preta/vermelha e o overlay
        x, y = pos[0] + 19, pos[1] + 12
        ratio = max(0, min(1, entity.hp / entity.max_hp))

        if entity.name == "Titã colossal":
            pygame.draw.rect(screen, (0, 0, 0), (x, y, 250, 9))
            pygame.draw.rect(screen, (170, 0, 7), (x, y, int(250 * ratio), 9))
            screen.blit(self.life_hud_boss_img, pos)
            self._draw_text(screen, f"{entity.hp}/{entity.max_hp}", x + 210, y + 14)

        else:
            pygame.draw.rect(screen, (0, 0, 0), (x, y, 132, 9))
            pygame.draw.rect(screen, (170, 0, 7), (x, y, int(132 * ratio), 9))
            screen.blit(self.life_hud_img, pos)
            self._draw_text(screen, f"{entity.hp}/{entity.max_hp}", x + 100, y + 14)

        # Textos
        self._draw_text(screen, entity.name, x + 2, y - 25, big=True)

        if entity == self.logic.player:
             self._draw_text(screen, f"Lv {entity.level}", x + 45, y - 25)
             xp_y = 57 if entity.map == "death" else 26
             self._draw_text(screen, f"XP: {entity.xp}/{entity.xp_to_next()}", 370 - 260, 75 + xp_y)

    def _draw_menus(self, screen):
        start_x = self.screen_w - 240
        start_y = self.screen_h - 86

        items = []
        details = False
        current_idx = 0

        if self.menu_mode == "main":
            items = self.menu_items
            current_idx = self.menu_index
        else:
            items = [m.name for m in self.logic.player.moves] + ["Voltar"]
            details = [[f"Acerto {m.accuracy * 100}%", f"Dano base {m.bonus}"] for m in self.logic.player.moves]
            details.append(["", ""])
            current_idx = self.fight_index
        for i, item in enumerate(items):
            prefix = "> " if i == current_idx else "  "
            if details and i == current_idx:
                self._draw_text(screen, details[i][0], start_x - 200, start_y, big=True)
                self._draw_text(screen, details[i][1], start_x - 200, start_y + 15, big=True)
            self._draw_text(screen, prefix + item, start_x + 50, start_y + i * 15, big=True)


    def _draw_message_box(self, screen):
        msg = self.logic.message_queue[0]
        self._draw_text(screen, msg, 18, self.screen_h - 80, big=True)
        self._draw_text(screen, "ENTER: continuar", self.screen_w - 110, self.screen_h - 28)

    def _draw_text(self, screen, text, x, y, big=False):
        surf = (self.font_big if big else self.font).render(str(text), True, (255, 255, 255))
        screen.blit(surf, (x, y))
