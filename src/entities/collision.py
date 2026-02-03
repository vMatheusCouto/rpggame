def entity_collision(playerPos, entityPos):
    x = 40
    y = 35
    if playerPos.x >= entityPos[0] - x:
        if playerPos.x <= entityPos[0] + x:
            if playerPos.y >= entityPos[1] - y:
                if playerPos.y <= entityPos[1] + y:
                    return True
    return False
