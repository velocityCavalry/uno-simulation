from random import choice, shuffle
from card import UnoCard


class UnoGame:
    def __init__(self, players=2, time_number_cards=2, time_num_function=1):

        # initialize players

        # initialize card decks
        self.deck = self.__create_deck(time_number_cards, time_num_function)
        self.num_cards = len(self.deck)



    def __create_deck(self, time_number_cards, time_num_function):

        colors = list(range(4))  # 0, 1, 2, 3
        numbers = list(range(1, 10)) # 1, 2, 3..., 9
        functions = ["plus4", "change color"]

        deck = []

        # create number cards:
        for _ in range(time_number_cards):
            for color in colors:
                for number in numbers:
                    card = UnoCard(color=color, number=number, type=None)
                    deck.append(card)

        # create plus2 and stop cards:
        for _ in range(time_number_cards):
            for color in colors:
                for function in ['plus 2', 'stop']:
                    card = UnoCard(color=color, number=None, type=function)
                    deck.append(card)

        # create other functional cards:
        for _ in range(time_num_function):
            for function in ["plus4", "change color"]:
                for i in range(4):
                    card = UnoCard(color=None, number=None, type=function)
                    deck.append(card)

        shuffle(deck)
        return deck


    def get_deck_str(self):
        return str([str(x) for x in self.deck])





