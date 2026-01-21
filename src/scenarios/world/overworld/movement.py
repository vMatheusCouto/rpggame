from src.props import props
from src.scenarios.world.colision import canWalk
from src.scenarios.world.event import *
dt = props.getDT()

def walk():
    props.setMoving(True)
    props.setStatus("walking")

def stopped(direction):
    props.setMoving(False)
    props.setStatus("walking")
    props.setDirection(direction)

def walkUp(blockedTiles, eventTiles):
    walk()
    props.player_pos.y -= props.getSpeed() * props.getDT()
    props.setDirection("up")
    if not canWalk(blockedTiles):
        walkDown(blockedTiles, eventTiles)
        stopped("up")
    event = getEvent(eventTiles)
    return event


def walkDown(blockedTiles, eventTiles):
    walk()
    props.player_pos.y += props.getSpeed() * props.getDT()
    props.setDirection("down")
    if not canWalk(blockedTiles):
        walkUp(blockedTiles, eventTiles)
        stopped("down")
    event = getEvent(eventTiles)
    return event

def walkRight(blockedTiles, eventTiles):
    walk()
    props.player_pos.x += props.getSpeed() * props.getDT()
    props.setDirection("right")
    if not canWalk(blockedTiles):
        walkLeft(blockedTiles, eventTiles)
        stopped("right")
    event = getEvent(eventTiles)
    return event

def walkLeft(blockedTiles, eventTiles):
    walk()
    props.player_pos.x -= props.getSpeed() * props.getDT()
    props.setDirection("left")
    if not canWalk(blockedTiles):
        walkRight(blockedTiles, eventTiles)
        stopped("left")
    event = getEvent(eventTiles)
    return event

