from game import UnoGame
from player import Player
from card import Color
import matplotlib.pyplot as plt
import argparse
from tqdm import tqdm
from statistics import mean

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


def simulate_one_game(p1pid, p1strategy, p2pid, p2strategy):
    # simulate one game
    game = UnoGame()
    # draw 5 cards
    p1 = Player(pid=p1pid, cards=game.pop_cards(5), strategy=p1strategy)
    p2 = Player(pid=p2pid, cards=game.pop_cards(5), strategy=p2strategy)

    cnt = 1
    while True:
        player1_card = p1.play(last_card=game.last_card,
                               opponent_num=len(p2.cards),
                               last_color=game.last_color)

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

        player2_card = p2.play(last_card=game.last_card,
                               opponent_num=len(p1.cards),
                               last_color=game.last_color)

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
            print(f'-' * 10 + f'ROUND {cnt}' + '-' * 10)
            p1.hands()
            print(f'\tPlayer {p1.pid} played {str(player1_card)}')
            p2.hands()
            print(f'\tPlayer {p2.pid} played {str(player2_card)}')


def simulate_games(num_games, p1strategy, p2strategy, verbose=False):
    p1pid = 1
    p2pid = 2
    avg_round, p1win, p2win, run_out_cards = 0, 0, 0, 0

    for _ in range(1, num_games + 1):
        winner, r, num_cards_left = simulate_one_game(p1pid=p1pid,
                                                      p1strategy=p1strategy,
                                                      p2pid=p2pid,
                                                      p2strategy=p2strategy)
        avg_round += r
        if winner == p1pid:
            p1win += 1
        elif winner == p2pid:
            p2win += 1

    avg_round = avg_round / num_games

    if verbose:
        print(f'the average number of rounds to end the game is {avg_round}')
        print(f'the number of games p1 wins is {p1win}')
        print(f'the number of games p2 wins is {p2win} ')
        print(f'the number of games that run out of cards is {run_out_cards}')

    return avg_round, p1win, p2win, run_out_cards


def winning_rate_diff(args):
    exp_num = 1000
    # simulate 100 args.num_game and calculate winning rate, do this exp_num times to get histogram
    p1_win_rate_diffs = []
    for i in range(exp_num):
        _, p1win_no_stra, _, _ = simulate_games(args.num_game, False, False)
        _, p1win_wi_stra, _, _ = simulate_games(args.num_game, True, False)
        p1_win_rate_diff = (p1win_wi_stra - p1win_no_stra) / args.num_game
        p1_win_rate_diffs.append(p1_win_rate_diff)
    
    # An "interface" to matplotlib.axes.Axes.hist() method
    n, bins, patches = plt.hist(x=p1_win_rate_diffs, bins='auto', color='#0504aa',
                                alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Winning rate of player 1 with strategy - winning rate of player 1 with no strategy')
    plt.ylabel('Frequency')
    plt.title('Histogram of difference in winning rate of player 1 distribution')
    plt.text(23, 45, r'$\mu=15, b=3$')
    plt.show()


def first_exp(args):
    # first experiment: whether the probability of strategy/no strategy converges or not
    strategy_avg_rounds,  strategy_p1win_rate, strategy_p2win_rate = [], [], []
    avg_rounds, p1win_rate, p2win_rate, p1win_rate_diff = [], [], [], []

    for i in tqdm(range(1, args.num_game + 1)):
        strategy_avg_round, strategy_p1win, \
            strategy_p2win, _ = simulate_games(num_games=i,
                                                p1strategy=True,
                                                p2strategy=False,
                                                verbose=False)
        no_strategy_avg_round, no_strategy_p1win, \
            no_strategy_p2win, _ = simulate_games(num_games=i,
                                                    p1strategy=False,
                                                    p2strategy=False,
                                                    verbose=False)

        strategy_avg_rounds.append(strategy_avg_round)
        strategy_p1win_rate.append(strategy_p1win / i)
        strategy_p2win_rate.append(strategy_p2win / i)

        avg_rounds.append(no_strategy_avg_round)
        p1win_rate.append(no_strategy_p1win / i)
        p2win_rate.append(no_strategy_p2win / i)

        p1win_rate_diff.append(strategy_p1win / i - no_strategy_p1win / i)

    # p1 (w/strategy w/out strategy) winning rate vs. number of games simulated
    plt.figure()
    plt.plot(list(range(1, args.num_game + 1)), strategy_p1win_rate, label='the rate of p1 wins using strategy')
    plt.plot(list(range(1, args.num_game + 1)), p1win_rate, label='the rate of p1 wins using no strategy')
    plt.xlabel('number of games simulated')
    plt.legend()
    plt.title('number of games simulated vs the rate of p1 wins with and without strategy')
    plt.savefig(f'figs/p1-win-rate-{args.num_game}.png')
    plt.clf()

    # p2 number of games simulated vs the average # rounds to end each game
    plt.figure()
    plt.plot(list(range(1, args.num_game + 1)), strategy_avg_rounds,
                label='the average # rounds to end each game when p1 uses strategy')
    plt.plot(list(range(1, args.num_game + 1)), avg_rounds,
                label='the average # rounds to end each game when p1 uses no strategy')
    plt.xlabel('number of games simulated')
    plt.legend()
    plt.title('number of games simulated vs the average # rounds to end each game')
    plt.savefig(f'figs/average-rounds-{args.num_game}.png')
    plt.clf()

    print(p1win_rate)
    print(strategy_p1win_rate)

    print(f'the average p1 win rate using strategy is {mean(strategy_p1win_rate)}')
    print(f'the average p1 win rate using no strategy is {mean(p1win_rate)}')
    print(f'the average p2 win rate when p1 use strategy is {mean(strategy_p2win_rate)}')
    print(f'the average p2 win rate using no strategy is {mean(p2win_rate)}')
    print(f'the average rounds to end the game when p1 uses strategy is {mean(strategy_avg_rounds)}')
    print(f'the average rounds to end the game when p1 does not use strategy is {mean(avg_rounds)}')



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--experiment', type=int, default=1,
                        help='1 = converge experiment\n\
                                2 = difference in winning rate experiment\n\
                                3 = ?')
    parser.add_argument('--num-game', type=int, default=100,
                        help='the number of simulated games')
    args = parser.parse_args()

    if args.experiment == 1 and args.num_game:
        first_exp(args)

    elif args.experiment == 2 and args.num_game:
        winning_rate_diff(args)

    elif args.experiment == 3 and args.num_game:
        print('unknown')

    else:
        print('Usage: python main.py --experiment --num-game NUM-GAME')
        exit(1)
                                                                    



