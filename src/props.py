import pygame

clock = pygame.time.Clock()

class Props:
    def __init__(self, screen, player_pos):
        self.screen = screen
        self.player_pos = player_pos
        self.background = None
        self.topLayer = None
        self.running = True
        self.speed = 40
        self.clock = clock
        self.dt = 0
        self.status = "idle"
        self.direction = "down"
        self.moving = False
        self.path = "player"

    def setDT(self, dt):
        self.dt = dt

    def getDT(self):
        return self.dt

    def setScreen(self, screen):
        self.screen = screen

    def getScreen(self):
        return self.screen

    def setPlayerPos(self, playerpos):
        self.player_pos = playerpos

    def getPlayerPos(self):
        return self.player_pos

    def setBackground(self, background):
        self.background = background

    def getBackground(self):
        return self.background

    def setTopLayer(self, topLayer):
        self.topLayer = topLayer

    def getTopLayer(self):
        return self.topLayer

    def getRunning(self):
        return self.running

    def stopRunning(self):
        self.running = False

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed

    def getClock(self):
        return self.clock

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def setDirection(self, direction):
        self.direction = direction

    def getDirection(self):
        return self.direction

    def setMoving(self, moving):
        self.moving = moving

    def getMoving(self):
        return self.moving

GAME_RESOLUTION = (640, 384)
screen = pygame.display.set_mode(
    GAME_RESOLUTION, pygame.FULLSCREEN | pygame.SCALED
)
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
props = Props(screen, player_pos)
