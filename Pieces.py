from enum import Enum, auto
from MovementRules import MOVEMENT_RULES

class PieceType(Enum):
    KING = auto()
    WARRIOR = auto()
    ARCHER = auto()
    KNIGHT = auto()
    DIREWOLF = auto()
    CATAPULT = auto()
    HEALER = auto()
    WIZARD = auto()
    JUGGERNAUT = auto()
    QUEEN = auto()
    
PIECE_STATS = {
    # Highcard
    PieceType.WARRIOR: {
        "health": 2,
        "heal": 0,
        "attack": 1,
        "movement": 1,
        "range": 1,
        "movement_rule": "forward_only",
        "promotes_to": PieceType.JUGGERNAUT
    },

    # Pair
    PieceType.ARCHER: {
        "health": 2,
        "heal": 0,
        "attack": 1,
        "movement": 1,
        "range": 3,  # +2 range
        "movement_rule": "forward_only",
        "promotes_to": PieceType.QUEEN
    },

    # Two-Pair
    PieceType.KNIGHT: {
        "health": 3,
        "heal": 0,
        "attack": 1,
        "movement": 1,
        "range": 1,
        "movement_rule": "knight",
        "promotes_to": None
    },

    # 3 of a Kind
    PieceType.WIZARD: {
        "health": 2,
        "heal": 0,
        "attack": 2,
        "movement": 1,
        "range": 2,  # +1 range
        "movement_rule": "king",
        "promotes_to": None
    },

    # Straight
    PieceType.CATAPULT: {
        "health": 3,
        "heal": 0,
        "attack": 2,
        "movement": 1,
        "range": 3,  # +2 range
        "movement_rule": "any",
        "promotes_to": None
    },

    # Flush
    PieceType.HEALER: {
        "health": 5,
        "heal": 2,
        "attack": 1,  
        "movement": 1,
        "range": 1,
        "movement_rule": "king",
        "promotes_to": None
    },

    # Full House
    PieceType.DIREWOLF: {
        "health": 4,
        "heal": 0,
        "attack": 3,
        "movement": 3,
        "range": 1,
        "movement_rule": "wolf",
        "promotes_to": None
    },

    # Four of a Kind
    PieceType.JUGGERNAUT: {
        "health": 7,
        "heal": 0,
        "attack": 3,
        "movement": 2,
        "range": 1,
        "movement_rule": "any",
        "promotes_to": None
    },

    # Straight Flush
    PieceType.QUEEN: {
        "health": 6,
        "heal": 0,
        "attack": 3,
        "movement": 2,
        "range": 3,  # Range+2
        "movement_rule": "any",
        "promotes_to": None
    },

    # King (for completeness)
    PieceType.KING: {
        "health": 7,
        "heal": 0,
        "attack": 2,
        "movement": 1,
        "range": 1,
        "movement_rule": "king",
        "promotes_to": None
    },
}

PIECE_SYMBOLS = {
    "KING": "K",
    "KNIGHT": "N",
    "QUEEN": "Q",
    "ARCHER": "A",
    "WARRIOR": "W",
    "DIREWOLF": "D",
    "HEALER": "H",
    "JUGGERNAUT": "J",   
    "WIZARD": "Z",
    "CATAPULT": "C",
}


class Piece:
    #initializes all fields of a piece   
    def __init__(self, piece_type, owner):
        self.type = piece_type
        self.owner = owner
        self.row = None 
        self.col = None 
        self.bonus = "commonUnit"
        self.image_obj = None
        
        self.apply_stats()

    #applys all stats to the piece
    def apply_stats(self):

        stats = PIECE_STATS[self.type]
        self.max_health = stats["health"]
        self.health = stats["health"]
        self.attack = stats["attack"]
        self.movement = stats["movement"]
        self.range = stats["range"]
        self.movement_rule = stats["movement_rule"]
        self.promotes_to = stats["promotes_to"]
        self.heal = stats["heal"]
        
    #Sets first initial of white pieces to uppercase
    def piece_initial(self):
        if (self.owner == "White"):
            return PIECE_SYMBOLS[self.type.name].upper()
        else:
            return PIECE_SYMBOLS[self.type.name].lower()
        
    #gets all moves that are possible
    def get_raw_moves(self, board):
        move_func = MOVEMENT_RULES[self.movement_rule]
        return move_func(board, self)
  
  #subtracts the damage done by the attack, returns true if the piece is dead, false otherwise
    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.health = 0  # Clamp to 0 to avoid negative health
        return self.is_piece_dead()
    
    
    def is_piece_dead(self):
        return self.health <= 0
        
    def promote(self):
        if (self.promotes_to != None):
            self.type = self.promotes_to
            self.apply_stats()
    
    def take_heal(self, amount):
    
        if self.health >= self.max_health:
            return False
        self.health = min(self.max_health, self.health + amount)
        return True
    
    def addBonusHealth(self):
        self.max_health += 1
        self.health += 1
        return self.max_health
    
    def addBonusDamage(self):
        self.attack += 1
        return self.attack
    
    def perform_action(self, target):
        if target is None:
            return False

        # Heal allies if this piece can heal
        if target.owner == self.owner and getattr(self, "heal", 0) > 0:
            return target.take_heal(self.heal)  # True if heal applied

        # Damage enemies
        if target.owner != self.owner:
            target.take_damage(self.attack)  # death is handled separately
            return True

        return False