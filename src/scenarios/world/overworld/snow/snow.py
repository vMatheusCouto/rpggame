from src.scenarios.scenario import ScenarioOpenWorld
from src.utils.paths import WORLD_ASSETS

from src.entities.enemy.enemies import Enemy

background_path = WORLD_ASSETS / "snow/background.png"
top_layer_path = WORLD_ASSETS / "snow/toplayer.png"
spawn_position = (93, 248)

eventTiles = [
    [
        (0,0)
    ]
]

entities = []
nonPassableTiles = []

Snow = ScenarioOpenWorld("snow", background_path, nonPassableTiles, top_layer_path, spawn_position, eventTiles, entities)
