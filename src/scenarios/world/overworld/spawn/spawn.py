from src.scenarios.scenario import ScenarioOpenWorld
from src.utils.paths import WORLD_ASSETS

background_path = WORLD_ASSETS / "spawn/background.png"
nonPassableTiles = [[[8, 5],[13, 8]],[[3,3],[9,7]],[[0, 0],[4, 17]],[[5,12],[5,17]],[[5,14],[4,17]],[[5,15],[13,17]]]

Spawn = ScenarioOpenWorld(background_path, nonPassableTiles)
