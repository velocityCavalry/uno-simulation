from game import UnoGame
from player import Player
from card import UnoCard
from card import Color, UnoCard

DEBUG = False

def draw_cards_check(game, player, player_card):
    if player_card is None:
        if game.last_card is None or game.last_card.get_type() != 'stop':
            if game.plus > 0:
                try:
                    cards_to_draw = game.pop_cards(game.plus)
                except AssertionError:
                    return False
                game.plus = 0
            else:
                try:
                    cards_to_draw = game.pop_cards(1)
                except AssertionError:
                    return False
            player.draw(cards_to_draw)
    return True

def simulate(p1pid, p1strategy, p2pid, p2strategy):
    # simulate one game
    game = UnoGame()
    # draw 5 cards
    p1 = Player(pid=p1pid, cards=game.pop_cards(5), strategy=p1strategy)
    p2 = Player(pid=p2pid, cards=game.pop_cards(5), strategy=p2strategy)

    cnt = 1
    while True:
        player1_card = p1.play(last_card=game.last_card, opponent_num=len(p2.cards), last_color=game.last_color)

        is_plus_4_or_change = player1_card is not None and (player1_card.get_type() == 'plus4' or player1_card.get_type() == 'change color')
        if p1.strategy and is_plus_4_or_change:
            color_tbc = p1.count_and_return_max_color()
        elif is_plus_4_or_change:
            color_tbc = Color.RED
        else:
            color_tbc = None
        
        if not draw_cards_check(game, p1, player1_card):
            # print("Running out of all cards so the game ends in {} round".format(cnt))
            return [p1.pid, cnt, len(game.deck)]

        game.update(player1_card, color_tbc)
        if len(p1.cards) == 0:
            # print("Player {} wins the game in {} round".format(p1.pid, cnt))
            return [p1.pid, cnt, len(game.deck)]

        player2_card = p2.play(last_card=game.last_card, opponent_num=len(p1.cards), last_color=game.last_color)

        is_plus_4_or_change = player2_card is not None and (player2_card.get_type() == 'plus4' or player2_card.get_type() == 'change color')
        if p2.strategy and is_plus_4_or_change:
            color_tbc = p2.count_and_return_max_color()
        elif is_plus_4_or_change:
            color_tbc = Color.RED
        else:
            color_tbc = None

        if not draw_cards_check(game, p2, player2_card):
            # print("Running out of all cards so the game ends in {} round".format(cnt))
            return [p2.pid, cnt, len(game.deck)]
        
        game.update(player2_card, color_tbc)
        if len(p2.cards) == 0:
            # print("Player {} wins the game in {} round".format(p1.pid, cnt))
            return [p2.pid, cnt, len(game.deck)]

        cnt += 1

        if DEBUG:
            print('-------------------ROUND {}-------------------'.format(cnt))
            p1.hands()
            print('\tPlayer ' + str(p1.pid) + ' played ' + str(player1_card))
            p2.hands()
            print('\tPlayer ' + str(p2.pid) + ' played ' + str(player2_card))

if __name__ == '__main__':
    p1pid = 1
    p2pid = 2

    avg_round = 0
    p1win = 0
    p2win = 0
    run_out_cards = 0
    
    for i in range(0, 1000):
        winner, r, num_cards_left = simulate(p1pid, True, p2pid, False)
        avg_round += r
        if winner == p1pid:
            p1win += 1
        elif winner == p2pid:
            p2win += 1
            
    
    avg_round = avg_round / 1000
    print(avg_round)

        