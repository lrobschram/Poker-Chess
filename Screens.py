from enum import Enum, auto

class Screen(Enum):
    POKER = auto()
    PLACEMENT = auto()
    MOVEMENT = auto()
    ATTACK = auto()
    GAME_OVER = auto()
    START = auto()