from src.scenarios.world.world import world
from src.props import props
from src.entities.player.sprites import sprite
import pygame

def currentFrameProps():
    return world.current_map.imagePath

def currentFrame(keys):
    props.setMoving(False)
    props.setStatus("idle")
    world.current_map.keyActions(keys)
    world.player_pos
    screen = props.getScreen()
    screen.blit(props.getBackground(), (0, 0))
    if keys[pygame.K_q]:
        props.stopRunning()
    screen.blit(sprite.getSprite(), props.getPlayerPos())
