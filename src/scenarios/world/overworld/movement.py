from src.props import props
from src.scenarios.world.colision import canWalk
dt = props.getDT()

def walk():
    props.setMoving(True)
    props.setStatus("walking")

def stopped(direction):
    props.setMoving(False)
    props.setStatus("walking")
    props.setDirection(direction)

def walkUp(blockedTiles):
    walk()
    props.player_pos.y -= props.getSpeed() * props.getDT()
    props.setDirection("up")
    if not canWalk(blockedTiles):
        walkDown(blockedTiles)
        stopped("up")

def walkDown(blockedTiles):
    walk()
    props.player_pos.y += props.getSpeed() * props.getDT()
    props.setDirection("down")
    if not canWalk(blockedTiles):
        walkUp(blockedTiles)
        stopped("down")

def walkRight(blockedTiles):
    walk()
    props.player_pos.x += props.getSpeed() * props.getDT()
    props.setDirection("right")
    if not canWalk(blockedTiles):
        walkLeft(blockedTiles)
        stopped("right")

def walkLeft(blockedTiles):
    walk()
    props.player_pos.x -= props.getSpeed() * props.getDT()
    props.setDirection("left")
    if not canWalk(blockedTiles):
        walkRight(blockedTiles)
        stopped("left")

