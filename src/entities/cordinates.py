def getTilePos(player_pos):
    tileX = 0
    for i in range(30):
        if player_pos.x >= (i+1) * GAME_RESOLUTION[0] / 30 and player_pos.x <= (i+2) * GAME_RESOLUTION[0] / 30:
            tileX = i+1
            break
    tileY = 0
    for i in range(18):
        if player_pos.y >= (i+1) * GAME_RESOLUTION[1] / 18 and player_pos.y <= (i+2) * GAME_RESOLUTION[1] / 18:
            tileY = i+1
            break
    return (tileX, tileY)
