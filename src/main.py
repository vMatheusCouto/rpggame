import os
import pygame

from src.frames import *

pygame.init()

# Display
pygame.display.set_caption("RPG Game")
pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 0)


background_image = pygame.image.load(currentFrameProps()).convert()
props.setBackground(background_image)

# Time
clock = pygame.time.Clock()

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
