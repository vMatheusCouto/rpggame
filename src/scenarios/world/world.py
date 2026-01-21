from src.scenarios.world.overworld.spawn.spawn import Spawn
from src.scenarios.world.overworld.cave.cave import Cave
from src.props import props
import pygame

class World:
    def __init__(self):
        self.current_map = Spawn
        self.player_pos = pygame.Vector2(props.getScreen().get_width() / 2, props.getScreen().get_height() / 2)

    def setMap(self, map):
        self.current_map = map

    def setMapByName(self, map):
        if map == "cave":
            self.setMap(Cave)
        elif map == "spawn":
            self.setMap(Spawn)
            print ("spawn")

world = World()
