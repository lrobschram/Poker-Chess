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

screens = {
    Screen.POKER: PokerScreen(),
    Screen.PLACEMENT: PlacementScreen(),
    Screen.MOVEMENT: MovementScreen(),
    Screen.ATTACK: AttackScreen(),
}

curr_phase = Screen.MOVEMENT
curr_screen = screens[curr_phase]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        new_phase = curr_screen.handle_event(event, game)

        if new_phase != curr_phase:
            # TODO add some "onExit" and "onEnter" methods
            curr_phase = new_phase
            curr_screen = screens[curr_phase]

    curr_screen.draw(screen, game)
    pygame.display.flip()

pygame.quit()
