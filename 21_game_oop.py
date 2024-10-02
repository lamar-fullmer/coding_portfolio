import random
import os

def clear_screen():
    os.system('clear')

class Cards:
    SUITS = ['Heart', 'Club', 'Diamond', 'Spade']
    RANK = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'Jack': 10,
        'Queen': 10,
        'King': 10,
        'Ace': 11,
    }

    def __init__(self):
        self.deck = []
        self.reset()

    def reset(self):
        deck = []
        for suit in Cards.SUITS:
            for rank in Cards.RANK:
                deck.append((rank, suit))

        random.shuffle(deck)

        self.deck = deck
    
    def deal(self):
        card1 = self.deck.pop()
        card2 = self.deck.pop()
        return [card1, card2] 

class Participant:
    def __init__(self):
        self.money = 5

    def hit(self, deck):
        return deck.pop()

    def is_busted(self, score):
        if score > 21:
            return True
        return False
    
    def score(self, cards):
        total = 0
        all_card_values = []

        for card in cards:
            value = self.calculate_one_card(card)
            all_card_values.append(value)
            total += value
        
        for card in all_card_values:
            if total > 21:
                if card == 11:
                    total -= 10

        return total

    def calculate_one_card(self, card):
        rank = card[0].split()
        card_face = rank[0]
        value = Cards.RANK[card_face]   
        return value

class TwentyOneGame:
    def __init__(self):
        # STUB
        # What attributes does the game need? A deck? Two
        # participants?
        self.cards = Cards()
        self.player = Participant()
        self.dealer = Participant()

    def start(self):
        while True:
            clear_screen()
            self.display_welcome_message()

            while True:
                self.cards.reset()
                player_cards = self.cards.deal()
                dealer_cards = self.cards.deal()
                self.player_turn(player_cards, dealer_cards)
                self.dealer_turn(player_cards, dealer_cards)
                self.display_result(player_cards, dealer_cards)
                print()
                input("When you're ready, press Enter to continue")

                if self.player.money == 10 or self.dealer.money == 10:
                    break
            
            self.display_money_results()

            if self.play_again() == 'y':
                self.reset_game()
            else:
                break

        self.display_goodbye_message()

    def show_player_turn_board(self, player_cards, dealer_cards):
        player_score = self.player.score(player_cards)
        dealer_card1 = [dealer_cards[0]]
        print(dealer_card1)
        dealer_score = self.player.score(dealer_card1)

        clear_screen()

        print(f"Your cards:")
        for cards in player_cards:
            print(f"[{cards[0]} of {cards[1]}]")
        print()
        print(f"Your score:   {player_score}")
        print()

        print("Dealer's Cards:")
        print(f"[{dealer_card1[0][0]} of {dealer_card1[0][1]}]")
        print(f"['Hidden Card...]")
        print()
        print(f"Dealer's score: {dealer_score}")
        print()

    def show_dealer_turn_board(self, player_cards, dealer_cards):
        player_score = self.player.score(player_cards)
        dealer_score = self.dealer.score(dealer_cards)

        clear_screen()

        print(f"Your cards:")
        for cards in player_cards:
            print(f"[{cards[0]} of {cards[1]}]")
        print()
        print(f"Your score:   {player_score}")
        print()

        print("Dealer's Cards:")
        for cards in dealer_cards:
            print(f"[{cards[0]} of {cards[1]}]")
        print()
        print(f"Dealer's score: {dealer_score}")
        print()

    def player_turn(self, player_cards, dealer_cards):
        self.show_player_turn_board(player_cards, dealer_cards)
        score = self.player.score(player_cards)

        while score < 21:
            while True:
                try:
                    choice = input("Do you wanna hit or stay? (h/s): ").lower()
                    if choice in ['h', 's']:
                        break
                except ValueError:
                    pass
                print("Sorry, that's not a valid choice")

            if choice == 'h':
                drawn_card = self.player.hit(self.cards.deck)
                player_cards.append(drawn_card)
                self.show_player_turn_board(player_cards, dealer_cards)

                score = self.player.score(player_cards)

            else:
                self.show_player_turn_board(player_cards, dealer_cards)
                break
        
    def dealer_turn(self, player_cards, dealer_cards):
        self.show_dealer_turn_board(player_cards, dealer_cards)
        score = self.dealer.score(dealer_cards)
        player_score = self.player.score(player_cards)

        if player_score > 21:
            return None

        while True:
            if score >= 17:
                self.show_dealer_turn_board(player_cards, dealer_cards)
                break

            if score < 17:
                drawn_card = self.dealer.hit(self.cards.deck)
                dealer_cards.append(drawn_card)
                self.show_dealer_turn_board(player_cards, dealer_cards)

                score = self.dealer.score(dealer_cards)

    def display_welcome_message(self):
        print()
        print("Hi, welcome to 21!")
        print()
        print()
        print("The Rules:")
        print()
        print("It's the same rules at BlackJack.")
        print()
        print("Try to get the highest score without going over 21 points.")
        print()
        print("You will start the game with $5.")
        print()
        print("Each round you will bet $1. Winner receives all the money.")
        print()
        print("The game ends when someone runs out of money")
        print()
        print("Good luck!")
        print()
        print()
        input("Press Enter when you are ready to begin the game ")

    def display_goodbye_message(self):
        clear_screen()
        print("Thanks for playing!")
    
    def display_money_results(self):
        clear_screen()
        if self.player.money == 10:
            print("You have $10 and took all the dealer's money. Congrats!")
        if self.dealer.money == 10:
            print("You have $0 and can't play anymore. What a loser! ")
        print()
    
    def dealer_won_money(self):
        self.dealer.money += 1
        self.player.money -= 1
    
    def player_won_money(self):
        self.dealer.money -= 1
        self.player.money += 1
    
    def print_money_score(self):
        print(f'Your money:     ${self.player.money}')
        print(f"Dealer's money: ${self.dealer.money}")

    def display_result(self, player_cards, dealer_cards):
        player_score = self.player.score(player_cards)
        dealer_score = self.dealer.score(dealer_cards)
        
        if player_score > 21:
            self.show_dealer_turn_board(player_cards, dealer_cards)
            self.dealer_won_money()
            print()
            print('You busted. The dealer won.')
            print()
            self.print_money_score()
        elif dealer_score > 21:
            self.show_dealer_turn_board(player_cards, dealer_cards)
            self.player_won_money()
            print()
            print('Dealer busted. You won!')
            print()
            self.print_money_score()
        elif dealer_score > player_score:
            self.show_dealer_turn_board(player_cards, dealer_cards)
            self.dealer_won_money()
            print()
            print('Dealer won...')
            print()
            self.print_money_score()
        elif dealer_score < player_score:
            self.show_dealer_turn_board(player_cards, dealer_cards)
            self.player_won_money()
            print()
            print('You won!')
            print()
            self.print_money_score()
        else:
            self.show_dealer_turn_board(player_cards, dealer_cards)
            print()
            print('It was a tie. How boring...')
            print()
            self.print_money_score()

    def play_again(self):
        while True:
            choice = input("Do you want to play again (y/n)? ").lower()
            try:
                if choice in ['y', 'n']:
                    break
            except ValueError:
                pass
            print()
            print("Sorry that's not a valid choice")
            print()

        return choice
    
    def reset_game(self):
        self.player = Participant()
        self.dealer = Participant()

game = TwentyOneGame()
game.start()
