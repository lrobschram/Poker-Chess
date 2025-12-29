class AttackPhase:
    def __init__(self, max_attacks=2):
        self.attacks_remaining = max_attacks

    def can_attack(self):
        return self.attacks_remaining > 0

    def use_attack(self):
        if self.can_attack():
            self.attacks_remaining -= 1
            return True
        return False