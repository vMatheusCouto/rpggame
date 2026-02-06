import pygame
from src.context import context

class Sound:
    def __init__(self):
        self.__current_music = None

    def load_music(self):
        if context.add_music == "stop":
            pygame.mixer.music.unload()
        elif context.add_music != self.__current_music:
            self.__current_music = context.add_music
            pygame.mixer.music.load(self.__current_music)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.3)

    def load_effect(self):
        if context.add_sound_effect:
            self.__current_sound_effect = context.add_sound_effect
            sound_effect = pygame.mixer.Sound(self.__current_sound_effect)
            sound_effect.set_volume(1)
            sound_effect.play()
            context.add_sound_effect = None

sound = Sound()
