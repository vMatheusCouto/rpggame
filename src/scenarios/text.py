from src.context import context

class TextMixin():

    def render_text(self, text, center, position, size="small", color=(255,255,255)):
        font = context.font_small
        if size == "medium":
            font = context.font_medium
        elif size == "large":
            font = context.font_large
        surface = font.render(str(text), True, color)
        position_center = (0,0)
        if center:
            position_center = (context.screen.get_width() / 2, context.screen.get_height() / 2)

            rect = surface.get_rect(
                center=(position_center[0] + position[0], position_center[1] + position[1])
            )
            context.screen.blit(surface, rect)
        else:
            context.screen.blit(surface, position)
