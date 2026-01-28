import pygame
import random
from src.entities.enemy.enemies import Enemy
from src.scenarios.world.world import world
from src.scenarios.scenario import ScenarioBattle
from src.props import props
from src.entities.player.sprites import entitySprites
from src.entities.cordinates import getTilePos
from src.entities.character import player
from src.utils.paths import ASSETS_DIR

ACTIVE_MODE = "world"
battle_scene = None

heroSprites = entitySprites(props)

def currentFrameProps(respawn=False):
    global battle_scene

    if ACTIVE_MODE == "battle" and battle_scene is not None:
        background_image = pygame.image.load(battle_scene.imagePath).convert()
        props.setBackground(background_image)
        props.setTopLayer(None)
        return
    background_image = pygame.image.load(world.current_map.imagePath).convert()
    top_layer_image = pygame.image.load(world.current_map.topLayerPath).convert_alpha()
    props.setBackground(background_image)
    props.setTopLayer(top_layer_image)
    if respawn:
        props.player_pos.x = world.current_map.spawn_position[0]
        props.player_pos.y = world.current_map.spawn_position[1]

pygame.font.init()
font = pygame.font.Font(ASSETS_DIR / "Pixeled.ttf", 5)

def currentFrame(keys):
    global ACTIVE_MODE, battle_scene

    props.setMoving(False)
    props.setStatus("idle")
    event = None

    position = None

    if ACTIVE_MODE == "world" and keys[pygame.K_b]:
        ACTIVE_MODE = "battle"
        position = props.getPlayerPos()
        battle_scene = ScenarioBattle(player, Enemy.enemyList[5], world.current_map.name)
        currentFrameProps()
        return

    if ACTIVE_MODE == "battle" and keys[pygame.K_ESCAPE]:
        ACTIVE_MODE = "world"
        battle_scene = None
        currentFrameProps()
        return
    event = None

    if ACTIVE_MODE == "battle":
        battle_scene.keyActions(keys)
    else:
        event = world.current_map.keyActions(keys, world.current_map.blockedTiles, world.current_map.eventTiles)
        if event:
            if event[0] == "mapevent":
                world.setMapByName(event[1])
                world.current_map.setSpawnPosition(event[2])
                currentFrameProps(True)
            elif event[0] == "entityevent":
                ACTIVE_MODE = "battle"
                battle_scene = ScenarioBattle(player, Enemy.enemyList[event[1]], world.current_map.name)
                currentFrameProps()
        elif world.current_map.name == "cave":
            if props.getStatus() == "walking" or props.getStatus() == "running":
                if random.randint(1, 80) == 2:
                    ACTIVE_MODE = "battle"
                    if random.randint(1, 4) == 3:
                        Enemy.enemyList[4].hp = Enemy.enemyList[4].max_hp
                        battle_scene = ScenarioBattle(player, Enemy.enemyList[4], world.current_map.name)
                    else:
                        Enemy.enemyList[0].hp = Enemy.enemyList[0].max_hp
                        battle_scene = ScenarioBattle(player, Enemy.enemyList[0], world.current_map.name)
                    currentFrameProps()

    screen = props.getScreen()

    if keys[pygame.K_q]:
        props.stopRunning()

    screen.blit(props.getBackground(), (0, 0))

    if ACTIVE_MODE == "battle":

        battle_scene.render(screen)

        if battle_scene.request_exit:
            ACTIVE_MODE = "world"
            battle_scene = None
            currentFrameProps()
        return

    (tileX, tileY) = props.getPlayerPos()
    text_surface = font.render(
        f"x = {props.getPlayerPos().x} ({tileX}) z = {props.getPlayerPos().y} ({tileY})",
        True, (255, 255, 255)
    )
    screen.blit(text_surface, (10, 10))
    enemies = world.getEntities()
    for enemy in enemies:
        screen.blit(enemy["enemy"].getSprite(), (enemy["position"]))
    screen.blit(heroSprites.getSprite(), (props.getPlayerPos().x - 16, props.getPlayerPos().y - 24))
    top = props.getTopLayer()
    if top is not None:
        screen.blit(top, (0, 0))

