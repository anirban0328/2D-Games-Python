# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
win = 0
lose = 0
message = "Hit or Stand?"
flag = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))        
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        if in_play == True:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.hand = []
 
    def __str__(self):
        return str(self.hand)

    def add_card(self, card):       
        self.hand.append(str(card))
        
# gets value of hand
    def get_value(self):
        global flag
        p = 0
        for i in range(len(self.hand)):
            if self.hand[i][1] in VALUES:
                 p += VALUES[self.hand[i][1]]
                 if flag == 0:   
                    if self.hand[i][1] == "A" and p + 10 <= 21:
                       p +=10        
        return p        
    
    def draw(self, canvas, p):
         for i in range(len(self.hand)):
                card = Card(self.hand[i][0], self.hand[i][1])
                card.draw(canvas, [i * 90 + 50, p * 200])
         
# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        self.deck = [(suit + rank) for suit in SUITS for rank in RANKS]
                
# add cards back to deck and shuffle
    def shuffle(self):
        random.shuffle(self.deck)
 
    def deal_card(self):
        return random.choice(self.deck)
 
    def __str__(self):
        return str(self.deck)

#define event handlers for buttons
def deal():
    global in_play,player,dealer,d,outcome,message,win,lose
    
    if(in_play == False):
       outcome = ""
       message = "Hit or Stand?"
       d = Deck()
       player = Hand() 
       dealer = Hand()
       player.add_card(d.deal_card())
       player.add_card(d.deal_card())
       dealer.add_card(d.deal_card())
       dealer.add_card(d.deal_card())
       in_play = True
    
    else:
       outcome = "Dealer Wins"
       lose +=1
       in_play = False
       message = "New Deal?"

def hit():
    global player,d,outcome,in_play,win,lose,message,flag
    flag = 1
    
    if(in_play == True):
      player.add_card(d.deal_card())      
      if player.get_value() > 21:        
        outcome = "Player got busted"
        message = "New Deal?"
        in_play = False
        lose += 1
      
      elif player.get_value() == 21:        
        outcome = "Blackjack-Player wins"
        message = "New Deal?"
        in_play = False
        win += 1        
       
def stand():
    global dealer,player,d,win,lose,in_play,outcome,message    
    if(in_play == True):
      if outcome == "Player got busted":        
        outcome = "Player got busted"
        message = "New Deal?"
      
      else:        
        while dealer.get_value() < 17:
            dealer.add_card(d.deal_card())
        
        if dealer.get_value() > 21:                   
            outcome = "Dealer is busted"
            message = "New Deal?"
            win +=1        
        elif dealer.get_value() == 21:
            outcome = "Blackjack-Dealer Wins"
            message = "New Deal?"
            lose +=1
        elif player.get_value() <= dealer.get_value():
            outcome = "Dealer Wins"
            message = "New Deal?"
            lose +=1
        else:
            outcome = "Player wins"
            message = "New Deal?"
            win +=1
      in_play = False

# draw handler    
def draw(canvas):
    global win,lose,outcome,message
    dealer.draw(canvas, 1)
    player.draw(canvas, 2)
    canvas.draw_text("Blackjack", (100, 100), 32, "Navy")
    canvas.draw_text("Dealer", (60, 170), 22, "Black")
    canvas.draw_text("Player", (60, 370), 22, "Black")
    canvas.draw_text("WIN : "+str(win), (350, 100), 20, "Maroon")
    canvas.draw_text(" |", (425, 100), 28, "Maroon")
    canvas.draw_text("LOSE : "+str(lose), (450, 100), 20, "Maroon")
    canvas.draw_text(str(outcome), (300, 170), 22, "Black")
    canvas.draw_text(str(message), (250, 370), 28, "WhiteSmoke")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# deal an initial hand
deal()

# get things rolling
frame.start()