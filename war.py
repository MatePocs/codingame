import sys
import math

debugging = True

class Card:

    def __init__(self, card_string):
        self.number = card_string[:-1]
        self.suit = card_string[-1]
        self.value = self.card_value(self.number)
    
    def card_value(self, card_number):
        """
        input: string, output: number from 2 to 14
        """
        if card_number[0].isdigit():
            return int(card_number)
        else:
            if card_number == 'J':
                return 11
            elif card_number == 'Q':
                return 12
            elif card_number == 'K':
                return 13
            elif card_number == 'A':
                return 14
            else:
                return 0

class PlayerDeck:

    def __init__(self, player_name):
        self.cards_in_hand = []
        self.cards_in_pile = []
        self.player_name = player_name

    def add_card_to_end(self, cards_to_modify, card_to_add):
        cards_to_modify.append(card_to_add)

    def remove_card_from_start(self, cards_to_modify):
        cards_to_modify.pop(0)

    def cards_count(self):
        return len(self.cards_in_hand)

    def move_cards_between_lists(self, number_of_cards, source, target):
        for i in range(0, number_of_cards):
            card = source[0]
            target.append(card)
            source.pop(0)

    def move_cards_from_hand_to_pile(self, number_of_cards):
        self.move_cards_between_lists(number_of_cards, self.cards_in_hand, self.cards_in_pile)

    def clear_pile(self):
        self.cards_in_pile = []

class FightHandler:

    def __init__(self):
        pass

    def battle(self, deck_1, deck_2):

        """
        inputs are PlayerDeck objects
        output is also a PlayerDeck
        """

        # moves the cards to the pile
        card_1 = deck_1.cards_in_hand[0]
        card_2 = deck_2.cards_in_hand[0]

        for deck in [deck_1, deck_2]:
            card = deck.cards_in_hand[0]
            deck.remove_card_from_start(deck.cards_in_hand)
            deck.add_card_to_end(deck.cards_in_pile, card)   

        winner = None
        loser = None

        # decides the winner
        if card_1.value > card_2.value:
            winner = deck_1
            loser = deck_2
        elif card_1.value < card_2.value:
            winner = deck_2
            loser = deck_1

        return winner, loser

    def war(self, deck_1, deck_2):
        """
        moves 3 cards from both deck's hand to pile
        if any player runs out, returns 'PAT'
        """

        result = None

        # if there is a war, first need to take 3 cards, and then do a battle, otherwise it's a draw

        if len(deck_1.cards_in_hand) < 4 or len(deck_2.cards_in_hand) < 4:
            result = 'PAT'
        else:
            deck_1.move_cards_from_hand_to_pile(3)
            deck_2.move_cards_from_hand_to_pile(3)

        return result


    def handle_battle_consquence(self, winner, loser):

        if winner is not None:
            self.handle_winning(winner, p1_deck, p2_deck)
            return 'new_round'

        else:
            # if there was no winner, do one war
            result = self.war(p1_deck, p2_deck)
            if result is not None:
                return result
            else:
                return 'new_round'

    def handle_winning(self, winner, first_deck_to_handle, second_deck_to_handle):
        """
        winner gets all the cards in the pile, 
        starting with the first player's pile
        """

        for card in first_deck_to_handle.cards_in_pile:
            winner.add_card_to_end(winner.cards_in_hand, card)
            first_deck_to_handle.clear_pile()

        for card in second_deck_to_handle.cards_in_pile:
            winner.add_card_to_end(winner.cards_in_hand, card)
            second_deck_to_handle.clear_pile()

    def winner_of_game(self, deck_1, deck_2):
        """
        checks if there is a winner in the game
        this is checked at the end of round, if one player has 0 cards
        """
        game_winner = None

        if deck_1.cards_count() == 0:
            game_winner = deck_2.player_name
        elif deck_2.cards_count() == 0:
            game_winner = deck_1.player_name

        return game_winner
        
# INITIAL DATA

p1_deck = PlayerDeck('1')
p2_deck = PlayerDeck('2')

n = int(input())  # the number of cards for player 1
for i in range(n):
    cardp_1 = input()  # the n cards of player 1
    card = Card(cardp_1)
    p1_deck.add_card_to_end(p1_deck.cards_in_hand, card)
m = int(input())  # the number of cards for player 2
for i in range(m):
    cardp_2 = input()  # the m cards of player 2
    card = Card(cardp_2)
    p2_deck.add_card_to_end(p2_deck.cards_in_hand, card)


fighthandler = FightHandler()
number_of_rounds = 0
game_over = False

def debug_print():

    if debugging: 
        cards = ''
        print('Round ' + str(number_of_rounds), file = sys.stderr)
        print('Player1 Deck :',  file = sys.stderr)
        for card in p1_deck.cards_in_hand:
            cards = cards + card.number + card.suit + ' '
        print(cards,  file = sys.stderr)
        cards = ''
        print('Player2 Deck :',  file = sys.stderr)
        for card in p2_deck.cards_in_hand:
            cards = cards + card.number + card.suit + ' '
        print(cards,  file = sys.stderr)

while not game_over:

    debug_print()

    # play a round of battle
    winner, loser = fighthandler.battle(p1_deck, p2_deck)

    # if we had a winner, increase rounds
    if winner is not None:
        number_of_rounds += 1

    # either someone won, or it's a draw which means war
    result = fighthandler.handle_battle_consquence(winner, loser)

    # result is one potential PAT, if we had to do a war

    if result == 'PAT':
        game_winner = 'PAT'
    else:
        game_winner = fighthandler.winner_of_game(p1_deck, p2_deck)

    if game_winner is not None:
        game_over = True



# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr)

if game_winner == 'PAT':
    game_result = 'PAT'
else:
    game_result = game_winner + ' ' + str(number_of_rounds)

print(game_result)