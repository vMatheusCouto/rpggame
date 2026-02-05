import pygame
from src.utils.paths import ASSETS_DIR

class Context:
    def __init__(self):
        self.__screen = None
        self.__clock = clock = pygame.time.Clock()
        self.__running = True
        self.delta = 0

        pygame.font.init()
        self.font_small = pygame.font.Font(ASSETS_DIR / "Pixeled.ttf", 5)
        self.font_medium = pygame.font.Font(ASSETS_DIR / "dogicapixel.ttf", 8)
        self.font_large = pygame.font.Font(ASSETS_DIR / "Pixellari.ttf", 16)

        self.__add_scene = None

        GAME_RESOLUTION = (640, 384)
        self.__screen = pygame.display.set_mode(
            GAME_RESOLUTION, pygame.FULLSCREEN | pygame.SCALED
        )

    @property
    def screen(self):
        return self.__screen

    @property
    def running(self):
        return self.__running

    def stop_running(self):
        self.__running = False

    @property
    def clock(self):
        return self.__clock

    @property
    def add_scene(self):
        return self.__add_scene

    @add_scene.setter
    def add_scene(self, add_scene):
        self.__add_scene = add_scene

context = Context()
