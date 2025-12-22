from enum import Enum, auto

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
    PieceType.KING: {
        "health": 5,
        "attack": 2,
        "movement": 1,
        "range": 1,
        "movement_rule": "king"
    },

    PieceType.WARRIOR: {
        "health": 1,
        "attack": 1,
        "movement": 1,
        "range": 1,
        "movement_rule": "forward_only"
    },

    PieceType.ARCHER: {
        "health": 1,
        "attack": 1,
        "movement": 1,
        "range": 2,
        "movement_rule": "forward_only"
    },

    PieceType.KNIGHT: {
        "health": 3,
        "attack": 1,
        "movement": 1,
        "range": 1,
        "movement_rule": "knight"
    },

    PieceType.DIREWOLF: {
        "health": 2,
        "attack": 3,
        "movement": 3,
        "range": 1,
        "movement_rule": "straight_or_side"
    },

    PieceType.CATAPULT: {
        "health": 3,
        "attack": 2,
        "movement": 1,
        "range": 3,
        "movement_rule": "any"
    },

    PieceType.JUGGERNAUT: {
        "health": 5,
        "attack": 2,
        "movement": 2,
        "range": 1,
        "movement_rule": "any"
    },

    PieceType.WIZARD: {
        "health": 2,
        "attack": 3,
        "movement": 1,
        "range": 4,
        "movement_rule": "any"
    },

    PieceType.JESTER: {
        "health": 4,
        "attack": 4,
        "movement": 2,
        "range": 1,
        "movement_rule": "any"
    },

    PieceType.QUEEN: {
        "health": 5,
        "attack": 5,
        "movement": 2,
        "range": 2,
        "movement_rule": "any"
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
        self.movement = stats["movement"]
        self.range = stats["range"]
        self.movement_rule = stats["movement_rule"]

    def is_alive(self):
        return self.health > 0

    def take_damage(self, dmg):
        self.health -= dmg

    def piece_initial(self):
        if (self.owner == "White"):
            return self.type.name[0].upper()
        else:
            return self.type.name[0].lower()
        