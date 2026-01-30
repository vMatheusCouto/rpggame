from src.props import props
from src.scenarios.world.colision import canWalk
from src.scenarios.world.event import *
dt = props.getDT()

def walk():
    from src.scenarios.world.world import world
    props.setMoving(True)
    props.setStatus("walking")
    return world.current_map.name

def stopped(direction):
    props.setMoving(False)
    props.setStatus("walking")
    props.setDirection(direction)

def walkUp(eventTiles):
    mapName = walk()
    props.player_pos.y -= props.getSpeed() * props.getDT()
    props.setDirection("up")
    if not canWalk(mapName):
        walkDown(eventTiles)
        stopped("up")
    event = getEvent(eventTiles)
    return event


def walkDown(eventTiles):
    mapName = walk()
    props.player_pos.y += props.getSpeed() * props.getDT()
    props.setDirection("down")
    if not canWalk(mapName):
        walkUp(eventTiles)
        stopped("down")
    event = getEvent(eventTiles)
    return event

def walkRight(eventTiles):
    mapName = walk()
    props.player_pos.x += props.getSpeed() * props.getDT()
    props.setDirection("right")
    if not canWalk(mapName):
        walkLeft(eventTiles)
        stopped("right")
    event = getEvent(eventTiles)
    return event

def walkLeft(eventTiles):
    mapName = walk()
    props.player_pos.x -= props.getSpeed() * props.getDT()
    props.setDirection("left")
    if not canWalk(mapName):
        walkRight(eventTiles)
        stopped("left")
    event = getEvent(eventTiles)
    return event

