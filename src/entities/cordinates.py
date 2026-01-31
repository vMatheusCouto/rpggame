# Transferir para Character ou Player

def getTilePos(player_pos):
    tileX = int(player_pos.x / (640/80))
    tileY = int(player_pos.y / (384/48))
    return (tileX, tileY)
