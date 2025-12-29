class AttackRules:
    @staticmethod
    def resolve_attack(attacker, defender, board):
       #check range
       if not AttackRules.in_range(attacker, defender):
           return False
        #calculate damage
       damage = attacker.attack
       died = defender.take_damage(damage)
       if died:
           #remove piece from board
           board.remove_piece(defender)
       return True
    
    #checks if defender is in range of attacker
    @staticmethod
    def in_range(attacker, defender):
        row_dist = abs(attacker.row - defender.row)
        col_dist = abs(attacker.col - defender.col)

        return max(row_dist, col_dist) <= attacker.range