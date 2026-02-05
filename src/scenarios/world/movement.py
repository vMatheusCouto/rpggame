from src.entities.character import player
from src.context import context
class Walk():

    def walk(self):
        player.moving = True
        player.status = "walking"

    def stopped(self, direction):
        player.moving = False
        player.status = "idle"
        player.direction = direction

    def up(self):
        self.walk()
        player.position.y -= player.speed * context.delta
        player.direction = "up"

    def down(self):
        self.walk()
        player.position.y += player.speed * context.delta
        player.direction = "down"

    def right(self):
        self.walk()
        player.position.x += player.speed * context.delta
        player.direction = "right"

    def left(self):
        self.walk()
        player.position.x -= player.speed * context.delta
        player.direction = "left"
