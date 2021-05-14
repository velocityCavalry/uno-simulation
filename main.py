from game import UnoGame


if __name__ == '__main__':
    game = UnoGame()
    print(game.get_deck_str())
    print(len(game.deck))