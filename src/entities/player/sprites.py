from src.utils.paths import CHARACTER_ASSETS
from src.props import props
import pygame

characterSprites = []
def loadSprites():
    global characterSprites
    characterStatus = f"{props.getStatus()}/"
    characterDirection = f"{props.getDirection()}/"
    characterSprites = []
    characterSpritesCount = 0
    if props.getStatus() == "idle":
        characterDirection = "down"
        characterSpritesCount = 4
    elif props.getStatus() == "walking":
        characterSpritesCount = 6
    elif props.getStatus() == "running":
        characterSpritesCount = 6
    for count in range(characterSpritesCount):
        characterSprites.append(pygame.image.load(CHARACTER_ASSETS / f"{props.getStatus()}/{characterDirection}/characterbase{count+1}.png"))

class sprites:
    def __init__(self):
        self.current = 0
        self.currentMax = 4
        self.characterSprites = characterSprites
    def advanceSprite(self):
        self.current += 1
        if self.current >= len(characterSprites):
            self.current = 0
        loadSprites()
        if self.current >= len(characterSprites):
            self.current = 0
    def getSprite(self):
        self.advanceSprite()
        loadSprites()
        return characterSprites[self.current]

sprite = sprites()
