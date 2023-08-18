# A class representing a generic card
class Card:
    def __init__(self, color=None):
        # Initializing instance variables
        self.name = ""  # A string representing the name of the card
        self.image = ""  # A string representing the name of the image file for the card
        self.color = color  # A string representing the color of the card (optional)
        self.get_name()  # A method to set the name of the card
        self.get_image()  # A method to set the image of the card
        self.is_playable = False  # A boolean indicating whether the card is playable

    # A method to set the image file name of the card based on its name
    def get_image(self):
        self.image = f"{self.name}.png"

    def get_name(self):
        pass  # A method to be overridden by subclasses that sets the name of the card

    def show(self):
        pass  # A method to be overridden by subclasses that displays information about the card


# A subclass of Card representing a special card with a specific effect
class SpecialCard(Card):
    def __init__(self, effect, color=None):
        # Initializing instance variables
        self.effect = effect  # A string representing the effect of the special card
        super().__init__(color)  # Calling the superclass constructor to set the name and image of the card

    # A method to set the name of the special card based on its color and effect
    def get_name(self):
        self.name = f"{self.color}_{self.effect}"


# A subclass of Card representing a numbered card with a specific color and number
class NumberedCard(Card):
    def __init__(self, color, number):
        # Initializing instance variables
        self.number = number  # An integer representing the number on the numbered card
        super().__init__(color)  # Calling the superclass constructor to set the name and image of the card

    # A method to set the name of the numbered card based on its color and number
    def get_name(self):
        self.name = f"{self.color}_{self.number}"
