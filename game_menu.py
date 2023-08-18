import os
import random
import time
import tkinter as tk

from PIL import ImageTk, Image

from GameObjects.cards import SpecialCard
from GameObjects.player import Bots
from game import Game

# Define the path to the assets directory
image_dir = os.path.join(os.path.dirname(__file__), "assets/PNGs/small")

OPTIONS = [1, 2, 3]


class MenuScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Menu Screen")
        self.clicked = None
        self.img = None
        self.game = None
        self.canv = None
        self.score = 0

        # Create menu widgets
        self.create_widgets()

    def create_widgets(self):
        # Check if canv and frm_buttons widgets already exist, and destroy them if they do.
        if self.canv:
            self.canv.destroy()
            self.frm_buttons.destroy()

        # Create a new canv widget with a white background and place it in row 0, column 0.
        self.canv = tk.Canvas(self.master, width=800, height=800, bg="white")
        self.canv.grid(row=0, column=0)

        # Load and display an image as the background of the canv widget.
        self.img = ImageTk.PhotoImage(Image.open("uno_background.jpg"))
        self.canv.create_image(0, 0, anchor=tk.NW, image=self.img)

        # Create a new frm_buttons widget with a raised relief and 2 pixel border.
        self.frm_buttons = tk.Frame(self.master, relief=tk.RAISED, bd=2)

        # Create a new tk.StringVar object and set it to the first option in the list.
        self.clicked = tk.StringVar()
        self.clicked.set(OPTIONS[0])

        # Create a new tk.Label widget with a message, and place it in the frm_buttons widget.
        bot_label = tk.Label(
            self.frm_buttons, text="Choose how many bots you want to play with:"
        )

        # Create a new tk.OptionMenu widget with options from the OPTIONS list,
        # and place it in the frm_buttons widget.
        drop = tk.OptionMenu(self.frm_buttons, self.clicked, *OPTIONS)

        # Create a new tk.Button widget with a message and command to start the game,
        # and place it in the frm_buttons widget.
        bots = tk.Button(
            self.frm_buttons, text="Start a new game", command=self.start_game
        )

        # Place the frm_buttons widget in row 0, column 1, and make it sticky to the north and south.
        self.frm_buttons.grid(row=0, column=1, sticky="ns")

        # Place the bot_label, drop, and bots widgets in the frm_buttons widget,
        # with appropriate padding and alignment.
        bot_label.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        drop.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        bots.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

    def start_game(self):
        # Create a new game object with the number of bots selected
        self.game = Game(int(self.clicked.get()))
        # Start the game
        self.game.start_game()
        # Update the board game to show the initial state
        self.update_board_game()

    def update_board_game(self, drawed=False):
        # Destroy the canvas frame and buttons frame
        self.canv.destroy()
        self.frm_buttons.destroy()

        # Create a new canvas frame
        self.canv = tk.Canvas(self.master, width=800, height=800, bg="white")
        self.canv.grid(row=0, column=0)

        # Get the image path of the top card on the pile
        image_path = os.path.join(image_dir, self.game.pile.cards[-1].image)

        # Show the player's hand
        player = self.game.get_human_player()
        self.show_hands(player)
        # Show the other players' hands
        self.show_others_hand()

        # Create an ImageTk.PhotoImage object of the top card on the pile
        self.top_pile_card_img = ImageTk.PhotoImage(Image.open(image_path))
        # Show the top card on the pile
        self.canv.create_image(300, 300, anchor=tk.NW, image=self.top_pile_card_img)

        # Create a new frame for the buttons
        self.frm_buttons = tk.Frame(self.master, relief=tk.RAISED, bd=2)

        # Update the window
        self.master.update()

        # Delay for 1 second
        time.sleep(1)
        # Show the play button
        self.play_button(drawed)

    def play_button(self, drawed=False):
        player = self.game.get_human_player()
        self.show_hands(player)
        self.show_others_hand()
        self.card_button = []

        if player.is_playing:
            player_num = self.game.players.index(player) + 1
            print(f"Player {player_num} is playing")
            print(f"Top of the pile is {self.game.pile.cards[-1].name}")

            # Display the buttons for drawing a card and playing a card
            self.frm_buttons.grid(row=0, column=1, sticky="ns")
            player_label = tk.Label(self.frm_buttons, text=f"Player {player_num}")
            if not drawed:
                draw_card = tk.Button(
                    self.frm_buttons,
                    text="Draw a card from the deck",
                    command=lambda: self.draw_card(player),
                )
                draw_card.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
            bot_label = tk.Label(self.frm_buttons, text="Choose a card:")

            player_label.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
            bot_label.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

            # Display the playable cards in the player's hand
            playable_hand = player.playable_hand(self.game.pile, self.game.deck)
            if playable_hand:
                for j, card in enumerate(playable_hand):
                    # Create a callback function for each card button
                    def make_callback(c):
                        return lambda: self.play_a_card(c, player)

                    card_button = tk.Button(
                        self.frm_buttons,
                        text=card.name,
                        command=make_callback(card),
                    )
                    card_button.grid(row=3 + j, column=1, sticky="ew", padx=5, pady=5)
                    self.card_button.append(card_button)
            else:
                # If the player cannot play any cards, end their turn
                if drawed:
                    player.is_playing = False
                    self.end_turn(player)
        else:
            # If it is a bot's turn to play, call the `bot_playing` method
            bot = self.game.get_playing_bot()
            if bot:
                self.bot_playing(bot)

    def draw_card(self, player, drawed=True):
        # Calls the draw_card method from the Game object, passing in the current player as an argument
        self.game.draw_card(player)
        # If drawed is True (the default), call the clear_player_button method with the argument drawed
        if drawed:
            self.clear_player_button(drawed)

    def play_a_card(self, card, player):
        # Set the player's "is_playing" attribute to False
        player.is_playing = False
        # Remove the played card from the player's list of cards
        player.cards.remove(card)
        # Add the played card to the game's pile of cards
        self.game.pile.cards.append(card)
        # Print out the name of the card that was played
        print(f"Card played : {card.name}")
        # If the player has no more cards, print out "WIN !" and call the win method with the index of the player plus one as an argument
        if player.check_win():
            print("WIN !")
            self.win(self.game.players.index(player) + 1)
            return
        # If the played card is a SpecialCard, check what effect it has
        if isinstance(card, SpecialCard):
            # If the card is a wild card, check what effect it has
            if card.color == "wild":
                # If the effect is "color_changer", call the pick_color method with the player as an argument and return
                if card.effect == "color_changer":
                    self.pick_color(player)
                    return
                # If the effect is "pick_four", call the pick_color method with the player and True as arguments (indicating that the card is a wild pick four) and return
                if card.effect == "pick_four":
                    self.pick_color(player, True)
                    return
            # If the played card is not a wild card, check what effect it has
            else:
                # If the effect is "picker", call the picker_effect method from the Game object with the player and 2 as arguments, call the clear_player_button method, and return
                if card.effect == "picker":
                    self.game.picker_effect(player, 2)
                    self.clear_player_button()
                    return
                # If the effect is "skip", call the skip_effect method from the Game object with the player as an argument, call the clear_player_button method, and return
                elif card.effect == "skip":
                    self.game.skip_effect(player)
                    self.clear_player_button()
                    return
                # If the effect is "reverse", call the reverse_effect method from the Game object and return
                elif card.effect == "reverse":
                    self.game.reverse_effect()
        # Call the end_turn method with the player as an argument
        self.end_turn(player)

    def clear_player_button(self, drawed=False):
        # Destroy the frame that holds the player's buttons
        self.frm_buttons.destroy()
        # Create a new frame to hold the player's buttons
        self.frm_buttons = tk.Frame(self.master, relief=tk.RAISED, bd=2)
        # Call the update_board_game method with the drawed argument (defaults to False)
        self.update_board_game(drawed)

    def end_turn(self, player):
        # Call the end_turn method from the Game object with the current player as an argument
        self.game.end_turn(player)
        # Call the clear_player_button method
        self.clear_player_button()

    def picker_effect(self, player, pick_number=2):
        # Print out a message indicating that the next player will draw cards
        print("Next player draw 2 cards")
        # Get the next player in the game
        next_player = self.game.get_next_player(player)
        # For each card that the current player has to draw (defaults to 2), call the draw_card method with the next player and False as arguments (indicating that the clear_player_button method should not be called after drawing the card)
        for i in range(pick_number):
            self.draw_card(next_player, False)
        # Call the skip_effect method with the current player as an argument
        self.skip_effect(player)

    def skip_effect(self, player):
        # Print out a message indicating that the next player is being skipped
        print("Next player get skipped")
        # Set a variable to the current player
        new_player = player
        # Iterate twice to get the player after the next player
        for _ in range(2):
            new_player = self.game.get_next_player(new_player)
        # Set the "is_playing" attribute of the new player to True
        new_player.is_playing = True
        # Call the clear_player_button method
        self.clear_player_button()

    def reverse_effect(self):
        # Print a message indicating that the direction of play is being reversed
        print("Sens is reversed")
        # Reverse the direction of play by multiplying the current direction by -1
        self.game.direction = -self.game.direction

    def pick_color(self, player, picker=False):
        # Create a list of available colors to choose from
        colors = ["red", "green", "blue", "yellow"]
        # If the player is a human player (not a bot), display a message and buttons for the player to choose a color
        if not isinstance(player, Bots):
            print("Pick a color")
            # Destroy the frame that holds the player's buttons
            self.frm_buttons.destroy()
            # Create a new frame to hold the color buttons
            self.frm_buttons = tk.Frame(self.master, relief=tk.RAISED, bd=2)
            self.frm_buttons.grid(row=0, column=1, sticky="ns")
            # For each available color, create a button that calls the change_color method with the chosen color as an argument when clicked
            for i, color in enumerate(["red", "green", "blue", "yellow"]):
                color_button = tk.Button(
                    self.frm_buttons,
                    text=color,
                    command=lambda c=color: self.change_color(c, player, picker),
                )
                color_button.grid(row=2 + i, column=1, sticky="ew", padx=5, pady=5)
        # If the player is a bot, choose a random color and call the change_color method with that color as an argument
        else:
            color = random.choice(colors)
            self.game.change_color(color, player, picker)
            self.end_turn(player)

    def change_color(self, color, player, picker=False):
        # Set the color of the top card in the pile to the chosen color
        self.game.pile.cards[-1].color = color
        # If the "picker" effect is active, call the picker_effect method with the current player and 4 as arguments
        if picker:
            self.picker_effect(player, 4)
        # Otherwise, call the end_turn method with the current player as an argument
        else:
            self.end_turn(player)

    def show_hands(self, player):
        self.card_images = []  # create a list to store the PhotoImage objects
        x_min, x_max = 50, 700
        y = 600
        if len(player.cards):
            card_width = (x_max - x_min) / len(player.cards)
            # Iterate over the list of cards
            for i, card in enumerate(player.cards):
                # Load the card image
                image_path = os.path.join(image_dir, card.image)
                card_image = ImageTk.PhotoImage(Image.open(image_path))

                # Calculate the x-coordinate of the card image
                x = x_min + (i * card_width)

                # Create the card image on the canvas
                self.card_images.append(card_image)
                self.canv.create_image(x, y, anchor=tk.NW, image=card_image)

    def show_others_hand(self):
        self.other_card_images = []  # create a list to store the PhotoImage objects
        other_player = self.game.get_other_player()
        if len(other_player) > 1:
            for i, player in enumerate(other_player):
                if i == 0:
                    self.show_cards(player.cards, 50, 500, 0, True)
                if i == 2:
                    self.show_cards(player.cards, 50, 500, 700, True)
                if i == 1:
                    self.show_cards(player.cards, 75, 625, 0, False)
        else:
            self.show_cards(other_player[0].cards, 75, 625, 0, False)

    def show_cards(self, cards, x_min, x_max, y, orientation):
        # Calculate the width of each card image
        if len(cards):
            card_width = (x_max - x_min) / len(cards)
            new_y = y
            # Iterate over the list of cards
            for i, card in enumerate(cards):
                # Load the card image
                image_path = os.path.join(image_dir, "card_back_alt.png")
                card_image = ImageTk.PhotoImage(Image.open(image_path))

                # Calculate the x-coordinate of the card image
                if orientation:
                    x = y
                    new_y = x_min + (i * card_width)
                    card_image = ImageTk.PhotoImage(Image.open(image_path).rotate(90))
                else:
                    x = x_min + (i * card_width)

                # Create the card image on the canvas
                self.other_card_images.append(card_image)
                self.canv.create_image(x, new_y, anchor=tk.NW, image=card_image)

    def bot_playing(self, bot):
        # Get the card the bot can play from its hand
        card = bot.play_playable_card(self.game.pile, self.game.deck)
        if card:
            # If a card is found, play it
            self.play_a_card(card, bot)
        else:
            # If no playable card is found, draw a card from the deck
            bot.cards.append(self.game.deck.pick())
            # Check again if there is a playable card after drawing
            card = bot.play_playable_card(self.game.pile, self.game.deck)
            if card:
                # If a playable card is found after drawing, play it
                self.play_a_card(card, bot)
            else:
                # If still no playable card is found after drawing, end the bot's turn
                self.end_turn(bot)

    def win(self, winner):
        # Destroy the canvas frame
        self.canv.destroy()  # remove the canvas frame
        self.frm_buttons.destroy()  # remove the button frame

        if winner == self.game.players[0]:
            self.score = 50
        else:
            self.score = -50

        # Create a new canvas and set its size and background color
        self.canv = tk.Canvas(self.master, width=800, height=800, bg="white")
        self.canv.grid(row=0, column=0)

        # Load and set the background image for the canvas
        self.img = ImageTk.PhotoImage(Image.open("uno_background.jpg"))
        self.canv.create_image(0, 0, anchor=tk.NW, image=self.img)

        # Create a new frame for the buttons
        self.frm_buttons = tk.Frame(self.master, relief=tk.RAISED, bd=2)

        # Create a label to display the winner's name
        winner_label = tk.Label(self.frm_buttons, text=f"Player {winner} has won!")

        # Create a button to start a new game, and set its command to 'create_widgets'
        new_game = tk.Button(
            self.frm_buttons, text="Go To Menu", command=self.master.quit
        )


        # Place the button frame in the grid layout, and the label and button inside the frame
        self.frm_buttons.grid(row=0, column=1, sticky="ns")
        winner_label.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        new_game.grid(row=2, column=1, sticky="ew", padx=5, pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    menu = MenuScreen(root)
    root.mainloop()
