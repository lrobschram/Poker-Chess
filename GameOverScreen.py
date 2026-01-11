import pygame
from Screens import Screen


class GameOverScreen:
    def __init__(self):
        self.font = pygame.font.SysFont("helvetica", 35)


    def handle_event(self, event, game):
        return Screen.GAME_OVER
    

    def draw(self, screen, game):
        screen.fill((100, 100, 100))

        lines = [
            f"GAME OVER",
            f"{game.winner} wins!"
        ]

        y = 250
        for line in lines:
            text = self.font.render(line, True, (0, 0, 0))
            screen.blit(text, (250, y))
            y += 50


    def on_enter(self, screen, game):
        return None
    

    def on_exit(self, screen, game):
        return None