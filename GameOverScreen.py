import pygame


class PokerScreen:
    def __init__(self):
        self.font = pygame.font.SysFont("dejavusans", 35)


    def handle_event(self, event, game):
        return None
    

    def draw(self, screen, game):
        screen.fill((100, 100, 100))
        text = self.font.render(f"GAME OVER", True, (0, 0, 0))
        screen.blit(text, (250, 250))


    def on_enter(self, screen, game):
        return None
    

    def on_exit(self, screen, game):
        return None