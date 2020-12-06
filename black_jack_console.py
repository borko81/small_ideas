import random


class Card:

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.suit} {self.value}"


class Deck:

    def __init__(self):
        self.cards = [
            Card(k, v) for k in
            ["Spades", "Clubs", "Hearts", "Diamonds"] for v in
            ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        ]

    def shuffle(self):
        if len(self.cards) > 0:
            random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop(0)


class Hand:

    def __init__(self, dealer=False):
        self.dealer = dealer
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        self.value = 0
        has_ace = False
        for c in self.cards:
            if c.value.isnumeric():
                self.value += int(c.value)
            else:
                if c.value == 'A':
                    has_ace = True
                    self.value += 11
                else:
                    self.value += 10

        if has_ace and self.value > 21:
            self.value -= 10

    def get_value(self):
        self.calculate_value()
        return self.value

    def display(self):
        if self.dealer:
            print("Dilar")
            for c in self.cards:
                print(c)
            print(f"Result: {self.get_value()}")
        else:
            for c in self.cards:
                print(c)
            print(f"Result: {self.get_value()}")


class Game:
    def __init__(self):
        playing = True
        self.gemeover = False

        while playing:
            self.deck = Deck()
            self.deck.shuffle()

            self.player_hand = Hand()
            self.dealer_hand = Hand(dealer=True)

            for _ in range(2):
                self.player_hand.add_card(self.deck.deal())
                self.dealer_hand.add_card(self.deck.deal())

            print("Your hand is :")
            self.player_hand.display()
            print()
            print("Dealer hand is :")
            self.dealer_hand.display()
            print()

            
            while not self.gemeover:
                player_has_black, dealar_has_black = self.check_for_blackjack()
                if player_has_black or dealar_has_black:
                    self.gemeover = True
                    self.showblackjack(player_has_black, dealar_has_black)
                else:
                    continue
            if self.gemeover:
                break


    def check_for_blackjack(self):
        player = False
        dealer = False
        if self.player_hand.get_value() == 21:
            player = True
        if self.dealer_hand.get_value() == 21:
            dealer == True

        return player, dealer

    def showblackjack(self, player_has_black, dealar_has_black):
        if player_has_black and dealar_has_black:
            print("Both has blackjack")
        elif player_has_black:
            print("Player win")
        elif dealar_has_black:
            print("Dealer win")


if __name__ == '__main__':
    test = Game()
