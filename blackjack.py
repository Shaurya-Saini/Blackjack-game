#BLACKJACK

import random
from random import shuffle
from tabulate import tabulate
import os
import time

ranks={'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':[1,11]}
class Card():
    def __init__(self,value,suite):
        self.suite=suite
        self.value=value
    def __str__(self):
        return f'{self.value} of {self.suite}'
    def rank(self):
        return ranks[self.value]

suits=['Hearts','Diamonds','Spades','Clubs']
values=['Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']
class Deck():
    def __init__(self,list_cards=[]):
        self.list_cards=list_cards
    def new_deck(self):
        for i in values:
            for j in suits:
                self.list_cards.append(Card(i,j))
    def shuffle_deck(self):
        shuffle(self.list_cards)
    def deal_card(self,number=1):
        lis=[]
        for i in range(0,number):
            lis.append(self.list_cards.pop(0))
        return lis
    def cards_left(self):
        return len(self.list_cards)
    def add_cards(self,lis):
        for i in lis:
            self.list_cards.append(i)
    def index(self,number):
        return self.list_cards[number]
    def points(self):
        point=0
        n=0
        for i in self.list_cards:
            if i.value!='Ace':
                point+=i.rank() 
            elif i.value=='Ace':
                n+=1
        lis=[point]
        for i in range(0,n):
            newlis=[]
            for j in lis:
                newlis.append(j+1)
                newlis.append(j+11)
            lis=list(newlis)
        if len(lis)>1:
            for i in lis:
                if i>21:
                    lis.remove(i)
        return lis
    def show(self,number=0):
        lis=[]
        for i in self.list_cards:
            lis.append(str(i))
        if number!=0:
            lis.pop(-1)
            lis.append('???????')
        return lis
    def over21(self):
        flag=0
        for i in self.points():
            if i>21:
                flag+=1
        if flag==len(self.points()):
            return True
        else:
            return False


class Money():
    def __init__(self,amount=2000,bet=0):
        self.amount=amount
        self.bet=bet 
    def bet_money(self,amt='lol'):
        while True:
            amt=input('ENTER BET AMOUNT = $')
            if amt.isdigit()==False:
                continue
            amt=int(amt)
            if self.amount<amt:
                print('Not enough Money')
                continue
            else:
                break
        self.bet=amt
        self.amount-=amt
    def win_bet(self):
        self.amount+=2*self.bet
        print(f'YOU WON ${self.bet}')
        self.bet=0
    def lost_bet(self):
        self.bet=0
    def blackjack(self):
        self.amount+=self.bet*2.5
        print(f'YOU WON ${self.bet*1.5}')
        self.bet=0
    def __str__(self):
        return f'YOU HAVE ${self.amount}'


def table(game_cards):
    os.system('cls')
    print(tabulate(game_cards,headers="keys",tablefmt="outline"))
cash='lol'
while True:
    cash=input("ENTER THE MONEY YOU WOULD LIKE TO START WITH limit=(1,5000) = $")
    if cash.isdigit()==False:
        continue
    cash=int(cash)
    if cash in range(1,5001):
        break
casino=Money(cash)
push=0
while True:
    if push==0:
        os.system('cls')
        print(casino)
        casino.bet_money()
    while True:
        game=Deck([])
        game.new_deck()
        game.shuffle_deck() 
        lost=0
        win=0
        blackjack=0
        push=0
        dealer=Deck([])
        player=Deck([])
        dealer.add_cards(game.deal_card(2))
        player.add_cards(game.deal_card(2))
        game_cards={f"PLAYER'S CARDS -- {player.points()}":player.show(),f"DEALER'S CARDS -- [??]":dealer.show(1)}
        table(game_cards)
        if player.over21()==True:
            lost+=1
            break
        for i in player.points():
            if i==21:
                blackjack+=1
        if blackjack!=0:
            break
        while True:
            print('\n\n\nIf you wish to HIT, enter anything\nIf you wish to STAND, just press enter\n')
            choice=input("Enter your choice - ")
            if choice:
                player.add_cards(game.deal_card())
                game_cards={f"PLAYER'S CARDS -- {player.points()}":player.show(),f"DEALER'S CARDS -- [??]":dealer.show(1)}
                table(game_cards)
                if player.over21()==True:
                    lost+=1
                    break
                continue
            else:
                break
        if player.over21()==True:
            lost+=1
            break
        game_cards={f"PLAYER'S CARDS -- {player.points()}":player.show(),f"DEALER'S CARDS -- {dealer.points()}":dealer.show()}
        table(game_cards)
        time.sleep(1)
        if dealer.over21()==True:
            win+=1
            break
        while dealer.points()[-1]<=16:
            dealer.add_cards(game.deal_card())
            game_cards={f"PLAYER'S CARDS -- {player.points()}":player.show(),f"DEALER'S CARDS -- {dealer.points()}":dealer.show()}
            table(game_cards)
            time.sleep(1)
        if dealer.over21()==True:
            win+=1
            break
        dealer.points()
        if player.points()[-1]>dealer.points()[-1] and player.over21()==False:
            win+=1
            break
        elif player.points()[-1]<dealer.points()[-1] or player.over21()==True:
            lost+=1
            break
        else:
            push+=1
            break
    if win!=0:
        print('CONGRATES YOU WON')
        casino.win_bet()
        print(casino)
    elif lost!=0:
        print('YOU LOST')
        print(casino)
    if blackjack!=0:
        print('CONGRATES YOU WON BY BLACKJACK')
        casino.blackjack()
        print(casino)
    elif push!=0:
        print('PUSH')
        time.sleep(1)
        continue
    if casino.amount==0:
        time.sleep(2)
        break
    gameon=input("If you want to continue enter anything = ")
    if gameon:
        continue
    else:
        break
os.system('cls')
print(casino)
print('THANKS FOR PLAYING')
time.sleep(100)