import random

class HumanPlayer(object):
    def __init__(self):
        self.hand = []
        self.point_cards = []
        self.effect_cards = []
        self.score = 0
        self.to_win = 21
    
    def take_turn(self):
        if len(self.hand) > 0:
            return random.choice([["draw", -1],
                                  ["point", random.choice(self.hand)],
                                  ["one", random.choice(self.hand)],
                                  ["perm", random.choice(self.hand)]])
        else:
            return ["draw", -1]

    def draw_card(self, deck, error):
        if len(deck) == 0:
            print("Error, go again.")
            error[0] = "Error"
        else:
            self.hand.append(deck.pop())

    def point(self, card, error):
        if card % 13 <= 10 and card % 13 >=1:
            self.hand.remove(card)
            self.point_cards.append(card)
        else:
            print("Error, go again.")
            error[0] = "Error"

    def permanent(self, card, error):
        if card % 13 >= 11 or card % 13 == 8 or  card % 13 == 0:
            self.hand.remove(card)
            self.effect_cards.append(card)
        else:
            print("Error, go again.")
            error[0] = "Error"

    def one_off(self, card, error):
        if (card % 13 <= 7 and card % 13 >= 1) or card % 13 == 9:
            self.hand.remove(card)
        else:
            print("Error, go again.")
            error[0] = "Error"

    def discard_points(self):
        temp = self.point_cards
        self.point_cards = []
        return temp

    def discard_effect(self):
        self.to_win = 21
        temp = self.effect_cards
        self.effect_cards = []
        return temp

    def king(self):
        self.to_win = self.to_win - 4

class Board:
    players = [HumanPlayer(), HumanPlayer()]
    deck = []
    discard = []
    
    def print_board(self):
        print("Player 1, Score: " + str(self.players[0].score) + "/" + str(self.players[0].to_win))
        print(self.convert_cards(self.players[0].point_cards))
        print(self.convert_cards(self.players[0].effect_cards))
        print(self.convert_cards(self.players[0].hand))
        print("Player 2, Score: " + str(self.players[1].score) + "/" + str(self.players[1].to_win))
        print(self.convert_cards(self.players[1].point_cards))
        print(self.convert_cards(self.players[1].effect_cards))
        print(self.convert_cards(self.players[1].hand))
        print("Discard:")
        print(self.convert_cards(self.discard))
        print()
        print()

    def convert_card(self, card):
        value = str(card % 13)
        suit_num = card / 13

        if value == "11":
            value = "Jack"
        if value == "12":
            value = "Queen"
        if value == "0":
            value = "King"
        if value == "1":
            value = "Ace"

        suit = "Hearts"
        if suit_num <= 1:
            suit = "Clubs"
        elif suit_num <= 2:
            suit = "Diamonds"
        elif suit_num <= 3:
            suit = "Spades"

        if card == -1:
            return "NaC"
        else:
            return value + " of " + suit

    def convert_cards(self, cards):
        converted = list(cards)
        j = 0
        for i in cards:
            converted[j] = self.convert_card(i)
            j += 1
        return converted

    def effect(self, card, turn):
        error = [""]
        if card % 13 == 1:
            self.players[0].score = 0
            self.players[1].score = 0
            self.discard += self.players[0].discard_points() + self.players[1].discard_points()
        elif card % 13 == 3:
            self.players[turn].draw_card(self.discard, error)
        elif card % 13 == 5:
            self.players[turn].draw_card(self.deck, error)
            self.players[turn].draw_card(self.deck, error)
        elif card % 13 == 6:
            self.discard += self.players[0].discard_effect() + self.players[1].discard_effect()
        else:
            self.players[0].score = 0
            self.players[1].score = 0
            self.discard += self.players[0].discard_points() + self.players[1].discard_points()

    def permanent_effect(self, card, turn):
        error = [""]
        if card % 13 == 0:
            self.players[turn].king()
        else:
            pass

    def run_game(self):
        deck = list(range(1,53))
        random.shuffle(deck)

        turn = 0
        while self.players[0].score < self.players[0].to_win and self.players[1].score < self.players[1].to_win:
            decision = self.players[turn].take_turn()

            print(turn)
            print([decision[0], self.convert_card(decision[1])])
            print()
            #self.players[turn].score += 1

            error = ["No Error"]
            if decision[0] == "draw":
                self.players[turn].draw_card(deck, error)
            elif decision[0] == "point":
                self.players[turn].point(decision[1], error)
                if error[0] == "No Error":
                    self.players[turn].score += decision[1] % 13
            elif decision[0] == "one":
                self.players[turn].one_off(decision[1], error)
                if error[0] == "No Error":
                    self.effect(decision[1], turn)
            elif decision[0] == "perm":
                self.players[turn].permanent(decision[1], error)
                if error[0] == "No Error":
                    self.permanent_effect(decision[1], turn)
                

            if error[0] == "Error":
                continue
            else:
                if turn == 0:
                    turn = 1
                elif turn == 1:
                    turn = 0
            self.print_board()

            if len(deck) == 0:
                print("Done, yo!")
                break

x = Board()
x.run_game()
