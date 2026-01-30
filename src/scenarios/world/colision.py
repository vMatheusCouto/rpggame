from src.entities.cordinates import getTilePos
from src.props import props
from src.utils.paths import SRC_DIR
import os
import json

worldsFolder = SRC_DIR / "scenarios/world/overworld/maps/"
def canWalk(mapName):
    with open(worldsFolder / f"{mapName}.json", "r") as file:
        data = json.load(file)
    x, y = getTilePos(props.player_pos)
    tile_key = f"{x},{y}"
    tile = data["tiles"].get(tile_key)
    if tile is None:
        return True

def entityColision(playerPos, entityPos):
    x = 40
    y = 35
    if playerPos.x >= entityPos[0] - x:
        if playerPos.x <= entityPos[0] + x:
            if playerPos.y >= entityPos[1] - y:
                if playerPos.y <= entityPos[1] + y:
                    return True
    """ if playerPos.x >= entityPos[0] - 19:
        if playerPos.x <= entityPos[0] + 19:
            if playerPos.y >= entityPos[1] - 25:
                if playerPos.y <= entityPos[1] + 9:
                    return True """
    return False
