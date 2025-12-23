def forward_moves(board, piece):
    return NotImplementedError

def king_moves(board, piece):
    return NotImplementedError

def knight_moves(board, piece):
    return NotImplementedError

def wolf_moves(board, piece):
    return NotImplementedError

def any_dir_moves(board, piece):
    return NotImplementedError

MOVEMENT_RULES = {
    "king": king_moves,
    "knight": knight_moves,
    "wolf": wolf_moves,
    "forward_only": forward_moves,
    "any": any_dir_moves,  
}