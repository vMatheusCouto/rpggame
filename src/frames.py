import pygame
import random

from src.entities.character import Enemy
from src.scenarios.world.map import Map
from src.scenarios.scene import SceneWorld, SceneBattle, SceneMainMenu
from src.scenarios.world.movement import *
from src.context import context

class Frames:
    def __init__(self):
        self.__current_scene = SceneMainMenu()

    def current_frame(self, keys):

        # Gerencia ações da cena e a renderiza em seguida
        self.__current_scene.handle_input(keys)
        self.__current_scene.handle_event()
        self.__current_scene.render()

        # Realiza a troca de cena
        if context.add_scene != self.__current_scene and context.add_scene != None:
            self.current_scene = context.add_scene
            self.current_frame(keys)

        pygame.display.update()

    @property
    def current_scene(self):
        return self.__current_scene

    @current_scene.setter
    def current_scene(self, scene):
        self.__current_scene = scene
        pygame.display.update()
