from enum import Enum, auto
from MovementRules import MOVEMENT_RULES

class PieceType(Enum):
    KING = auto()
    WARRIOR = auto()
    ARCHER = auto()
    KNIGHT = auto()
    DIREWOLF = auto()
    CATAPULT = auto()
    JUGGERNAUT = auto()
    WIZARD = auto()
    JESTER = auto()
    QUEEN = auto()
PIECE_STATS = {
    # Highcard
    PieceType.WARRIOR: {
        "health": 1,
        "attack": 1,
        "movement": 1,
        "range": 1,
        "movement_rule": "forward_only",
        "promotes_to": PieceType.JESTER
    },

    # Pair
    PieceType.ARCHER: {
        "health": 1,
        "attack": 1,
        "movement": 1,
        "range": 2,  # +1 range
        "movement_rule": "forward_only",
        "promotes_to": PieceType.QUEEN
    },

    # Two-Pair
    PieceType.KNIGHT: {
        "health": 3,
        "attack": 1,
        "movement": 1,
        "range": 1,
        "movement_rule": "knight",
        "promotes_to": None
    },

    # 3 of a Kind
    PieceType.WIZARD: {
        "health": 2,
        "attack": 2,
        "movement": 1,
        "range": 2,  # +1 range
        "movement_rule": "king",
        "promotes_to": None
    },

    # Straight
    PieceType.CATAPULT: {
        "health": 3,
        "attack": 2,
        "movement": 1,
        "range": 3,  # +2 range
        "movement_rule": "king",
        "promotes_to": None
    },

    # Flush
    PieceType.JUGGERNAUT: {
        "health": 5,
        "attack": 2,
        "movement": 2,
        "range": 1,
        "movement_rule": "any",
        "promotes_to": None
    },

    # Full House
    PieceType.DIREWOLF: {
        "health": 2,
        "attack": 3,
        "movement": 4,
        "range": 1,
        "movement_rule": "wolf",
        "promotes_to": None
    },

    # Four of a Kind
    PieceType.JESTER: {
        "health": 4,
        "attack": 4,
        "movement": 2,
        "range": 1,
        "movement_rule": "any",
        "promotes_to": None
    },

    # Straight Flush
    PieceType.QUEEN: {
        "health": 5,
        "attack": 5,
        "movement": 2,
        "range": 2,  # Range+1
        "movement_rule": "any",
        "promotes_to": None
    },

    # King (for completeness)
    PieceType.KING: {
        "health": 5,
        "attack": 2,
        "movement": 1,
        "range": 1,
        "movement_rule": "king",
        "promotes_to": None
    },
}

class Piece:

    def __init__(self, piece_type, owner):
        self.type = piece_type
        self.owner = owner

        self.row = None
        self.col = None

        self.apply_stats()

    def apply_stats(self):
        
        stats = PIECE_STATS[self.type]
        self.max_health = stats["health"]
        self.health = stats["health"]
        self.attack = stats["attack"]

    def piece_initial(self):
        if (self.owner == "White"):
            return self.type.name[0].upper()
        else:
            return self.type.name[0].lower()
    
    def get_raw_moves(self, board):
        move_func = MOVEMENT_RULES[self.movement_rule]
        return move_func(board, self)
        