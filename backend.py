import random
import pygame

pygame.init()

screen=pygame.display.set_mode((1280,720))
pygame.display.set_caption("CALL BREAK")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))

suites=['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
deck=[]

def get_font(size):
	return pygame.font.Font("assets/font.ttf", size)

def get_font_d(size):
	return pygame.font.Font("assets/digital-7.ttf", size)

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):	#blit the text and image of the button
		if self.image is not None:
			screen.blit(self.image, self.rect)
		if self.text is not "":
			screen.blit(self.text, self.text_rect)	
		
	def checkForInput(self, position):	#check for the button being selected by mouse
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):	#change color on hovering based on mouse position
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

class cards:
	def __init__(self,value,suit,priority):
		self.suit=suit
		self.value=value
		self.priority=priority
		self.image=pygame.image.load("cards/"+value+suit+".png")	



class player:
	def __init__(self,name):
		self.name=name
		self.point=0
		self.score=0
		self.bid=0
		self.hand=[]        #hand of total cards available
		self.playable=[]    #cards that can be played in a turn is selected

	
	def select_card(self,suit,priority):        #select card for bot
		self.playable=[]
		for i in self.hand:
			if i.suit==suit and i.priority>priority:
				self.playable.append(i)
		if (len(self.playable)==0):
			for i in self.hand:
				if i.suit==suit:
					self.playable.append(i)
			if (len(self.playable)==0):
				for i in self.hand:
					if i.priority>20:
						self.playable.append(i)
				if (len(self.playable)==0):
					if(len(self.hand)>0):
						min=self.hand[0]
					for a in self.hand:
						if a.priority < min.priority:      #same suit and spade not available so min priority is selected
							min=a
					self.hand.remove(min)    
					return min
				else:   #same suit not available but spade is available
					min=self.playable[0]
					for a in self.playable:
						if a.priority < min.priority:
							min=a
					self.hand.remove(min)    
					return min
			else: #same suit but less priority
				min=self.playable[0]
				for a in self.playable:
					if a.priority < min.priority:
						min=a
				self.hand.remove(min)    
				return min
		else:   #same suit and greater priority
			max=self.playable[0]
			for a in self.playable:
				if a.priority > max.priority:
					max=a
			self.hand.remove(max)    
			return max

	def select_card_user(self,suit,priority):   #showing suitable cards for user
		self.playable=[]
		for i in self.hand:
			if i.suit==suit and i.priority>priority:		  #same suit and higher priority
				self.playable.append(i)
		if (len(self.playable)==0):
			for i in self.hand:
				if i.suit==suit:							  #Same suit but not higher priority
					self.playable.append(i)
			if (len(self.playable)==0):
				for i in self.hand:
					if i.priority>20:						  #Same suit not available but higher priority
						self.playable.append(i)
				if (len(self.playable)==0):                   # same suit or spade not available
					self.playable=self.hand



p=[player("You"),player("Player 2"),player("Player 3"),player("Player 4")]  #four player object created

def un_deck():
	for i in suites:
		p=1
		for j in values:                 
			if i =="Spades":
				pri=p*15
				p+=1
			else:
				pri=p
				p+=1
			deck.append(cards(j,i,pri))         #unrandomized deck is created

def shuffle() :
	random.shuffle(deck)        #deck is shuffled
	return deck


def distribue_cards():
	card=shuffle()
	n=51
	while n>=0:
		if n%4==0:                                     
			p[0].hand.append(card.pop(n))       #distribute
		elif n%4==1:                                    #among
			p[1].hand.append(card.pop(n))                      #four
		elif n%4==2:                                                #players
			p[2].hand.append(card.pop(n))
		elif n%4==3:
			p[3].hand.append(card.pop(n))
		n-=1
	del card                                            
	del n 
	check()


def check() :       #rulles of shuffling
	for i in p:
		ace,heart,diamond,spade,club=0,0,0,0,0
		for j in i.hand:
			if j.value=="A":
				ace+=1
			if j.suit=="Hearts":
				heart+=1    
			elif j.suit=="Diamonds":
				diamond+=1 
			elif j.suit=="Clubs":
				club+=1 
			else:
				spade+=1
		if (ace>=3 or heart>=7 or diamond>=7 or club>=7 or spade>=7 or heart==0 or diamond==0 or club==0 or spade==0):
			for i in range(4):   
				p[i].hand=[]
			un_deck()     
			distribue_cards()
			break      


def bid_setter(): #bid is set for the bots
	# for i in range (4):
	# 	p[i].bid=0
	# 	p[i].point=0
	# p[0].show_hand()    
	# p[0].bid=int(input("Enter your bid : "))
	for i in range (1,4):
		for j in p[i].hand:
			if(j.value == "A" or j.value == "K"):
				p[i].bid+=1
		if(p[i].bid==0):
			p[i].bid=1  
		# print("player",i+1,"took bid",p[i].bid)          

def score_setter(): #points and bid are compared after a turn and scored is calculated and stored
	for i in range(4):
		if(p[i].bid>p[i].point):
			p[i].score-=p[i].bid
		else:
			p[i].score+=p[i].bid+0.1*(p[i].point-p[i].bid)  


def winner(trn,suit): #turn list and turn suit are the parameter
	max,index=0,0
	for i in range (4):
		if (trn[i].suit==suit or trn[i].suit=="Spades") and (trn[i].priority > max):
			max=trn[i].priority
			index=i

	return index