from src.scenarios.world.overworld.spawn.spawn import Spawn
from src.scenarios.world.overworld.cave.cave import Cave
from src.scenarios.world.overworld.village.village import Village
from src.scenarios.world.overworld.death.death import Death
from src.scenarios.world.overworld.snow.snow import Snow
from src.scenarios.world.overworld.lake.lake import Lake
from src.props import props
import pygame

class World:
    def __init__(self):
        self.current_map = Spawn
        self.player_pos = pygame.Vector2(props.getScreen().get_width() / 2, props.getScreen().get_height() / 2)

    def getEntities(self):
        return self.current_map.entities

    def setMap(self, map):
        # Repensar na forma atual, o player deveria decidir o mundo que ele tá; World poderia ser apenas uma instanciação dos mapas com funções para fazer um get pelo nome e atributos dos mapas;

        # E se o mapa fosse carregado na hora? Ou seja, na hora que o player troca de mapa, uma nova instância é criada pela leitura do json;
        self.current_map = map
        props.player_pos.x = map.spawn_position[0]
        props.player_pos.y = map.spawn_position[1]

    def setMapByName(self, map):
        # Adicionar laço para encontrar mapa pelo nome
        if map == "cave":
            self.setMap(Cave)
        elif map == "spawn":
            self.setMap(Spawn)
        elif map == "village":
            self.setMap(Village)
        elif map == "lake":
            self.setMap(Lake)

world = World()
