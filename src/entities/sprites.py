from src.utils.paths import CHARACTER_ASSETS
import os
import pygame

class entity_sprites:
    def __init__(self, entity):
        self.current = 0
        self.current_max = 0
        self.character_sprites = []
        self.entity = entity
        self.amount = 0
        self.current_status = "init"
        self.current_direction = "init"
        self.non_loop = ["death","pierce","hit","slice", "slice2", "rush"]
        self.once = ["pierce","hit","slice", "slice2", "rush"]

    def load(self):
        character_status = f"{self.entity.status}/"
        character_direction = f"{self.entity.direction}/"
        self.character_sprites = []
        if self.current_max == 0:
            if self.entity.status == "idle":
                self.amount = 4
            elif self.entity.status == "walking":
                self.amount = 6
            elif self.entity.status == "running":
                self.amount = 6
            elif self.entity.status == "death":
                if self.entity.name == "Skeleton":
                    self.amount = 8
                elif self.entity.name == "Orc Shaman":
                    self.amount = 7
                else:
                    self.amount = 6

            elif self.entity.status == "pierce":
                self.amount = 8
            elif self.entity.status == "hit":
                self.amount = 4
            elif self.entity.status == "slice":
                self.amount = 8
            elif self.entity.status == "slice2":
                self.amount = 8
            elif self.entity.status == "rush":
                self.amount = 8
        else:
            self.amount = self.current_max
        for count in range(self.amount):
            print(count)
            self.character_sprites.append(pygame.image.load(CHARACTER_ASSETS / f"{self.entity.path}/{self.entity.status}/{character_direction}characterbase{count+1}.png"))

    def advance_sprite(self):
        load = False
        if self.entity.status != self.current_status:
            load = True
        if self.entity.direction != self.current_direction:
            load = True
        if load:
            self.current_status = self.entity.status
            self.current_direction = self.entity.direction

            self.reset_sprite()
        if self.current_status in self.once and self.current == self.amount:
            self.current_status = "idle"
            self.current_direction = "right"

            self.reset_sprite()

        self.current += 1
        if self.current == len(self.character_sprites) and self.entity.status in self.non_loop:
            self.current -= 1
            if load:
                self.load()
        else:
            if self.current >= len(self.character_sprites):
                self.current = 0
            if load:
                self.load()
            if self.current >= len(self.character_sprites):
                self.current = 0

    def reset_sprite(self, maximum=0):
        self.current = 0
        if maximum != 0:
            self.current_max = maximum

    def get_sprite(self):
        self.advance_sprite()
        return self.character_sprites[self.current]
