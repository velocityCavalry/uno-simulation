from game import UnoGame
from player import Player
from card import UnoCard

class Gameover(Exception):
    def __init__(self, pid):
        print("Winner: player", pid)

def draw_cards_check(game, player, player_card):
    if game.last_card is None or (player_card is None and game.last_card.get_type() != 'stop'):
        cards_to_draw = []
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

    
    for i in range(0, 5):
        print('round', i)
        player1_card = p1.play(last_card=game.last_card, last_color=game.last_color)
        print('\tPlayer ' + str(p1.pid) + ' played ' + str(player1_card))
        draw_cards_check(game, p1, player1_card)
        game.update(p1.pid, player1_card)
        #print("last card =", game.last_card)
        #print("last color =", game.last_color)
        check_win(p1)
        p1.hands()

        player2_card = p2.play(last_card=game.last_card, last_color=game.last_color)
        print('\tPlayer ' + str(p2.pid) + ' played ' + str(player2_card))
        draw_cards_check(game, p2, player2_card)
        game.update(p2.pid, player2_card)
        #print("last card =", game.last_card)
        #print("last color =", game.last_color)
        check_win(p2)
        p2.hands()
    