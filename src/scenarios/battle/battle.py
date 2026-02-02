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

    def use_potion(self):
        if self.player.potions > 0:
            self.player.potions -= 1
            self.player.hp += 30
            self.add_message("Voce usou uma pocao! +30 HP")
            self.pending_enemy_attack = True
        else:
            self.add_message("Sem pocoes!")

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

        if self.player.level > lvl_before:
            self.add_message(f"SUBIU PARA O NIVEL {self.player.level}!")

        self.enemy.status = "death"
        self.enemy.dead = True
        self.add_message("VITORIA!")
        self.turn = "victory"

    def _get_move_animation(self, move_name):
        # Mapeia nome do golpe para animação
        if move_name == "Corte rápido": return "pierce"
        if move_name == "Fatiar": return "slice"
        if move_name == "Foice da morte": return "slice2"
        if move_name == "Investida": return "rush"
        return "idle"
