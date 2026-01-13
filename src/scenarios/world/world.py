from src.scenarios.world.overworld.movement import *
from src.scenarios.world.overworld.spawn.spawn import Spawn
from src.props import props
import pygame

class World:
    def __init__(self):
        self.current_map = Spawn
        self.player_pos = pygame.Vector2(props.getScreen().get_width() / 2, props.getScreen().get_height() / 2)

world = World()
