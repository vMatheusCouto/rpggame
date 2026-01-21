from src.props import props
from src.scenarios.world.colision import canWalk
dt = props.getDT()

def walk():
    props.setMoving(True)
    props.setStatus("walking")

def walkUp(blockedTiles):
    walk()
    props.player_pos.y -= props.getSpeed() * props.getDT()
    props.setDirection("up")
    if not canWalk(blockedTiles):
        walkDown(blockedTiles)

def walkDown(blockedTiles):
    walk()
    props.player_pos.y += props.getSpeed() * props.getDT()
    props.setDirection("down")
    if not canWalk(blockedTiles):
        walkUp(blockedTiles)

def walkRight(blockedTiles):
    walk()
    props.player_pos.x += props.getSpeed() * props.getDT()
    props.setDirection("right")
    if not canWalk(blockedTiles):
        walkLeft(blockedTiles)

def walkLeft(blockedTiles):
    walk()
    props.player_pos.x -= props.getSpeed() * props.getDT()
    props.setDirection("left")
    if not canWalk(blockedTiles):
        walkRight(blockedTiles)

