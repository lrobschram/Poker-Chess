import string
from Board import Board


def valid_input(input, letters):

    if len(input) != 2:
        return False
    if input[0] not in letters:
        return False
    if not input[1].isdigit():
        return False

    return True


def display_pos_move_board(piece, board, pos_moves):
    dis_board = board.copy_for_display()

    for (r, c) in pos_moves:
        # only mark empty squares so we don't overwrite pieces
        if dis_board.grid[r][c] is None:
            dis_board.grid[r][c] = "★"

    print(dis_board)

def rc_to_pos(rc_tuple):
    letters = string.ascii_uppercase
    return f"{letters[rc_tuple[1]]}{rc_tuple[0]} "

def print_all_pos_moves(piece, moves, board):
    all_moves = f"All possible moves for {piece.type.name}: "
    for move in moves:
        # if (board.get_piece(move) == None):
        #     all_moves += rc_to_pos(move)
        all_moves += rc_to_pos(move)

    print(all_moves)


def ask_to_move(color, board, pieces_moved):

    letters = string.ascii_uppercase[:board.cols]

    while True:

        # grab user piece input and test if valid
        to_move_raw = input("Enter a piece's loc to move or Enter to skip (ie. A7): ").strip().upper()

        if (to_move_raw == ""):
            print("Skipped remaining movements!")
            return None, None

        if (not valid_input(to_move_raw, letters)):
            print("Please enter valid spaces on the board - try again")
            continue

        curr_loc = to_move_raw

        # check user has a piece at inputted loc
        curr_r = int(curr_loc[1])
        curr_c = letters.index(curr_loc[0])

        piece = board.get_piece( (curr_r, curr_c) )
        if (piece == None):
            print("There is no piece there - try again")
            continue
        if (piece.owner != color): 
            print("The piece must be owned by you - try again")
            continue
        if piece in pieces_moved:
            print("Piece already moved this turn - try again")
            continue

        # generate all legal moves for the piece
        all_moves = piece.get_raw_moves(board)
        display_pos_move_board(piece, board, all_moves)
        print_all_pos_moves(piece, all_moves, board)

        while True:
            # ask for new loc
            move_to_raw = input("Enter where to move to or Enter to pick a different piece (ie. A7): ").strip().upper()

            if (move_to_raw == ""):
                break

            if (not valid_input(move_to_raw, letters)):
                print("Please enter valid spaces on the board - try again")
                continue

            move = (int(move_to_raw[1]), letters.index(move_to_raw[0]))

            # check inputted new loc is in bounds and legal for the piece
            if (not board.in_bounds(move)):
                print("New position must be in bounds - try again")
                continue

            if move not in all_moves:
                print(f"{piece.type.name} is not allowed to move there")
                continue

            # make sure new spot is empty
            if (board.get_piece(move) != None) :
                print("A piece is already there - try again")
                continue

            return (curr_r, curr_c), move
    

"""
    Walks through the Movement Phase for the inputed player

    (1) keeps track of remaining moves + pieces moved this turn
    (2) asks player to move one of their pieces and checks if move is valid
    (3) updates the board accordingly
"""
def MovementPhase(player, board):

    can_move = True
    pieces_moved = []

    # make sure player has movements left
    # TODO make sure there are pieces that can move
    while can_move:

        print(f"\n~~~Moves left: {player.movements_left}~~~")
        print(board)

        # ask which piece to move
        curr_loc, new_loc = ask_to_move(player.color, board, pieces_moved)

        # check if player skipped remaining movements ??
        if (curr_loc == None and new_loc == None):
            break

        # move the piece
        board.move_piece(curr_loc, new_loc)

        # store pieces already moved this turn
        pieces_moved.append( board.get_piece(new_loc) )

        player.use_move()
        
        can_move = player.can_move()