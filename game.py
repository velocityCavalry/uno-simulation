from random import choice, shuffle
from card import UnoCard


class UnoGame:
    def __init__(self, players, time_number_cards=2, time_num_function=1):

        # initialize players

        # initialize card decks
        self.deck = self.__create_deck(time_number_cards, time_num_function)
        self.num_cards = len(self.deck)



    def __create_deck(self, time_number_cards, time_num_function):

        colors = list(range(4))  # 0, 1, 2, 3
        numbers = list(range(1, 10)) # 1, 2, 3..., 9
        functions = ["plus2", "plus4", "stop", "change color"]

        deck = []

        # create number cards:
        for _ in time_number_cards:
            for color in colors:
                for number in numbers:
                    card = UnoCard(color=color, number=number, type=None)
                    deck.append(card)

        # create plus2 cards:
        for _ in time_number_cards:
            for color in colors:
                card = UnoCard(color=color, number=None, type="plus2")
                deck.append(card)

        # create other functional cards:
        for _ in time_num_function:
            for function in functions[1:]:
                for _ in range(4):
                    card = UnoCard(color=None, number=None, type=function)
                    deck.append(card)

        return deck




