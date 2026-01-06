import pygame
from Game import Game
from Screens import Screen
from MovementScreen import MovementScreen
from PokerScreen import PokerScreen
from PlacementScreen import PlacementScreen
from AttackScreen import AttackScreen


pygame.init()
screen = pygame.display.set_mode((560, 560))
pygame.display.set_caption("Board Game")

game = Game()

curr_phase = Screen.MOVEMENT
curr_screen = MovementScreen()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if curr_phase == Screen.POKER:
            curr_phase = PokerScreen.handle_event(event, game)

        elif curr_phase == Screen.PLACEMENT:
            curr_phase = PlacementScreen.handle_event(event, game)

        elif curr_phase == Screen.MOVEMENT:
            curr_phase = curr_screen.handle_event(event, game)
        
        elif curr_phase == Screen.ATTACK:
            curr_phase = AttackScreen.handle_event(event, game)

    if curr_phase == Screen.POKER:
        PokerScreen.draw(screen, game)

    elif curr_phase == Screen.PLACEMENT:
        PlacementScreen.draw(screen, game)

    elif curr_phase == Screen.MOVEMENT:
        curr_screen.draw(screen, game)

    elif curr_phase == Screen.ATTACK:
        AttackScreen.draw(screen, game)

    pygame.display.flip()


pygame.quit()
