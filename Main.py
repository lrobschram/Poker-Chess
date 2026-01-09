import pygame
from Game import Game
from Screens import Screen
from MovementScreen import MovementScreen
from PokerScreen import PokerScreen
from PlacementScreen import PlacementScreen
from AttackScreen import AttackScreen

pygame.init()

BOARD_W = 8 * 70  # 560
PANEL_W = 200
screen = pygame.display.set_mode((BOARD_W + PANEL_W, BOARD_W))
pygame.display.set_caption("Board Game")

game = Game()

screens = {
    Screen.POKER: PokerScreen(),
    Screen.PLACEMENT: PlacementScreen(),
    Screen.MOVEMENT: MovementScreen(),
    Screen.ATTACK: AttackScreen(),
}

curr_phase = Screen.POKER
curr_screen = screens[curr_phase]

running = True
while running:

    # send screen events from the player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        new_phase = curr_screen.handle_event(event, game)

        # change screens when switching to a new phase
        if new_phase != curr_phase:
            
            curr_screen.on_exit(screen, game) # clean up screen before switching
            curr_phase = new_phase
            curr_screen = screens[curr_phase]
            curr_screen.on_enter(screen, game) # set up new screen just switched to

    curr_screen.draw(screen, game)
    pygame.display.flip()

pygame.quit()
