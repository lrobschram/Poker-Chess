from MovementRules import (
    ANY_ONE_DIRECTION_OFFSETS,
    KNIGHT_OFFSETS,
    ORTHOGONAL_OFFSETS,
    DIAGONAL_OFFSETS
)


from Pieces import PieceType

# -------------------------------------------------
# Core ray helper (offsets + range + blocking)
# -------------------------------------------------

def ray_attacks(board, piece, directions, max_range):
    """
    Ray-based attack logic.
    - Walks in given directions
    - Stops at first piece
    - Can attack that piece if enemy
    """
    targets = []

    for dr, dc in directions:
        for step in range(1, max_range + 1):
            r = piece.row + dr * step
            c = piece.col + dc * step

            if not board.in_bounds((r, c)):
                break

            target = board.get_piece((r, c))

            if target is None:
                continue

            # First piece hit
            if target.owner != piece.owner:
                targets.append((r, c))

            break  # ray ALWAYS stops at first piece

    return targets

from MovementRules import ORTHOGONAL_OFFSETS

def get_heal_targets(board, healer):

    targets = []

    for dr, dc in ORTHOGONAL_OFFSETS:  # only orthogonal directions
        for step in range(1, healer.range + 1):
            r = healer.row + dr * step
            c = healer.col + dc * step

            if not board.in_bounds((r, c)):
                break

            target = board.get_piece((r, c))
            if target is None:
                continue

            # Only heal allies that are not full health
            if target.owner == healer.owner and target.health < target.max_health:
                targets.append((r, c))

            break  # healer stops at first piece in that direction

    return targets


# -------------------------------------------------
# Offset-only attacks (Knight-style)
# -------------------------------------------------

def offset_attacks(board, piece, offsets):
    """
    Single-step attacks using offsets.
    (Used by Knight)
    """
    targets = []

    for dr, dc in offsets:
        r = piece.row + dr
        c = piece.col + dc

        if not board.in_bounds((r, c)):
            continue

        target = board.get_piece((r, c))
        if target and target.owner != piece.owner:
            targets.append((r, c))

    return targets
# -------------------------------------------------
# Catapult (range but NO line-of-sight)
# -------------------------------------------------

def catapult_attacks(board, piece):
    """
    Catapult ignores blockers.
    Can attack any enemy within range.
    """
    targets = []

    for dr, dc in ORTHOGONAL_OFFSETS:
        for step in range(1, piece.range + 1):
            r = piece.row + dr * step
            c = piece.col + dc * step

            if not board.in_bounds((r, c)):
                break

            target = board.get_piece((r, c))
            if target and target.owner != piece.owner:
                targets.append((r, c))

    return targets

# Healer-specific healing targets (orthogonal only)
def get_heal_targets(board, healer):
    targets = []
    for dr, dc in ORTHOGONAL_OFFSETS:
        for step in range(1, healer.range + 1):
            r = healer.row + dr * step
            c = healer.col + dc * step
            if not board.in_bounds((r, c)):
                break
            target = board.get_piece((r, c))
            if target is None:
                continue
            if target.owner == healer.owner and target.health < target.max_health:
                targets.append((r, c))
            break  # healer stops at first piece in that direction
    return targets

# Public API
def get_attack_targets(board, piece):
    targets = []

     # Healer: include both healable allies and attackable enemies
    if piece.type == PieceType.HEALER:
        targets = get_heal_targets(board, piece)  # allies
        targets += ray_attacks(board, piece, ORTHOGONAL_OFFSETS, piece.range)  # enemies
        return targets
    # Add normal attacks
    if piece.type == PieceType.KNIGHT:
        targets += offset_attacks(board, piece, KNIGHT_OFFSETS)

    if piece.type == PieceType.CATAPULT:
        targets += catapult_attacks(board, piece)
    else:
        targets += ray_attacks(board, piece, ORTHOGONAL_OFFSETS, piece.range)

    return targets