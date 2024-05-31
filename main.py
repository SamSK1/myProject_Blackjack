from math import *
import random

class Card:
    def __init__(self,suit,value,name):
        self.suit=suit
        self.value=value
        self.name=name
    def __str__(self):
        return self.name+" of "+self.suit+' value: '+str(self.value)


class Deck:
    def __init__(self):
        self.deck=[]
        
    def get_deck(self):
        card_name=""
        for suits in ['Hearts','Diamonds','Spades','Clubs']:
            
            for value in range(2,15):
                card_value=value
                card_name=str(value)
                if value==11:
                    card_value=10
                    card_name='Jack'
                elif value==12:
                    card_value=10
                    card_name='Queen'
                elif value==13:
                    card_value=10
                    card_name='King'
                elif value==14:
                    card_value=11
                    card_name='Ace'

                c=Card(suits,card_value,card_name)
                self.deck.append(c)
        return self.deck
    def show_deck(self):
        for i in self.deck:
            print(i)
    def shuffle_deck(self):
        return random.shuffle(self.deck)
    def deal_a_card(self):
       return self.deck.pop()

class Player_Instance():
    def __init__(self):
        self.name=" "
        self.hand=[]
        self.hands_score=0
        self.aces_count=0
    def bust_check(self):
        if self.hands_score>21 and self.aces_count==0:
            print(f'{self.name} Bust with {self.hands_score} ')
            return True
        elif self.hands_score>21 and self.aces_count>0:
            self.hands_score-=10
            self.aces_count-=1
            self.show_hand_info()
        return False
        

    def hit(self,card):
        self.hand.append(card)
        if card.name=='Ace':
            self.aces_count+=1
        self.hands_score+=card.value
        self.bust_check()
        

    def get_hands_score(self):
        current_score=0
        self.hands_score=0
        for card in self.hand:
            current_score+=card.value
        self.hands_score=current_score
        return self.hands_score

    

    def show_hand_info(self):
        print(f'{self.name} has in his hand: ')
        for card in self.hand:
            print(card)
        print(f'Current hand value is: {self.get_hands_score()}')

class Player(Player_Instance):
    def __init__(self):
        super().__init__()
        self.name=input('Input your name: ')
        self.chips=1000
        self.current_bet=0
        self.playing_state=True
        self.black_jack=False
        print(f'Welcome {self.name}! Your Balance is {self.chips}')

    def place_your_bet(self):
        bet=input('Place your bet please: ')
        while True:
            if bet.isdigit():
                if int(bet)>self.chips:
                   print(f'Not enough chips! You currently have {self.chips}')
                   bet=input('Insert suffcient amount: ')
                else:
                   self.current_bet=int(bet)
                   self.chips-=self.current_bet
                   print(f'You have placed {self.current_bet}. Chips:{self.chips}')
                   break
                   
            else:
                bet=input('Your bet has to be a number! ')
        print('No more bets!')



class Dealer(Player_Instance):
    def __init__(self):
        super().__init__()
        self.name="Dealer_Bob"
    def show_one_card(self):
        print(f'Dealer plays with open {self.hand[0]}')

class Game:
    def __init__(self,player,dealer):
        self.player=player
        self.dealer=dealer
        self.playing_deck=Deck()

    def play_the_game(self):
        
        while True:
            
            would_you_like_to_play=input('Would you like to play? Y/N')
            while would_you_like_to_play!='Y' and would_you_like_to_play!='N':
                would_you_like_to_play=input('Would you like to play? Y/N')
            if would_you_like_to_play=='N':
                break
            else:
                self.player.hands_score=0
                self.dealer.hands_score=0
                self.player.playing_state=True
                self.player.hand.clear()
                self.dealer.hand.clear()
                
                self.playing_deck.get_deck()
                self.playing_deck.shuffle_deck()
                self.player.place_your_bet()
                

                

                self.player.hand.append(self.playing_deck.deal_a_card())
                self.player.hand.append(self.playing_deck.deal_a_card())
                self.player.bust_check()
                self.dealer.hand.append(self.playing_deck.deal_a_card())
                self.dealer.hand.append(self.playing_deck.deal_a_card())
                self.dealer.bust_check()
                self.player.show_hand_info()
                self.dealer.show_one_card()
                self.player.get_hands_score()
                while self.player.playing_state:
                    if self.player.hands_score==21 and len(self.player.hand)==2:
                        print(f'Congratulations {self.player.name}! Its a BLACKJACK')
                        self.player.chips+=self.player.current_bet*2.5
                        self.player.playing_state=False
                        self.player.black_jack=True
                    else:
                        if self.player.hands_score<22:
                            print(f'Your hand value is {self.player.hands_score}')
                            askForAction=input('Stand/Hit? ')
                            while askForAction!='Hit' and askForAction!='Stand':
                                askForAction=input('Please insert Hit or Stand')
                            if askForAction=='Hit':
                                
                                self.player.hit(self.playing_deck.deal_a_card())
                                self.player.bust_check()
                            elif askForAction=='Stand':
                                self.player.playing_state=False
                        else:
                            self.player.playing_state=False
                print('???')
                if self.player.black_jack==False:
                    if self.player.hands_score<22:
                        self.player.show_hand_info()

                        print(f'{self.dealer.name} is now playing')

                        self.dealer.show_hand_info()
                        self.dealer.get_hands_score()
                        if self.dealer.hands_score==21 and len(self.dealer.hand)==2:
                            print(f"{self.dealer.name} has a blackjack!")
                            print(f'Unfortunately {self.player.name} has lost')
                        elif self.dealer.hands_score<17:
                            while self.dealer.hands_score<16:
                                self.dealer.hit(self.playing_deck.deal_a_card())
                                self.dealer.show_hand_info()
                                self.dealer.get_hands_score()
                            if self.dealer.hands_score<self.player.hands_score or self.dealer.hands_score>21:
                                print(f"{self.player.name} has won! You get {self.player.current_bet*2}")
                                self.player.chips+=self.player.current_bet*2
                                print(f"Your balance is now {self.player.chips}")
                            elif self.dealer.hands_score>self.player.hands_score:
                                print(f"{self.dealer.name} has won! You lost {self.player.current_bet}")
                                
                                print(f"Your balance is now {self.player.chips}")
                            elif self.dealer.hands_score==self.player.hands_score:
                                print(f"Its a draw! {self.player.name} gets back {self.player.current_bet}")
                                self.player.chips+=self.player.current_bet
                                print(f"Your balance is now {self.player.chips}")
                    else:
                            print(f"{self.dealer.name} has won! {self.player.name} lost {self.player.current_bet}")
                            
                            print(f"Your balance is now {self.player.chips}")
                else:
                    if self.dealer.hands_score<self.player.hands_score or self.dealer.hands_score>21:
                                print(f"{self.player.name} has won! You get {self.player.current_bet*2}")
                                self.player.chips+=self.player.current_bet*2.5
                if self.player.chips<=0:
                    print(f"{self.player.name} lost everythin in the casino!")
                    break
                

            # while self.player.playing_state:

        # self.playing_deck.show_deck()
        



if __name__=='__main__':
    player1=Player()
    dealer=Dealer()
    myGame=Game(player1,dealer)
    myGame.play_the_game()
    print('Thanks for playing!')






    



# class Dealer:
#     def __init__(self):
#         self.name="Dealer Richard"
#         self.dealer_hand=[]
#         self.bank=1000
#     def get_hand_value(self):
#         total_score=0
#         if self.dealer_hand==[]:
#             print(f"{self.name}'s is empty ")
#         else:
#             for cards in self.dealer_hand:
#                 total_score+=cards.value
#             print(f'{self.name} has {total_score} in their hand')
#             self.get_hand()
#             return total_score
#     def get_hand(self):
#         print(f'Dealer cards are:')
#         for card in self.dealer_hand:
#             print(card)
#     def show_one_card(self):
#         print(f'Dealer has {self.dealer_hand[0]}')
#         print('..............')

# class Player:
#     def __init__(self):
#         self.name=input('Input your name: ')
#         self.player_hand=[]
#         self.bank=1000
#     def get_hand_value(self):
#         total_score=0
#         if self.player_hand==[]:
#             print(f"{self.name}'s is empty ")
#         else:
#             for cards in self.player_hand:
                
#                 total_score+=cards.value
#             print(f'{self.name} has {total_score} in their hand')
#             self.get_hand()
#             return total_score
#     def get_hand(self):
#         print(f'Your cards are:')
#         for card in self.player_hand:
#             print(card)
#         print('..............')