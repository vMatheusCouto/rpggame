from abc import ABC, abstractmethod
from src.scenarios.world.overworld.movement import *
import pygame
class Scenario(ABC):
    def __init__(self, imagePath):
        self.imagePath = imagePath

    @abstractmethod
    def keyActions():
        pass

class ScenarioOpenWorld(Scenario):
    def __init__(self, imagePath, blockedTiles, topLayerPath, spawn_position, eventTiles):
        super().__init__(imagePath)
        self.blockedTiles = blockedTiles
        self.events = []
        self.topLayerPath = topLayerPath
        self.spawn_position = spawn_position
        self.eventTiles = eventTiles

    def keyActions(self, keys, blockedTiles, eventTiles):
        canMove = True
        event = None
        props.setSpeed(35)
        if keys[pygame.K_LSHIFT]:
            props.setSpeed(60)
        if keys[pygame.K_w] and canMove:
            event = walkUp(blockedTiles, eventTiles)
            canMove = False
        if keys[pygame.K_s] and canMove:
            event = walkDown(blockedTiles, eventTiles)
            canMove = False
        if keys[pygame.K_a] and canMove:
            event = walkLeft(blockedTiles, eventTiles)
            canMove = False
        if keys[pygame.K_d] and canMove:
            event = walkRight(blockedTiles, eventTiles)
            canMove = False
        return event

class ScenarioDialogue(Scenario):
    pass

class ScenarioBattle(Scenario):
    pass
