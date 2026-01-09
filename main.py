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
movingDirection = "down"
value = 0
paused = False
newDirection = "down"
movingStatus = "idle"

characterSprites = []
def loadSprites():
    global characterSprites
    characterPath = "./assets/character/"
    characterStatus = f"{movingStatus}/"
    characterDirection = f"{movingDirection}/"
    characterSprites = []
    characterSpritesCount = 0
    if movingStatus == "idle":
        characterSpritesCount = 4
    elif movingStatus == "walking":
        characterSpritesCount = 6
    for count in range(characterSpritesCount):
        print(count)
        characterSprites.append(pygame.image.load(f"{characterPath}{characterStatus}{characterDirection}characterbase{count+1}.png"))

loadSprites()

pygame.font.init()
font = pygame.font.Font(None, 30) # None uses the default built-in font
text_surface = font.render("Paused", True, (255, 255, 255)) # White text

text_rect = text_surface.get_rect()
text_rect.center = (screen.get_width() / 2, screen.get_height() / 2) # Center the text on the screen


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
enemy_pos = pygame.Vector2(20, 20)

background_image_original = pygame.image.load('./assets/background4.png').convert()
background_image = pygame.transform.scale(background_image_original, GAME_RESOLUTION)
nonPassableRange = [[[77,84], [180, 141]]]
nonPassableTiles = [[[8, 5],[13, 8]],[[3,3],[9,7]],[[0, 0],[4, 17]],[[5,12],[5,17]],[[5,14],[4,17]],[[5,15],[13,17]]]

mapArray = []

for y in range(0, GAME_RESOLUTION[1], 32):
    row = []
    for x in range(0, GAME_RESOLUTION[0], 32):
        row.append([x, y, x + 32, y + 32, True, False])
    mapArray.append(row)

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
        screen.blit(text_surface, text_rect)

        pygame.display.update()
        pygame.display.flip()
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
        print("Pos X:", player_pos.x)
        print("Pos Y:", player_pos.y)
        """
        TILE_SIZE = 21

        for y in range(0, GAME_RESOLUTION[1], TILE_SIZE):
            for x in range(0, GAME_RESOLUTION[0], TILE_SIZE):
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    (x, y, TILE_SIZE, TILE_SIZE),
                    1  # outline only
                )
        """
        tileX = 0
        for i in range(30):
            if player_pos.x >= (i+1) * GAME_RESOLUTION[0] / 30 and player_pos.x <= (i+2) * GAME_RESOLUTION[0] / 30:
                tileX = i+1
                break
        print(tileX)

        tileY = 0
        for i in range(18):
            if player_pos.y >= (i+1) * GAME_RESOLUTION[1] / 18 and player_pos.y <= (i+2) * GAME_RESOLUTION[1] / 18:
                tileY = i+1
                break
        print(tileY)

        canMove = True
        """ grid tile based
        speed = 2
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
            speed = 50

        if keys[pygame.K_h]:
            hunting = True
        movingStatus = "idle"

        if keys[pygame.K_w] and canMove and player_pos.y > borderLimit:
            player_pos.y -= speed * dt
            canMove = False
            moving = True
            movingStatus = "walking"
            newDirection = "up"
        if keys[pygame.K_s] and player_pos.y < screen.get_height() - borderLimit:
            player_pos.y += speed * dt
            canMove = False
            moving = True
            movingStatus = "walking"
            newDirection = "down"
        if keys[pygame.K_a] and canMove and player_pos.x > borderLimit:
            player_pos.x -= speed * dt
            canMove = False
            moving = True
            movingStatus = "walking"
            newDirection = "left"
        if keys[pygame.K_d] and canMove and player_pos.x < screen.get_width() - borderLimit:
            player_pos.x += speed * dt
            canMove = False
            moving = True
            movingStatus = "walking"
            newDirection = "right"

        targetTileX = 0
        for i in range(30):
            if player_pos.x >= (i+1) * GAME_RESOLUTION[0] / 30 and player_pos.x <= (i+2) * GAME_RESOLUTION[0] / 30:
                targetTileX = i+1
                break
        print(targetTileX)

        targetTileY = 0
        for i in range(18):
            if player_pos.y >= (i+1) * GAME_RESOLUTION[1] / 18 and player_pos.y <= (i+2) * GAME_RESOLUTION[1] / 18:
                targetTileY = i+1
                break
        print(targetTileY)
        if targetTileX != tileX:
            print("AGORA SIM")

        if targetTileY != targetTileY:
            print("AGORA SIM")

        if moving:
            goBack = False
            for positions in nonPassableTiles:
                if goBack:
                    break
                print(positions[0][0])
                print(positions[1][0])
                if int(targetTileX) in range(positions[0][0], positions[1][0]):
                    print("não pode passar 1")
                    if int(targetTileY) in range(positions[0][1], positions[1][1]):
                        goBack = True
                        print("não pode passar 2")

            if movingDirection == "up" and goBack:
                player_pos.y += speed * dt
                print(f"Speed: {speed}")

            if movingDirection == "down" and goBack:
                player_pos.y -= speed * dt
                print(f"Speed: {speed}")

            if movingDirection == "right" and goBack:
                player_pos.x -= speed * dt
                print(f"Speed: {speed}")

            if movingDirection == "left" and goBack:
                player_pos.x += speed * dt
                print(f"Speed: {speed}")

            moving = False

        value += 1
        if value >= len(characterSprites):
            value = 0
        if newDirection != movingDirection:
            movingDirection = newDirection

        loadSprites()
        if value >= len(characterSprites):
            value = 0
        speed = 32
        print("Value",value)
        print("Status",movingStatus)
        image = characterSprites[value]

        screen.blit(image, player_pos)
        pygame.display.update()

        pygame.draw.circle(screen, "red", enemy_pos, 4)

        pygame.display.flip()

        dt = clock.tick(12) / 1000


pygame.quit()

