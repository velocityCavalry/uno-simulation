from game import UnoGame
from player import Player
from card import UnoCard
from card import Color, UnoCard


class Gameover(Exception):
    def __init__(self, pid):
        print("Winner: player", pid)

def draw_cards_check(game, player, player_card):
    if player_card is None:
        if game.last_card is None or game.last_card.get_type() != 'stop':
            if game.plus > 0:
                cards_to_draw = game.pop_cards(game.plus)
                game.plus = 0
            else:
                cards_to_draw = game.pop_cards(1)
            player.draw(cards_to_draw)


def check_win(player):
    if len(player.cards) == 0:
        raise Gameover(player.pid)
    pass

if __name__ == '__main__':
    # simulate one game
    game = UnoGame()
    # draw 5 cards
    p1 = Player(pid=1, cards=game.pop_cards(5))
    p2 = Player(pid=2, cards=game.pop_cards(5))
    p1.hands()
    p2.hands()

    cnt = 0
    for round in range(0, 10):
        print('round', cnt)
        player1_card = p1.play(last_card=game.last_card, opponent_num=len(p2.cards), last_color=game.last_color)
        print('\tPlayer ' + str(p1.pid) + ' played ' + str(player1_card))

        is_plus_4_or_change = player1_card is not None and (player1_card.get_type() == 'plus4' or player1_card.get_type() == 'change color')
        if p1.strategy and is_plus_4_or_change:
            color_tbc = p1.count_and_return_max_color()
        elif is_plus_4_or_change:
            color_tbc = Color.RED
        else:
            color_tbc = None

        draw_cards_check(game, p1, player1_card)
        game.update(player1_card, color_tbc)
        check_win(p1)
        p1.hands()

        player2_card = p2.play(last_card=game.last_card, opponent_num=len(p1.cards), last_color=game.last_color)
        print('\tPlayer ' + str(p2.pid) + ' played ' + str(player2_card))

        is_plus_4_or_change = player2_card is not None and (player2_card.get_type() == 'plus4' or player2_card.get_type() == 'change color')
        if p2.strategy and is_plus_4_or_change:
            color_tbc = p2.count_and_return_max_color()
        elif is_plus_4_or_change:
            color_tbc = Color.RED
        else:
            color_tbc = None

        draw_cards_check(game, p2, player2_card)
        game.update(player2_card, color_tbc)
        check_win(p2)
        p2.hands()

        cnt += 1
    