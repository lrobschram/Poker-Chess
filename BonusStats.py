BONUS_VALUE = {"commonUnit": 0, "healthyUnit": 1, "strongUnit": 2, "royalUnit": 3}

class BonusStats:
    def __init__(self):
        self.played = []  # store bonusValue each time the player plays

    def record_play(self, chips):
        if chips < 40: tier = "commonUnit"
        elif chips < 50: tier = "healthyUnit"
        elif chips < 60: tier = "strongUnit"
        else: tier = "royalUnit"
        self.played.append(BONUS_VALUE[tier])

    def avg_played(self):
        return sum(self.played) / len(self.played) if self.played else 0.0

    def dist_played(self):
        from collections import Counter
        return Counter(self.played)