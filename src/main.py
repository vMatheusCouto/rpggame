import os
import pygame

from src.frames import *

# Inicializar mapa, ataques e inimigos
from src.scenarios.world.map import Map
from src.entities.moves.moves import Move
from src.entities.character import Enemy
Map.load_maps()
Move.load_attacks()
Enemy.load_enemies()

pygame.init()

pygame.display.set_caption("RPG Game")
pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 0)

clock = pygame.time.Clock()
pygame.font.init()

frames = Frames()

# Loop que compõe o jogo inteiro
while context.running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Frame atual, gerencia ações e renderização e atualização da tela
    frames.current_frame(pygame.key.get_pressed())

    pygame.display.update()
    pygame.display.flip()

    dt = clock.tick(12) / 1000
    context.delta = dt

pygame.quit()
