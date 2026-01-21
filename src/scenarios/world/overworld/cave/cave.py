from src.scenarios.scenario import ScenarioOpenWorld
from src.utils.paths import WORLD_ASSETS

background_path = WORLD_ASSETS / "cave/background.png"
top_layer_path = WORLD_ASSETS / "spawn/toplayer.png"
nonPassableTiles = [
  (11, 8), (11,9), (11,10)
]
Cave = ScenarioOpenWorld(background_path, nonPassableTiles, top_layer_path)
