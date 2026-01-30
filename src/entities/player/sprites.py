from src.utils.paths import CHARACTER_ASSETS
import pygame

class entitySprites:
    def __init__(self, entity):
        self.current = 0
        self.currentMax = 4
        self.characterSprites = []
        self.entity = entity

    def load(self):
        characterStatus = f"{self.entity.getStatus()}/"
        characterDirection = f"{self.entity.getDirection()}/"
        self.characterSprites = []
        characterSpritesCount = 0
        if self.entity.getStatus() == "idle":
            characterSpritesCount = 4
        elif self.entity.getStatus() == "walking":
            characterSpritesCount = 6
        elif self.entity.getStatus() == "running":
            characterSpritesCount = 6
        for count in range(characterSpritesCount):
            self.characterSprites.append(pygame.image.load(CHARACTER_ASSETS / f"{self.entity.path}/{self.entity.getStatus()}/{characterDirection}/characterbase{count+1}.png"))

    def advanceSprite(self):
        self.current += 1
        if self.current >= len(self.characterSprites):
            self.current = 0
        self.load()
        if self.current >= len(self.characterSprites):
            self.current = 0
    def getSprite(self):
        self.advanceSprite()
        self.load()
        return self.characterSprites[self.current]
