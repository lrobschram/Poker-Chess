import pygame
from Game import Game
from Screens import Screen
from MovementScreen import MovementScreen
from PokerScreen import PokerScreen
from PlacementScreen import PlacementScreen
from AttackScreen import AttackScreen
from GameOverScreen import GameOverScreen
from StartScreen import StartScreen
from CardCollectionScreen import CardCollectionScreen

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
    Screen.GAME_OVER: GameOverScreen(),
    Screen.START: StartScreen(),
    Screen.CARD_COLLECTION: CardCollectionScreen(),
}

clock = pygame.time.Clock()

curr_phase = Screen.START
curr_screen = screens[curr_phase]

curr_screen.on_enter(screen, game)  # initial poker set up

running = True
while running:

    new_phase = curr_phase  # default: stay here

    # 1) handle input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        new_phase = curr_screen.handle_event(event, game)
        if new_phase != curr_phase:
            break  # stop processing events; we’re switching

    if not running:
        break

    # 2) update screen logic EVERY FRAME (timers, animations, etc.)
    update_phase = curr_screen.update(screen, game)

    # if update wants a phase change, honor it
    if update_phase != curr_phase:
        new_phase = update_phase

    # 3) switch screens if needed
    if new_phase != curr_phase:
        curr_screen.on_exit(screen, game)
        curr_phase = new_phase
        curr_screen = screens[curr_phase]
        curr_screen.on_enter(screen, game)

    # 4) draw
    curr_screen.draw(screen, game)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
