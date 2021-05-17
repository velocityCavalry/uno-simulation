from random import randint

DEBUG = False


class Player:
    def __init__(self, pid, cards, strategy=False):
        self.pid = pid
        self.cards = cards
        self.strategy = strategy
    
    def draw(self, cards_to_draw):
        for card in cards_to_draw:
            self.cards.append(card)
    
    def win(self):
        return len(self.cards) == 0

    def hands(self):
        print('\tPlayer ' + str(self.pid) + ' has ' + str(len(self.cards)) + ' cards')
        for card in self.cards:
            print('\t\t' + str(card))
        print()

    def play(self, opponent_num=None, last_card=None, last_color=None):

        # sanity check
        assert len(self.cards) > 0
        # if last_color is None:
        #     assert last_card is None

        if last_card is None:
            # At the beginning of the game
            if last_color is None:
                card = self.cards.pop(randint(0, len(self.cards) - 1))
                # card = self.check_color(card)
                return card
            # last card is None, so the last player does not play a card but color is fixed
            # in this case, the player who played 'stop' can play another stop of different color
            else:
                eligible_cards = []
                for card in self.cards:
                    if card.get_type() == 'plus4' or card.get_type() == 'change color':
                        eligible_cards.append(card)
                    elif card.get_color() == last_color:
                        eligible_cards.append(card)
                if DEBUG:
                    print(f'{self.pid} eligible cards:  {str([str(x) for x in eligible_cards])}')

                if len(eligible_cards) == 0:
                    return None

                card_to_pop = eligible_cards[randint(0, len(eligible_cards) - 1)]
                self.cards.remove(card_to_pop)

                # card_to_pop = self.check_color(card_to_pop)
                return card_to_pop
        
        # middle of the game
        # case 1: stop for one round
        if last_card.get_type() == 'stop':
            return None

        eligible_cards = []
        # functional and non-functional cards:
        for card in self.cards:
            # if last card is a normal card
            if not last_card.is_functional():
                # the card to play must have
                if card.is_functional():
                    if (card.get_type() != 'stop' and card.get_type() != 'plus2') or \
                            card.get_color() == last_card.get_color():
                        eligible_cards.append(card)
                elif last_card.get_color() == card.get_color() or last_card.get_number() == card.get_number():
                    eligible_cards.append(card)
            else:
                if card.get_type() == 'plus4':
                    eligible_cards.append(card)
                if last_card.get_type() == 'plus2':
                    if card.get_type() == 'plus2':
                        eligible_cards.append(card)
                if last_card.get_type() == 'change color':
                    if card.get_type() == 'change color':
                        eligible_cards.append(card)
        if DEBUG:
            print(f'{self.pid} eligible cards:  {str([str(x) for x in eligible_cards])}')

        if len(eligible_cards) == 0:
            return None

        if not self.strategy:
            card_to_pop = eligible_cards[randint(0, len(eligible_cards) - 1)]
        else:  # use strategy
            eligible_cards = self.strategically_pop(eligible_cards, opponent_num)
            card_to_pop = eligible_cards[0]

        self.cards.remove(card_to_pop)

        # card_to_pop = self.check_color(card_to_pop)
        return card_to_pop

    # count the current deck and return the color that has maximum number of cards
    def count_and_return_max_color(self):
        color2card = dict()
        for card in self.cards:
            if not card.is_functional or card.get_type == 'plus2':
                if card.get_color() not in color2card:
                    color2card[card.get_color()] = []
                color2card[card.get_color()].append(card)

        max_num_cards = 0
        max_color = 0
        for color in color2card:
            if len(color2card[color]) > max_num_cards:
                max_num_cards = len(color2card[color])
                max_color = color
        return max_color

    # count the current deck and reconstruct the color2card dictionary to be a
    # list of cards sorted by number in each color desc
    @staticmethod
    def sort_and_reconstruct_dict(color2card):
        sorted_idx = sorted(color2card.keys(), key=lambda x: len(color2card[x]), reverse=True)
        sorted_list = []
        for color in sorted_idx:
            sorted_list.extend(color2card[color])
        return sorted_list

    # strategically construct the eligible cards
    def strategically_pop(self, eligible_cards, opponent_deck_num, threshold=1):
        color2card = dict()
        pluses = []
        stops = []
        change_colors = []
        # iterate cards and categorize them
        for card in eligible_cards:
            if card.get_type() == 'plus4':
                pluses.append(card)
            elif card.get_type() == 'plus2':
                pluses.append(card)
            elif card.get_type == 'change color':
                change_colors.append(card)
            elif card.get_type == 'stop':
                stops.append(card)
            else:  # normal card
                if card.get_color() not in color2card:
                    color2card[card.get_color()] = []
                color2card[card.get_color()].append(card)

        sorted_eligible_hands = []
        # emergency check: opponent almost winning?
        if opponent_deck_num <= threshold:
            # gives it all the pluses, plus 2 > plus 4
            pluses = sorted(pluses, key=lambda x: int(x.get_type().replace('plus', '')))
            sorted_eligible_hands.extend(pluses)

            # if there's no pluses, give stops
            sorted_eligible_hands.extend(stops)

            # then, colors i have from max to min
            color2card = self.sort_and_reconstruct_dict(color2card)
            sorted_eligible_hands.extend(color2card)

            # otherwise.. let opponent win
            sorted_eligible_hands.extend(change_colors)

        else:
            color2card = self.sort_and_reconstruct_dict(color2card)
            sorted_eligible_hands.extend(color2card)
            sorted_eligible_hands.extend(stops)
            pluses = sorted(pluses, key=lambda x: int(x.get_type().replace('plus', '')))
            sorted_eligible_hands.extend(pluses)
            sorted_eligible_hands.extend(change_colors)

        return sorted_eligible_hands
