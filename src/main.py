import os
import pygame

# Carregamento inicial (manter nessa ordem)
from src.entities.moves.moves import Move
Move.load_attacks()

from src.scenarios.world.map import Map
from src.entities.character import Enemy
Map.load_maps()
Enemy.load_enemies()

from src.save import Save
Save.load_saves()

from src.frames import *
pygame.init()

pygame.display.set_caption("RPG Game")
pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 0)

clock = pygame.time.Clock()
pygame.font.init()
pygame.mixer.init()

frames = Frames()

# Loop que compõe o jogo inteiro
while context.running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            context.stop_running()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                context.stop_running()

    # Frame atual, gerencia ações e renderização e atualização da tela
    frames.current_frame(pygame.key.get_pressed())

    pygame.display.update()
    pygame.display.flip()

    dt = clock.tick(12) / 1000
    context.delta = dt

pygame.mixer.music.stop()
pygame.quit()
