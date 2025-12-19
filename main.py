# Example file showing a circle moving on screen
import os
import pygame

# pygame setup
pygame.init()
GAME_RESOLUTION = (640, 360)
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
value = 0

characterPath = "./assets/character/"
characterDirection = "down/"
characterSprites = [pygame.image.load(f"{characterPath}{characterDirection}Sprite1.png"),
                pygame.image.load(f"{characterPath}{characterDirection}Sprite2.png"),
                pygame.image.load(f"{characterPath}{characterDirection}Sprite3.png")]


def load_image(name):
    # Joins the current directory path with the image name for cross-platform compatibility
    fullname = os.path.join(os.path.dirname(__file__), name)
    try:
        image = pygame.image.load(fullname)
        # Use convert_alpha() for images with transparency (like PNGs)
        if name.endswith('.png'):
            return image.convert_alpha()
        else:
            return image.convert() # Use convert() for opaque images
    except pygame.error as message:
        print(f"Cannot load image: {name}")
        raise SystemExit(message)

player_image = load_image('character.png')
player_rect = player_image.get_rect()

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_rect.center = player_pos
enemy_pos = pygame.Vector2(20, 20)


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

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

    keys = pygame.key.get_pressed()
    canMove = True
    speed = 16
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


    if keys[pygame.K_q]:
        running = False

    if moving:
        value += 1

    if value >= len(characterSprites):
        value = 0

    image = characterSprites[value]

    screen.blit(image, player_pos)
    pygame.display.update()
    moving = False

    pygame.draw.circle(screen, "red", enemy_pos, 4)

    pygame.display.flip()

    dt = clock.tick(12) / 1000


pygame.quit()

