import pygame
from Screens import Screen
from ui import Button

class AttackScreen:

    def __init__(self):
        self.font = pygame.font.SysFont("helvetica", 35)
        self.hud_font = pygame.font.SysFont("helvetica", 18)
        self.skip_button = Button(
            rect=(250, 250, 160, 40), 
            text="TESTING",
            font=self.hud_font,
            bg_color=(200, 200, 200)
            )
        

    def handle_event(self, event, game):

        if self.skip_button.is_clicked(event):
            return Screen.MOVEMENT
        
        return Screen.ATTACK
    

    def draw(self, screen, game):
        screen.fill((240, 240, 240))
        self.skip_button.draw(screen)

    def on_enter(self, screen, game):
        return None
