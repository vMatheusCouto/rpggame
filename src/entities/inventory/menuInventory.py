import pygame

# inventario fora de batalhas
def desenhar_inventario(tela, inventario, fonte, indice_selecionado=0):
    LARGURA_BOX = 400
    X_INICIAL = 50
    Y_INICIAL = 50
    ALTURA_ITEM = 40
    
    pygame.draw.rect(tela, (30, 30, 30), (X_INICIAL - 10, Y_INICIAL - 10, LARGURA_BOX, 300))
    pygame.draw.rect(tela, (200, 200, 200), (X_INICIAL - 10, Y_INICIAL - 10, LARGURA_BOX, 300), 2)

    if not inventario.itens:
        texto_vazio = fonte.render("Inventário Vazio", True, (150, 150, 150))
        tela.blit(texto_vazio, (X_INICIAL + 20, Y_INICIAL + 20))
    else:
        for i, item in enumerate(inventario.itens):
            pos_y = Y_INICIAL + (i * ALTURA_ITEM)
            
            if i == indice_selecionado:
                texto = f"> {item.nome} x {item.quantidade}"
                cor = (250, 255, 0)
            else:
                texto = f"  {item.nome} x {item.quantidade}"
                cor = (255, 255, 255)

            superficie_texto = fonte.render(texto, True, cor)
            tela.blit(superficie_texto, (X_INICIAL, pos_y))
            
            if i == indice_selecionado:
                desc_font = pygame.font.Font(None, 24)
                desc_surface = desc_font.render(item.descricao, True, (200, 200, 200))
                tela.blit(desc_surface, (X_INICIAL, Y_INICIAL + 260))

#inventario dentro das batalhas(formaetar)
def inventory_battle(tela, inventario, fonte, indice_selecionado=0):
    
    X_INICIAL = 400 
    Y_INICIAL = 300
    ALTURA_ITEM = 30
    LARGURA_BOX = 200
    
    
    pygame.draw.rect(tela, (0, 0, 0), (X_INICIAL - 5, Y_INICIAL - 5, LARGURA_BOX, 150))
    pygame.draw.rect(tela, (255, 255, 255), (X_INICIAL - 5, Y_INICIAL - 5, LARGURA_BOX, 150), 1)

    if not inventario.itens:
        texto_vazio = fonte.render("Vazio", True, (150, 150, 150))
        tela.blit(texto_vazio, (X_INICIAL + 10, Y_INICIAL + 10))
    else:
        for i, item in enumerate(inventario.itens):
            pos_y = Y_INICIAL + (i * ALTURA_ITEM)
            
            if i == indice_selecionado:
                texto = f"> {item.nome} ({item.quantidade})"
                cor = (250, 255, 0)
            else:
                texto = f"  {item.nome} ({item.quantidade})"
                cor = (255, 255, 255)

            superficie_texto = fonte.render(texto, True, cor)
            tela.blit(superficie_texto, (X_INICIAL, pos_y))