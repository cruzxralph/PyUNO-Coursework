from GameObjects.deck import Deck
from GameObjects.player import Player, Bots


class Game:
    def __init__(self, num_bots):
        self.players = []
        self.deck = Deck()
        self.deck.initialize()
        self.turn = 0
        self.pile = Deck()
        self.direction = 1
        self.num_bots = num_bots

    def start_game(self):
        # Create a human player and add 7 cards to their hand
        self.players.append(Player())
        for _ in range(7):
            self.players[-1].cards.append(self.deck.pick())

        # Create bot players and add 7 cards to each of their hands
        for i in range(self.num_bots):
            self.players.append(Bots())
            for _ in range(7):
                self.players[-1].cards.append(self.deck.pick())

        # Pick a card from the deck to start the pile
        self.pile.cards.append(self.deck.pick())

        # Return the player who is currently playing
        self.players[0].is_playing = True

    def get_playing_player(self):
        # Return the player who is currently playing
        for player in self.players:
            if player.is_playing:
                return player

    def get_human_player(self):
        # Return the human player
        for player in self.players:
            if isinstance(player, Player):
                return player

    def check_win(self, player):
        # Check if a player has won by running out of cards
        print(len(player.cards))
        if len(player.cards) > 0:
            return False
        return True

    def get_index_player(self, player):
        # Get the index of a player
        return self.players.index(player) + 1

    def get_playing_bot(self):
        # Return the bot player who is currently playing
        for player in self.players:
            if player.is_playing and isinstance(player, Bots):
                return player

    def bot_playing(self, bot):
        # Let a bot play a card or draw a card if it can't play
        card = bot.play_playable_card(self.pile, self.deck)
        if card:
            self.play_a_card(card, bot)
        else:
            new_card = self.deck.pick()
            if new_card is None:
                self.refill_deck()
                new_card = self.deck.pick()
            bot.cards.append(new_card)
            card = bot.play_playable_card(self.pile, self.deck)
            if card:
                self.play_a_card(card, bot)
            else:
                self.end_turn(bot)

    def end_turn(self, player):
        # End a player's turn and move on to the next player
        player.is_playing = False
        next_player = self.get_next_player(player)
        next_player.is_playing = True

    def draw_card(self, player):
        # Draw a card from the deck and add it to a player's hand
        new_card = self.deck.pick()
        if new_card is None:
            self.refill_deck()
            new_card = self.deck.pick()
        player.cards.append(new_card)
        print(
            f"The player {self.get_index_player(player)} is drawing a {new_card.name}"
        )
        return new_card

    def play_a_card(self, card, player):
        # Remove a card from a player's hand and add it to the pile of played cards
        player.cards.remove(card)
        self.pile.cards.append(card)

    def get_other_player(self):
        # Return a list of all bot players
        other_player = []
        for player in self.players:
            if isinstance(player, Bots):
                other_player.append(player)
        return other_player

    def get_next_player(self, player):
        # Determine the next player in the game based on the current player and the game direction
        index = self.players.index(player) + self.direction
        if index == len(self.players):
            return self.players[0]
        elif index < 0:
            return self.players[-1]
        return self.players[index]

    def picker_effect(self, player, pick_number=2):
        # Apply the "picker" effect, which requires the next player to draw 2 cards
        print("Next player draw 2 cards")
        next_player = self.get_next_player(player)
        for i in range(pick_number):
            self.draw_card(next_player)
        self.skip_effect(player)

    def skip_effect(self, player):
        # Skip the turn of the next player
        print("Next player get skipped")
        new_player = player
        for _ in range(2):
            new_player = self.get_next_player(new_player)
        new_player.is_playing = True

    def change_color(self, color, player, picker=False):
        # Change the color of the top card on the pile to the specified color, and apply the "picker" effect if necessary
        self.pile.cards[-1].color = color
        if picker:
            self.picker_effect(player, 4)

    def reverse_effect(self):
        # Reverse the direction of the game
        print("Direction is reversed")
        self.direction = -self.direction

    def refill_deck(self):
        top_of_pile = self.pile.cards.pop()
        for card in self.pile.cards:
            self.deck.cards.append(card)
        self.deck.shuffle()
        self.pile.cards.clear()
        self.pile.cards.append(top_of_pile)