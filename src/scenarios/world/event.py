from src.entities.cordinates import getTilePos
from src.props import props

def getEvent(eventTiles):
    targetTiles = getTilePos(props.player_pos)
    runEvent = False
    event = None
    for position in eventTiles:
        if event:
            break
        for tile in position[0]:
            if runEvent:
                break
            if targetTiles == tile:
                runEvent = True
        if runEvent:
            event = (position[1], position[2], position[3])
    return event
