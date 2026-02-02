from src.utils.paths import SRC_DIR, WORLD_ASSETS
import os
import json
import pygame
class Map:
    map_list = {}

    def __init__(self, name, spawn_position, tiles, events):
        self.__name = name
        self.__background = pygame.image.load(WORLD_ASSETS / f"{name}/background.png")
        self.__top_layer = pygame.image.load(WORLD_ASSETS / f"{name}/toplayer.png").convert_alpha()
        self.__spawn_position = spawn_position
        self.__tiles = tiles
        self.__events = events

    @classmethod
    def load_maps(cls):
        maps_folder = SRC_DIR / "scenarios/world/maps"
        entries = os.listdir(maps_folder)
        for map in sorted(entries):
            with open(maps_folder / map, 'r') as file:
                data = json.load(file)
                print(file)
                current_map = Map(
                    name=data["name"],
                    spawn_position=data["spawn_position"],
                    tiles=data["tiles"],
                    events=data["events"]
                )
                cls.map_list[data["name"]] = current_map

    @classmethod
    def get_map_by_name(cls, new_map):
        return cls.map_list.get(new_map)

    @property
    def name(self):
        return self.__name

    @property
    def background(self):
        return self.__background

    @property
    def top_layer(self):
        return self.__top_layer

    @property
    def spawn_position(self):
        return self.__spawn_position

    @spawn_position.setter
    def spawn_position(self, new_position):
        self.__spawn_position = new_position

    @property
    def tiles(self):
        return self.__tiles

    @property
    def events(self):
        return self.__events

    def get_event_details(self, event):
        return self.__events.get(event)

    def get_tile_details(self, current_tile):
        x, y = current_tile
        return self.__tiles.get(f"{x},{y}")
