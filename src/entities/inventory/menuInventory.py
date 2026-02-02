import pygame
    
def desenhar_inventario(tela, inventario, fonte, indice_selecionado=0):
    LARGURA_BOX = 400
    ALTURA_ITEM = 40
    X_INICIAL = 50
    Y_INICIAL = 50
    
    pygame.draw.rect(tela, (50, 50, 50), (X_INICIAL - 10, Y_INICIAL - 10, LARGURA_BOX, 300))
    pygame.draw.rect(tela, (200, 200, 200), (X_INICIAL - 10, Y_INICIAL - 10, LARGURA_BOX, 300), 2)

    if not inventario.itens:
        texto_vazio = fonte.render("Inventário Vazio", True, (150, 150, 150))
        tela.blit(texto_vazio, (X_INICIAL + 20, Y_INICIAL + 20))
    else:
        for i, item in enumerate(inventario.itens):
            pos_y = Y_INICIAL + (i * ALTURA_ITEM)
            
            # Muda a cor  ou coloca seta se for o item selecionado
            if i == indice_selecionado:
                texto = f"> {item.nome} x {item.quantidade}"
                cor = (250, 255, 0) # Amarelo
            else:
                texto = f"  {item.nome} x {item.quantidade}"
                cor = (255, 255, 255)

            superficie_texto = fonte.render(texto, True, cor)
            tela.blit(superficie_texto, (X_INICIAL, pos_y))
            
            # Linha pra separar item
            pygame.draw.line(tela, (80, 80, 80), (X_INICIAL, pos_y + 35), (X_INICIAL + 350, pos_y + 35))