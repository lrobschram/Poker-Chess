FORWARD_OFFSETS = {
    "White": [(1, 0), (0, -1), (0, 1)],
    "Black": [(-1, 0), (0, -1), (0, 1)]
}

ANY_ONE_DIRECTION_OFFSET = [
    (1, 0), (-1, 0), (0, 1), (0, -1),
    (1, 1), (1, -1), (-1, 1), (-1, -1)
]

KNIGHT_OFFSETS = [
    (2, 1), (2, -1),
    (-2, 1), (-2, -1),
    (1, 2), (1, -2),
    (-1, 2), (-1, -2)
]


#helper method that returns legal moves based on the offset of the pieces
def offset_moves(board, piece, offsets):
    moves = []

    for dr, dc in offsets:
        r = piece.row + dr
        c = piece.col + dc

        if not board.in_bounds((c, r)):
            continue

        target = board.get_piece((c, r))
        if target is None: 
            moves.append((r, c))

    return moves

#helper method for ray moves that returns how many squares you can move in that direction
def ray_moves(board, piece, directions, max_distance):
    legal = []

    for dr, dc in directions:
        for step in range(1, max_distance + 1):
            r = piece.row + dr * step
            c = piece.col + dc * step

            if not board.in_bounds((c, r)):
                break

            target = board.get_piece((c, r))
            if target is None:
                legal.append((r, c))
            else:
                break  # Stop if anything is in the way

    return legal

#method that returns movement in any direction 
def any_dir_moves(board, piece):
    # max_distance comes from piece.movement
    return ray_moves(board, piece, ANY_ONE_DIRECTION_OFFSET, piece.movement)

# warrior, archer
def forward_moves(board, piece):
    return offset_moves(board, piece, FORWARD_OFFSETS[piece.owner])
#king
def king_moves(board, piece):
    return offset_moves(board, piece, ANY_ONE_DIRECTION_OFFSET)
#knight
def knight_moves(board, piece):
    return offset_moves(board, piece, KNIGHT_OFFSETS)

#dire wolf
def wolf_moves(board, piece):

    legal = []

    # Determine forward direction based on owner
    if piece.owner == "White":
        forward_dir = [(1, 0)]   # forward = down the rows
    else:
        forward_dir = [(-1, 0)]  # forward = up the rows

    # 4 squares forward
    legal.extend(ray_moves(board, piece, forward_dir, 4))


    # 1 square in any direction
    ANY_ONE_DIRECTION_OFFSET = [
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (1, -1), (-1, 1), (-1, -1)
    ]


    legal.extend(offset_moves(board, piece, ANY_ONE_DIRECTION_OFFSET))

    return legal

MOVEMENT_RULES = {
    "king": king_moves,
    "knight": knight_moves,
    "wolf": wolf_moves,
    "forward_only": forward_moves,
    "any": any_dir_moves,  
}