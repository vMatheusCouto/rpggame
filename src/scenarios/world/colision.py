from src.entities.cordinates import getTilePos
from src.props import props

def canWalk(nonPassableTiles):
    targetTiles = getTilePos(props.player_pos)
    return not targetTiles in nonPassableTiles
