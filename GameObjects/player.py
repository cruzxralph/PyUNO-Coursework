import random

from GameObjects.cards import NumberedCard, SpecialCard


class Player:
    # Initializing the class variables for every instance
    def __init__(self):
        self.cards = []
        self.is_playing = False
        self.picked = False
        self.points = 0

    # Method to return a list of playable cards based on the top card in the pile and the cards in the player's hand
    def playable_hand(self, pile, deck):
        pile_card = pile.cards[-1]
        playable_card = []
        for card in self.cards:
            if card.color == pile_card.color or card.color == "wild":
                playable_card.append(card)
            elif isinstance(card, NumberedCard) and isinstance(pile_card, NumberedCard):
                if card.number == pile_card.number:
                    playable_card.append(card)
            elif isinstance(card, SpecialCard) and isinstance(pile_card, SpecialCard):
                if card.effect == pile_card.effect:
                    playable_card.append(card)
        return playable_card

    # Method to play a card at the top of the pile
    def play_playable_card(self, pile, deck):
        pass

    # Method to pick a card from the deck
    def pick_a_card(self, playable_card, deck):
        return None  # Returns 'None' as a placeholder

    # Method to check if the player has won
    def check_win(self):
        if len(self.cards) > 0:
            return False  # Returns 'False' if the player still has cards left
        return True  # Returns 'True' if the player has no cards left


class Bots(Player):
    def play_playable_card(self, pile, deck):
        playable_card = self.playable_hand(pile, deck)
        return self.pick_a_card(playable_card, deck)

    def pick_a_card(self, playable_card, deck):
        if playable_card:
            chosen_card = random.choice(playable_card)
            return chosen_card
