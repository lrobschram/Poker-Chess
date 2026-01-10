FORWARD_OFFSETS = {
    "White": [(-1, 0), (0, -1), (0, 1)],
    "Black": [(1, 0), (0, -1), (0, 1)]
}

ANY_ONE_DIRECTION_OFFSETS = [
    (1, 0), (-1, 0), (0, 1), (0, -1),
    (1, 1), (1, -1), (-1, 1), (-1, -1)
]

KNIGHT_OFFSETS = [
    (2, 1), (2, -1),
    (-2, 1), (-2, -1),
    (1, 2), (1, -2),
    (-1, 2), (-1, -2)
]
# Orthogonal directions only (NO diagonals)
ORTHOGONAL_OFFSETS = [
    (1, 0),   # down
    (-1, 0),  # up
    (0, 1),   # right
    (0, -1),  # left
]

# If you still need diagonals elsewhere
DIAGONAL_OFFSETS = [
    (1, 1), (1, -1),
    (-1, 1), (-1, -1),
]

#helper method that returns legal moves based on the offset of the pieces
@staticmethod
def offset_moves(board, piece, offsets):
    moves = []

    for dr, dc in offsets:
        r = piece.row + dr
        c = piece.col + dc

        if not board.in_bounds((r, c)):
            continue

        target = board.get_piece((r, c))
        if target is None: 
            moves.append((r, c))

    return moves

@staticmethod
#helper method for ray moves that returns how many squares you can move in that direction
def ray_moves(board, piece, directions, max_distance):
    legal = []

    for dr, dc in directions:
        for step in range(1, max_distance + 1):
            r = piece.row + dr * step
            c = piece.col + dc * step

            if not board.in_bounds((r, c)):
                break

            target = board.get_piece((r, c))
            if target is None:
                legal.append((r, c))
            else:
                break  # Stop if anything is in the way

    return legal


#method that returns movement in any direction 
@staticmethod
def any_dir_moves(board, piece):
    # max_distance comes from piece.movement
    return ray_moves(board, piece, ORTHOGONAL_OFFSETS, piece.movement)

# warrior, archer
@staticmethod
def forward_moves(board, piece):
    return offset_moves(board, piece, FORWARD_OFFSETS[piece.owner])
#king
@staticmethod
def king_moves(board, piece):
    return offset_moves(board, piece, ANY_ONE_DIRECTION_OFFSETS)
#knight
@staticmethod
def knight_moves(board, piece):
    return offset_moves(board, piece, KNIGHT_OFFSETS)



#dire wolf
@staticmethod
def wolf_moves(board, piece):

    legal = []

    # Determine forward direction based on owner
    if piece.owner == "White":
        forward_dir = [(-1, 0)]   # forward = down the rows
    else:
        forward_dir = [(1, 0)]  # forward = up the rows

    # 4 squares forward
    legal.extend(ray_moves(board, piece, forward_dir, 4))


    legal.extend(offset_moves(board, piece, ORTHOGONAL_OFFSETS))

    return legal

MOVEMENT_RULES = {
    "king": king_moves,
    "knight": knight_moves,
    "wolf": wolf_moves,
    "forward_only": forward_moves,
    "any": any_dir_moves,  
}


