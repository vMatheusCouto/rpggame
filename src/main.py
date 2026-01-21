import os
import pygame

from src.frames import *

pygame.init()

pygame.display.set_caption("RPG Game")
pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 0)

currentFrameProps()

clock = pygame.time.Clock()
pygame.font.init()

while props.getRunning():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    currentFrame(keys)
    pygame.display.update()
    pygame.display.flip()

    dt = clock.tick(12) / 1000
    props.setDT(dt)

pygame.quit()
