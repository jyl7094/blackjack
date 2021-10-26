from random import shuffle

class Card:
    _values = {'Ace': 11, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 
               'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 
               'King': 10}
    def __init__(self, suit, rank):
        self._suit = suit
        self._rank = rank
        self._value = Card._values[self._rank]
        
    def __str__(self):
        return f'{self._rank} of {self._suit}'
    
    def get_value(self):
        return self._value
    
    def set_value(self, value):
        self._value = value

class Deck:
    _suits = ('Clubs', 'Diamonds', 'Hearts', 'Spades')
    _ranks = ('Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 
              'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King')
    def __init__(self):
        self._cards = []
        for suit in Deck._suits:
            for rank in Deck._ranks:
                self._cards.append(Card(suit, rank))
        shuffle(self._cards)
    
    def remove_top(self):
        return self._cards.pop()

class CardPlayer:
    def __init__(self):
        self._hands = []
        
    def draw(self, card):
        self._hands.append(card)
    
    def print_details(self):
        raise NotImplementedError('Warning: print_cards() not implemented.')
    
    def get_values(self):
        values = 0
        for card in self._hands:
            values += card.get_value()
        return values
    
    def get_hands(self):
        return self._hands
    
    def has_ace(self):
        for card in self._hands:
            if card.get_value() == 11:
                return True
        return False
    
    def change_ace(self):
        for card in self._hands:
            if card.get_value() == 11:
                card.set_value(1)
        print('Ace\'s value has been changed from 11 to 1!')

class Player(CardPlayer):
    def __init__(self, chips):
        self._hands = []
        self._chips = chips
    
    def get_chips(self):
        return self._chips
    
    def print_details(self):
        print('Player\'s hands: ' + ', '.join(map(str, self._hands)))
        print(f'Player\'s hands\' value: {self.get_values()}')
    
    def set_chips(self, chips):
        self._chips = chips
    
    def return_cards(self):
        self._hands = []

class Dealer(CardPlayer):
    def print_details(self, reveal):
        if reveal:
            print('Dealer\'s hands: ' + ', '.join(map(str, self._hands)))
            print(f'Dealer\'s hands\' value: {self.get_values()}')
        else:
            print(f'Dealer\'s hands: {self._hands[0]} and a HIDDEN CARD')
            print(f'Dealer\'s hands\' value: {self._hands[0].get_value()} plus HIDDEN VALUE')

def set_chips():
    while True:
        try:
            chips = int(input('>> Enter the number of chips to start with: '))
            if chips <= 0:
                raise
            return chips
        except:
            print('Warning: Invalid input.')
            continue
            
def set_bet():
    while True:
        try:
            bet = int(input('>> Enter the number of chips to bet: '))
            return bet
        except:
            print('Warning: Invalid input.')

def set_choice():
    while True:
        try:
            choice = input('>> Enter \'H\' or \'h\' to \'Hit\', or \'S\' or \'s\' to \'Stay\': ').upper()
            if choice == 'H' or choice == 'S':
                return choice
            else:
                raise
        except:
            print('Warning: Invalid input.')

def check_winner(player, dealer):
    winner = ''
    if player.get_values() > 21:
        winner = 'Dealer'
    elif player.get_values() == 21 and dealer.get_values() == 21:
        winner = 'Draw'
    elif dealer.get_values() > 21:
        winner = 'Player'
    else:
        if player.get_values() > dealer.get_values():
            winner = 'Player'
        elif player.get_values() == dealer.get_values():
            winner = 'Draw'
        else:
            winner = 'Dealer'
    
    return winner
    

def main():
    play = True
    rounds = 1
    player = Player(set_chips())
    while play:
        player.return_cards()
        deck = Deck()
        dealer = Dealer()
        
        print(f'---------------------------------------- Round {rounds} ----------------------------------------')
        print(f'Current number of chips: {player.get_chips()}')
        
        if player.get_chips() <= 0:
            print('Insufficient number of chips to play. Goodbye!')
            print(f'-------------------------------------- Round {rounds} End --------------------------------------')
            break
        
        while True:
            bet = set_bet()
            if bet > player.get_chips() or bet <= 0:
                print('Warning: Invalid input.')
                continue
            else:
                break
        
        player.set_chips(player.get_chips() - bet)
        
        for drawing in range(0, 2):
            player.draw(deck.remove_top())
            dealer.draw(deck.remove_top())
        
        reveal = False 
        players_turn = dealers_turn = True
        
        while players_turn:
            print('Player\'s turn:')
            dealer.print_details(reveal)
            player.print_details()
            if player.get_values() == 21:
                players_turn = False
            elif player.get_values() > 21:
                if player.has_ace():
                    player.change_ace()
                else:
                    players_turn = False
                    dealers_turn = False
            else:
                choice = set_choice()
                if choice == 'H':
                    print('Player chooses to hit...')
                    player.draw(deck.remove_top())
                elif choice == 'S':
                    print('Player chooses to stand...')
                    players_turn = False
                else:
                    print('Warning: Invalid input.')
        
        reveal = True
        while dealers_turn:
            print('Dealer\'s turn:')
            dealer.print_details(reveal)
            player.print_details()
            if dealer.get_values() == 21:
                dealers_turn = False
            elif dealer.get_values() > 21:
                if dealer.has_ace():
                    dealer.change_ace()
                else:
                    dealers_turn = False
            else:
                if dealer.get_values() < 17:
                    print('Dealer chooses to hit...')
                    dealer.draw(deck.remove_top())
                else:
                    print('Dealer chooses to stand...')
                    dealers_turn = False
                    
        winner = check_winner(player, dealer)
        print('Table Result:')
        dealer.print_details(reveal)
        player.print_details()
        if winner == 'Player':
            print('Player has won this round!')
            player.set_chips(player.get_chips() + int(bet * 1.5))
        elif winner == 'Dealer':
            print('Dealer has won this round!')
        else:
            print('There\'s no winner this round.')
        
        if player.get_chips() <= 0:
            print('Insufficient number of chips to play. Goodbye!')
            print(f'-------------------------------------- Round {rounds} End --------------------------------------')
            break
        
        while True:
            option = input('>> Enter \'Y\' or \'y\' to keep playing, or \'N\' or \'n\' to exit: ').upper()
            if option == 'Y':
                break
            elif option == 'N':
                play = False
                print('Thank you for playing. Goodbye!')
                break
            else:
                print('Warning: Invalid input.')
        
        print(f'-------------------------------------- Round {rounds} End --------------------------------------')
        rounds += 1

if __name__ == '__main__':
    main()
