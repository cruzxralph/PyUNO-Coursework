import random

# Importing classes from another module
from GameObjects.cards import NumberedCard, SpecialCard


# A class representing a deck of cards
class Deck:
    def __init__(self):
        self.cards = []  # A list to store the cards in the deck

    # A method to initialize the deck with all the cards
    def initialize(self):
        # Looping through each color in the deck
        for color in ["blue", "green", "red", "yellow"]:
            # Looping through each number from 0 to 8 for each color
            for i in range(9):
                # Adding two of each numbered card to the deck, except for 0
                self.cards.append(NumberedCard(color, i))
                if i > 0:
                    self.cards.append(NumberedCard(color, i))
            # Adding two of each special card (skip, reverse, and picker) to the deck for each color
            for _ in range(2):
                self.cards.append(SpecialCard("skip", color))
                self.cards.append(SpecialCard("reverse", color))
                self.cards.append(SpecialCard("picker", color))
        # Adding four of each wild card (color changer and pick four) to the deck
        for _ in range(4):
            self.cards.append(SpecialCard("color_changer", "wild"))
            self.cards.append(SpecialCard("pick_four", "wild"))
        self.shuffle()  # Shuffling the deck after it has been initialized

    # A method to shuffle the cards in the deck
    def shuffle(self):
        random.shuffle(self.cards)

    # A method to pick a card from the deck
    def pick(self):
        try:
            # Removing and returning the last card in the list (which represents the top of the deck)
            return self.cards.pop()
        except IndexError:
            return None
