class Render:
    def __init__(self):

    def _draw_rect(self, screen, rect):
        pygame.draw.rect(screen, (128, 128, 128), rect, border_radius)

    def _draw_text(self, screen, text, x, y, font):
        surf = font.render(text, True, (255, 255, 255))
        screen.blit(surf, (x, y))
