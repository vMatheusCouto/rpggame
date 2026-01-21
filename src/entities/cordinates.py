def getTilePos(player_pos):
    tileX = round(player_pos.x / (640/40))
    tileY = round(player_pos.y / (384/24))
    return (tileX, tileY)
