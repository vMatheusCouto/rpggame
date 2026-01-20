
from src.props import props
dt = props.getDT()

def walk():
    props.setMoving(True)
    props.setStatus("walking")

def walkUp():
    walk()
    props.player_pos.y -= props.getSpeed() * props.getDT()
    props.setDirection("up")

def walkDown():
    walk()
    props.player_pos.y += props.getSpeed() * props.getDT()
    props.setDirection("down")

def walkRight():
    walk()
    props.player_pos.x += props.getSpeed() * props.getDT()
    props.setDirection("right")

def walkLeft():
    walk()
    props.player_pos.x -= props.getSpeed() * props.getDT()
    props.setDirection("left")

