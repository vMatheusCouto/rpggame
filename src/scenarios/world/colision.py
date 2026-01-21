from src.entities.cordinates import getTilePos
from src.props import props

def canWalk(nonPassableTiles):
    targetTiles = getTilePos(props.player_pos)
    goBack = False
    for positions in nonPassableTiles:
        if goBack:
            break
        if targetTiles == positions:
            goBack = True
    return not goBack
