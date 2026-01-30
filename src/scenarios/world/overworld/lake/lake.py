from src.scenarios.scenario import ScenarioOpenWorld
from src.utils.paths import WORLD_ASSETS

from src.entities.enemy.enemies import Enemy

background_path = WORLD_ASSETS / "lake/background.png"
top_layer_path = WORLD_ASSETS / "lake/toplayer.png"
spawn_position = (36, 76)

eventTiles = [
    [
        (0,0)
    ]
]

entities = []
nonPassableTiles = []

Lake = ScenarioOpenWorld("lake", background_path, nonPassableTiles, top_layer_path, spawn_position, eventTiles, entities)
