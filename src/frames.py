from src.scenarios.world.world import world
from src.props import props
from src.entities.player.sprites import sprite
from src.entities.cordinates import getTilePos
import pygame

def currentFrameProps():
    background_image = pygame.image.load(world.current_map.imagePath).convert()
    top_layer_image = pygame.image.load(world.current_map.topLayerPath).convert_alpha()
    props.setBackground(background_image)
    props.setTopLayer(top_layer_image)

pygame.font.init()
font = pygame.font.Font(None, 16) # None uses the default built-in font

def currentFrame(keys):
    props.setMoving(False)
    props.setStatus("idle")
    world.current_map.keyActions(keys, world.current_map.blockedTiles)
    screen = props.getScreen()

    if keys[pygame.K_q]:
        props.stopRunning()
    if keys[pygame.K_c]:
        currentFrameProps()
        world.setMapByName("cave")
    if keys[pygame.K_m]:
        currentFrameProps()
        world.setMapByName("spawn")

    screen.blit(props.getBackground(), (0, 0))

    (tileX, tileY) = getTilePos(props.getPlayerPos())
    text_surface = font.render(f"x = {props.getPlayerPos().x} ({tileX}) z = {props.getPlayerPos().y} ({tileY})", True, (255, 255, 255)) # White text

    text_rect = text_surface.get_rect()
    text_rect.center = (screen.get_width() / 2, screen.get_height() / 2) # Center the text on the screen

    screen.blit(text_surface, text_rect)
    screen.blit(sprite.getSprite(), (props.getPlayerPos().x - 16, props.getPlayerPos().y - 16))
    screen.blit(props.getTopLayer(), (0, 0))
