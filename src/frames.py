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
    props.player_pos.x = world.current_map.spawn_position[0]
    props.player_pos.y = world.current_map.spawn_position[1]

pygame.font.init()
font = pygame.font.Font(None, 16)

def currentFrame(keys):
    props.setMoving(False)
    props.setStatus("idle")
    event = world.current_map.keyActions(keys, world.current_map.blockedTiles, world.current_map.eventTiles)
    if event:
        if event[0] == "mapevent":
            world.setMapByName(event[1])
            currentFrameProps()
    screen = props.getScreen()

    if keys[pygame.K_q]:
        props.stopRunning()

    screen.blit(props.getBackground(), (0, 0))

    (tileX, tileY) = getTilePos(props.getPlayerPos())
    text_surface = font.render(f"x = {props.getPlayerPos().x} ({tileX}) z = {props.getPlayerPos().y} ({tileY})", True, (255, 255, 255)) # White text

    text_rect = text_surface.get_rect()
    text_rect = (10, 10)

    screen.blit(text_surface, text_rect)
    screen.blit(sprite.getSprite(), (props.getPlayerPos().x - 16, props.getPlayerPos().y - 16))
    screen.blit(props.getTopLayer(), (0, 0))
