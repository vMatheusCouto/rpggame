import pygame
import random

from src.entities.character import Enemy
from src.scenarios.world.map import Map
from src.scenarios.scene import SceneWorld, SceneBattle
from src.scenarios.world.movement import *
from src.context import context

class Frames:
    def __init__(self):
        self.__current_scene = SceneWorld()

    def current_frame(self, keys):
        self.__current_scene.handle_input(keys)
        self.__current_scene.handle_event()
        self.__current_scene.render()
        if context.add_scene != self.__current_scene and context.add_scene != None:
            self.current_scene = context.add_scene
            self.current_frame(keys)
        self.update()

    def update(self):
        if player.respawn:
            player.position.x = Map.get_map_by_name(player.map).spawn_position[0]
            player.position.y = Map.get_map_by_name(player.map).spawn_position[1]
            player.respawn = False
        pygame.display.update()

    @property
    def current_scene(self):
        return self.__current_scene

    @current_scene.setter
    def current_scene(self, scene):
        self.__current_scene = scene
        self.update()
