from Game import Game

def main():
    print("=== Creating Game ===")
    game = Game()

    print("\n=== Initial Board ===")
    game.print_board()

    print("\n=== Current Player ===")
    print(game.current_player_color)

    print("\n=== Switching Player ===")
    game.switch_player()
    print("Current Player:", game.current_player_color)

    print("\n=== Switching Back ===")
    game.switch_player()
    print("Current Player:", game.current_player_color)

    print("\n=== Game Over Check (should be False) ===")
    print(game.is_game_over())

    print("\n=== Forcing Black King Death ===")
    black_king = game.board.kings["Black"]
    black_king.take_damage(999)

    print("\n=== Game Over Check (should be True) ===")
    print(game.is_game_over())


if __name__ == "__main__":
    main()
