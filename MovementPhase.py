class MovementPhase:
    def __init__(self, max_moves=3):
        self.moves_remaining = max_moves

    def can_move(self):
        return self.moves_remaining > 0

    def use_move(self):
        if self.can_move():
            self.moves_remaining -= 1
            return True
        return False