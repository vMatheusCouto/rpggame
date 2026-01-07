# Example file showing a circle moving on screen
import os
import pygame

# pygame setup
pygame.init()
GAME_RESOLUTION = (640, 384)
pygame.display.set_caption("Pixel Art Game")
pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 0)

screen = pygame.display.set_mode(GAME_RESOLUTION, pygame.FULLSCREEN | pygame.SCALED)
clock = pygame.time.Clock()
running = True
dt = 0
borderLimit = 10
hunting = False
enemySpeed = 40
moving = False
movingDirection = None
value = 0
paused = False

characterPath = "./assets/character/"
characterDirection = "down/"
characterSprites = [pygame.image.load(f"{characterPath}{characterDirection}Sprite1.png"),
                pygame.image.load(f"{characterPath}{characterDirection}Sprite2.png"),
                pygame.image.load(f"{characterPath}{characterDirection}Sprite3.png")]

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
enemy_pos = pygame.Vector2(20, 20)

background_image_original = pygame.image.load('./assets/background.png').convert()
background_image = pygame.transform.scale(background_image_original, GAME_RESOLUTION)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_r:
                player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
                enemy_pos = pygame.Vector2(20, 20)

    keys = pygame.key.get_pressed()
    if paused:
        pass
    else:
        screen.blit(background_image, (0, 0))

        pygame.draw.circle(screen, "red", enemy_pos, 4)

        enemyCanMove = True
        if hunting:
            if enemy_pos.x >= player_pos.x - 10 and enemy_pos.x <= player_pos.x + 10:
                if enemy_pos.y >= player_pos.y - 10 and enemy_pos.y <= player_pos.y + 10:
                    hunting = False
                else:
                    if enemy_pos.y < player_pos.y and enemyCanMove:
                        enemy_pos.y += enemySpeed * dt
                        enemyCanMove = False
                    if enemy_pos.y > player_pos.y and enemyCanMove:
                        enemy_pos.y -= enemySpeed * dt
                        enemyCanMove = False
            else:
                if enemy_pos.x < player_pos.x and enemyCanMove:
                    enemy_pos.x += enemySpeed * dt
                    enemyCanMove = False
                if enemy_pos.x > player_pos.x and enemyCanMove:
                    enemy_pos.x -= enemySpeed * dt
                    enemyCanMove = False
        print("enemypos: ", enemy_pos.x)
        print("playerpos", player_pos.x)

        canMove = True
        """ grid tile based
        speed = 2
        print("Pos X:", player_pos.x)
        print("Pos Y:", player_pos.y)
        print("Screen X:", GAME_RESOLUTION[0])
        print("Screen Y:", GAME_RESOLUTION[1])
        print(GAME_RESOLUTION[0] % player_pos.x)
        print(GAME_RESOLUTION[1] % player_pos.y)

        if moving:
            print("ok")
            if movingDirection == "up":
                player_pos.y -= speed
            if movingDirection == "down":
                player_pos.y += speed
            if movingDirection == "right":
                player_pos.x -= speed
            if movingDirection == "left":
                player_pos.x += speed

            if movingDirection == "left" or movingDirection == "right":
                print("1")
                if GAME_RESOLUTION[0] % player_pos.x == 0:
                    moving = False
                    print("2")

            print(movingDirection)
            if movingDirection == "up" or movingDirection == "down":
                print("4")
                if GAME_RESOLUTION[1] % player_pos.y == 0:
                    print("3")
                    moving = False
        if not moving:
            if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
                moving = True
                if keys[pygame.K_w]:
                    movingDirection = "up"
                if keys[pygame.K_s]:
                    movingDirection = "down"
                if keys[pygame.K_a]:
                    movingDirection = "left"
                if keys[pygame.K_d]:
                    movingDirection = "right"
        """
        if keys[pygame.K_LSHIFT]:
            speed = 40

        if keys[pygame.K_h]:
            hunting = True

        if keys[pygame.K_w] and canMove and player_pos.y > borderLimit:
            player_pos.y -= speed * dt
            canMove = False
        if keys[pygame.K_s] and player_pos.y < screen.get_height() - borderLimit:
            print("pos ", player_pos.y)
            print("height ", screen.get_height())
            player_pos.y += speed * dt
            canMove = False
            moving = True
        if keys[pygame.K_a] and canMove and player_pos.x > borderLimit:
            player_pos.x -= speed * dt
            canMove = False
        if keys[pygame.K_d] and canMove and player_pos.x < screen.get_width() - borderLimit:
            player_pos.x += speed * dt
            canMove = False
        speed = 16

        if moving:
            value += 1

        if value >= len(characterSprites):
            value = 0

        image = characterSprites[value]

        screen.blit(image, player_pos)
        pygame.display.update()

        pygame.draw.circle(screen, "red", enemy_pos, 4)

        pygame.display.flip()

        dt = clock.tick(12) / 1000


pygame.quit()

