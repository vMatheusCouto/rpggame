from src.utils.paths import CHARACTER_ASSETS
import os
import pygame

class entitySprites:
    def __init__(self, entity):
        self.current = 0
        self.currentMax = 0
        self.characterSprites = []
        self.entity = entity
        self.amount = 0
        self.currentStatus = "init"
        self.currentDirection = "init"
        self.nonLoop = ["death","pierce","hit","slice", "slice2", "rush"]
        self.once = ["pierce","hit","slice", "slice2", "rush"]

    def load(self):
        characterStatus = f"{self.entity.getStatus()}/"
        characterDirection = f"{self.entity.getDirection()}/"
        self.characterSprites = []
        if self.currentMax == 0:
            if self.entity.getStatus() == "idle":
                self.amount = 4
            elif self.entity.getStatus() == "walking":
                self.amount = 6
            elif self.entity.getStatus() == "running":
                self.amount = 6
            elif self.entity.getStatus() == "death":
                if self.entity.name == "Skeleton":
                    print("skeleton")
                    self.amount = 8
                elif self.entity.name == "Orc Shaman":
                    self.amount = 7
                else:
                    self.amount = 6

            elif self.entity.getStatus() == "pierce":
                self.amount = 8
            elif self.entity.getStatus() == "hit":
                self.amount = 4
            elif self.entity.getStatus() == "slice":
                self.amount = 8
            elif self.entity.getStatus() == "slice2":
                self.amount = 8
            elif self.entity.getStatus() == "rush":
                self.amount = 8
        else:
            self.amount = self.currentMax
        for count in range(self.amount):
            self.characterSprites.append(pygame.image.load(CHARACTER_ASSETS / f"{self.entity.path}/{self.entity.getStatus()}/{characterDirection}/characterbase{count+1}.png"))

    def advanceSprite(self):
        print("entityst",self.entity.getStatus())
        print("currentst:",self.currentStatus)
        load = False
        if self.entity.getStatus() != self.currentStatus:
            load = True
        if self.entity.getDirection() != self.currentDirection:
            load = True
        if load:
            self.currentStatus = self.entity.getStatus()
            self.currentDirection = self.entity.getDirection()

            self.resetSprite()
        if self.currentStatus in self.once and self.current == self.amount:
            self.currentStatus = "idle"
            self.currentDirection = "right"

            self.resetSprite()

        self.current += 1
        if self.current == len(self.characterSprites) and self.entity.getStatus() in self.nonLoop:
            self.current -= 1
            if load:
                self.load()
        else:
            if self.current >= len(self.characterSprites):
                self.current = 0
            if load:
                self.load()
            if self.current >= len(self.characterSprites):
                self.current = 0

    def resetSprite(self, maximum=0):
        self.current = 0
        if maximum != 0:
            self.currentMax = maximum

    def getSprite(self):
        self.advanceSprite()
        return self.characterSprites[self.current]
