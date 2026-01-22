from src.scenarios.world.overworld.spawn.spawn import Spawn
from src.scenarios.world.overworld.cave.cave import Cave
from src.scenarios.world.overworld.village.village import Village
from src.props import props
import pygame

class World:
    def __init__(self):
        self.current_map = Spawn
        self.player_pos = pygame.Vector2(props.getScreen().get_width() / 2, props.getScreen().get_height() / 2)

    def setMap(self, map):
        self.current_map = map
        props.player_pos.x = map.spawn_position[0]
        props.player_pos.y = map.spawn_position[1]

    def setMapByName(self, map):
        if map == "cave":
            self.setMap(Cave)
        elif map == "spawn":
            self.setMap(Spawn)
        elif map == "village":
            self.setMap(Village)

world = World()
