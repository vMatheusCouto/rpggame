import random
from src.entities.character import player

class BattleLogic:
    def __init__(self, player_battler, enemy_battler):
        self.player = player_battler
        self.enemy = enemy_battler
        self.enemy.hp = self.enemy.max_hp  # Reset enemy HP
        self.enemy.dead = False

        # Estado
        self.turn = "player" # player, enemy, victory, defeat, runaway
        self.message_queue = []
        self.pending_enemy_attack = False

    def add_message(self, text):
        self.message_queue.append(text)

    def next_message(self):
        if self.message_queue:
            self.message_queue.pop(0)
            if player.status != "death":
                player.status = "idle"
            # Se acabou as mensagens e tinha um ataque inimigo pendente
            if not self.message_queue and self.pending_enemy_attack:
                self.pending_enemy_attack = False
                self.execute_enemy_turn()

    def has_messages(self):
        return len(self.message_queue) > 0

    def player_attack(self, move_index):
        move_name, damage, hit = self.player.use_move(move_index, self.enemy)

        self.add_message(f"{self.player.name} usou {move_name}!")
        if hit:
            # Retorna o status que o player deve assumir para a UI saber
            status_effect = self._get_move_animation(move_name)
            self.player.status = status_effect
            self.add_message(f"Causou {damage} de dano!")
            if self.enemy.hp <= 0:
                self._handle_victory()
                return "hit", True # hit type, is_over
            else:
                self.pending_enemy_attack = True
                return "hit", False
        else:
            self.add_message("Mas errou!")
            self.pending_enemy_attack = True
            return "miss", False

    def player_use_item(self, bag_index):
        item = self.player.inventory.list_items()[bag_index][0]
        self.player.inventory.use_item(item, self.player)

        if item.type == "cura":
            self.add_message(f"Usou {item.display_name}! Recuperou {item.heal_value} HP.")
        self.show_inventory = False
        self.turn = "enemy"
        self.pending_enemy_attack= True

    def run_away(self):
        self.add_message("Voce fugiu da batalha!")
        self.turn = "runaway"

    def execute_enemy_turn(self):
        move_name, dmg, hit = self.enemy.use_random_move(self.player)
        self.add_message(f"{self.enemy.name} usou {move_name}!")

        if hit:
            self.player.status = "hit"
            self.add_message(f"Causou {dmg} de dano!")
            if self.player.hp <= 0:
                self.player.status = "death"
                self.add_message("DERROTA...")
                self.player.dead = True
                self.turn = "defeat"
        else:
            self.add_message("Mas errou!")

    def _handle_victory(self):
        self.add_message("Inimigo derrotado!")
        xp = self.enemy.drop_xp
        lvl_before = self.player.level
        self.player.take_xp(xp)
        self.add_message(f"Voce ganhou {xp} XP!")
        drop_message = self.enemy.drop_random_item(self.player)
        if drop_message:
            self.add_message(drop_message)

        if self.player.level > lvl_before:
            self.add_message(f"SUBIU PARA O NIVEL {self.player.level}!")

        self.enemy.status = "death"
        self.enemy.dead = True
        self.add_message("VITORIA!")
        self.turn = "victory"

    def _get_move_animation(self, move_name):
        # Mapeia nome do golpe para animação
        if move_name == "Corte Rápido": return "pierce"
        if move_name == "Fatiar": return "slice"
        if move_name == "Foice da Morte": return "slice2"
        if move_name == "Investida": return "rush"
        return "idle"
