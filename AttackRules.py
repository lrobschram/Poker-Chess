from MovementRules import (
    ANY_ONE_DIRECTION_OFFSET,
    KNIGHT_OFFSETS
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

    for dr, dc in ANY_ONE_DIRECTION_OFFSET:
        for step in range(1, piece.range + 1):
            r = piece.row + dr * step
            c = piece.col + dc * step

            if not board.in_bounds((r, c)):
                break

            target = board.get_piece((r, c))
            if target and target.owner != piece.owner:
                targets.append((r, c))

    return targets

# -------------------------------------------------
# Public API (used by Game / AttackScreen)
# -------------------------------------------------

def get_attack_targets(board, piece):
    """
    Returns a list of (row, col) squares that this piece can attack.
    """

    # Knight: offset-only
    if piece.type == PieceType.KNIGHT:
        return offset_attacks(board, piece, KNIGHT_OFFSETS)

    # Catapult: ignores line of sight
    if piece.type == PieceType.CATAPULT:
        return catapult_attacks(board, piece)

    # Default: all directions, ray-based
    return ray_attacks(
        board,
        piece,
        ANY_ONE_DIRECTION_OFFSET,
        piece.range
    )
