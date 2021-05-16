from card import UnoCard
from random import randint, choice

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
    
    def check_color(self, card_to_pop):
        if card_to_pop.get_type() == 'change color' or card_to_pop.get_type() == 'plus4':
            # TODO: change to a color that the player has
            card_to_pop.color = 0
        return card_to_pop

    def play(self, last_card=None, last_color=None):
        # sanity check
        assert len(self.cards) > 0
        if last_color is None:
            assert last_card is None

        if last_card is None:
            # At the beginning of the game
            if last_color is None:
                # TODO: change randint to choice
                card = self.cards.pop(randint(0, len(self.cards) - 1))
                card = self.check_color(card)
                return card
            # last card is None, so the last player does not play a card but color is fixed
            # in this case, the player who played 'stop' can play another stop of different color
            else:
                eligible_cards = set()
                for card in self.cards:
                    if card.get_type() == 'plus4' or card.get_type() == 'change color':
                        eligible_cards.add(card)
                    elif card.get_color() == last_color:
                        eligible_cards.add(card)

                eligible_cards = list(eligible_cards)
                print("m1")
                print(str([str(x) for x in eligible_cards]))

                if len(eligible_cards) == 0:
                    return None
                
                card_to_pop = eligible_cards[randint(0, len(eligible_cards) - 1)]
                self.cards.remove(card_to_pop)

                card_to_pop = self.check_color(card_to_pop)
                return card_to_pop
        
        # middle of the game
        # case 1: stop for one round
        if last_card.get_type() == 'stop':
            return None

        eligible_cards = set()
        print(last_card)
        # functional and non-functional cards:
        for card in self.cards:
            # if last card is a normal card
            if not last_card.is_functional():
                # the card to play must have
                if card.is_functional():
                    if (card.get_type() != 'stop' and card.get_type() != 'plus2') or card.get_color() == last_card.get_color():
                        eligible_cards.add(card)
                elif last_card.get_color() == card.get_color() or last_card.get_number() == card.get_number():
                    eligible_cards.add(card)
            else:
                if card.get_type() == 'plus4':
                    eligible_cards.add(card)
                if last_card.get_type() == 'plus2':
                    if card.get_type() == 'plus2':
                        eligible_cards.add(card)
                if last_card.get_type() == 'change color':
                    if card.get_type() == 'change color':
                        eligible_cards.add(card)
        eligible_cards = list(eligible_cards)
        print("m2")
        print(str([str(x) for x in eligible_cards]))

        if len(eligible_cards) == 0:
                return None

        card_to_pop = eligible_cards[randint(0, len(eligible_cards) - 1)]
        self.cards.remove(card_to_pop)

        card_to_pop = self.check_color(card_to_pop)
        return card_to_pop
                
            
            