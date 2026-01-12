import pygame
from Screens import Screen
from ui import Button


class StartScreen:
    def __init__(self):
        self.font = pygame.font.SysFont("helvetica", 35)
        self.hud_font = pygame.font.SysFont("helvetica", 18)
        self.start_button = Button(
            rect=(260, 300, 160, 40),
            text="Start Game",
            font=self.hud_font,
            bg_color=(200, 200, 200)
        )


    def handle_event(self, event, game):

        if self.start_button.is_clicked(event):
            return Screen.POKER

        return Screen.START
    

    def draw(self, screen, game):
        screen.fill((100, 100, 100))
        text = self.font.render(f"Start Game!", True, (0, 0, 0))
        screen.blit(text, (250, 250))
        self.start_button.draw(screen)


    def on_enter(self, screen, game):
        return None
    

    def on_exit(self, screen, game):
        player = game.get_current_player()
        player.start_turn()

    def update(self, screen, game):
        return Screen.START