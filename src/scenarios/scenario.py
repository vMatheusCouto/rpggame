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
    def __init__(self, imagePath, blockedTiles):
        super().__init__(imagePath)
        self.blockedTiles = blockedTiles
        self.events = []

    def keyActions(self, keys):
        canMove = True
        
        props.setSpeed(35)
        if keys[pygame.K_LSHIFT]:
            props.setSpeed(60)
        if keys[pygame.K_w] and canMove:
            walkUp()
            canMove = False
        if keys[pygame.K_s] and canMove:
            walkDown()
            canMove = False
        if keys[pygame.K_a] and canMove:
            walkLeft()
            canMove = False
        if keys[pygame.K_d] and canMove:
            walkRight()
            canMove = False

class ScenarioDialogue(Scenario):
    pass

class ScenarioBattle(Scenario):
    pass
