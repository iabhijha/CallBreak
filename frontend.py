from random import randint
import sys
from time import sleep
from tkinter import CENTER
from backend import *

BG_MM = pygame.image.load("assets/mainmenu.png")
BG_PLAY = pygame.image.load("assets/playscreen.png")
BB_RULES1 = pygame.image.load("assets/Help1.png")
BB_RULES2 = pygame.image.load("assets/Help2.png")
bid_screen=pygame.image.load("assets/BidScreen.png")
name_screen=pygame.image.load("assets/NameScreen.png")
BG_WS=pygame.image.load("assets/WinnerScreen.png")

pygame.mixer.music.load("assets/bgm.mp3")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)

card_sound=pygame.mixer.Sound("assets/card_all.mp3")
wrong_card_sound=pygame.mixer.Sound("assets/wrong_card.mp3")
player_win=pygame.mixer.Sound("assets/IfUserWins.mp3")
player_lose=pygame.mixer.Sound("assets/IfUserLoses.mp3")


turn = [None, None, None, None]

def print_card(user,one,two,three):
	# for i in range(10000):     #to make the gameplay slow
	# 	print()
	
	if user is not None:
		screen.blit(user.image,(598,399))	
	else:
		screen.blit(pygame.image.load("cards/1B.png"),(600,399))
	
	if one is not None:
		screen.blit (one.image,(884,275))
	else:
		screen.blit(pygame.image.load("cards/1B.png"),(884,275))
	
	if two is not None:
		screen.blit(two.image,(598,153))
	else:
		screen.blit(pygame.image.load("cards/1B.png"),(598,153))
	
	if three is not None:
		screen.blit(three.image,(330,275))
	else:
		screen.blit(pygame.image.load("cards/1B.png"),(330,275))

#--------------------------------------------------------------------------------------

def print_score(user,one,two,three):
	font=pygame.font.Font("assets/digital-7.ttf",40)
	text=font.render(str(user),True,(255,255,255))
	screen.blit(text,(880,676))

	font=pygame.font.Font("assets/digital-7.ttf",40)
	text=font.render(str(one),True,(255,255,255))
	screen.blit(text,(1210,494))

	font=pygame.font.Font("assets/digital-7.ttf",40)
	text=font.render(str(two),True,(255,255,255))
	screen.blit(text,(820,34))

	font=pygame.font.Font("assets/digital-7.ttf",40)
	text=font.render(str(three),True,(255,255,255))
	screen.blit(text,(150,494))

#--------------------------------------------------------------------------------------

def print_bid():
	font=pygame.font.Font("assets/Blacklisted.ttf",20)
	text=font.render("Bid: "+str(p[0].bid),True,(255,255,255))
	screen.blit(text,(612,519))

	font=pygame.font.Font("assets/Blacklisted.ttf",20)
	text=font.render("Bid: "+str(p[1].bid),True,(255,255,255))
	screen.blit(text,(980,290))

	font=pygame.font.Font("assets/Blacklisted.ttf",20)
	text=font.render("Bid: "+str(p[2].bid),True,(255,255,255))
	screen.blit(text,(612,118))

	font=pygame.font.Font("assets/Blacklisted.ttf",20)
	text=font.render("Bid: "+str(p[3].bid),True,(255,255,255))
	screen.blit(text,(260,290))

#--------------------------------------------------------------------------------------
def WinnerScreen():
	global name
	score=[p[0].score,p[1].score,p[2].score,p[3].score]
	max_index=0
	max=score[0]
	for i in range(4):
		if max<score[i]:
			max=score[i]
			max_index=i
	if(max_index==0):
		player_win.play()
		txt=name
	else :
		player_lose.play()
		txt="BOT "+str(max_index)	
	while True:
		mouse_pos=pygame.mouse.get_pos()
		screen.blit(BG_WS,(0,0))
		b_MM=Button(None,(425,490),"MAIN MENU",get_font_d(80),"White","Cyan")
		b_NG=Button(None,(850,490),"NEW GAME",get_font_d(80),"White","Cyan")

		for i in [b_MM,b_NG]:
			i.changeColor(mouse_pos)
			i.update(screen)

		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type==pygame.MOUSEBUTTONDOWN:
					if b_MM.checkForInput(mouse_pos):
						name=""
						pygame.mixer.music.play()
						mainmenu()
					if b_NG.checkForInput(mouse_pos):
						name=""
						name_accept()
		
		font=pygame.font.Font("assets/Blacklisted.ttf",20)
		font1=pygame.font.Font("assets/Blacklisted.ttf",90)
		font2=pygame.font.Font("assets/Gumela.ttf",30)

		winner=font1.render(txt,True,(50,155,100))
		user=font.render(name,True,(0,0,0))
		usr_pnt=font.render(str(p[0].score),True,(0,0,0))
		bot1=font.render("BOT 1                    "+str(p[1].score),True,(0,0,0))
		bot2=font.render("BOT 2                    "+str(p[2].score),True,(0,0,0))
		bot3=font.render("BOT 3                    "+str(p[3].score),True,(0,0,0))
		txt2=font2.render("THE WINNER IS",True,(0,0,0))
		screen.blit(usr_pnt,(530,285))
		screen.blit(user,(380,285))
		screen.blit(bot1,(800,285))
		screen.blit(bot2,(380,368))
		screen.blit(bot3,(800,368))
		win_rect=winner.get_rect(center=(640,200))
		txt2_rect=txt2.get_rect(center=(640,110))
		screen.blit(txt2,txt2_rect)
		screen.blit(winner,win_rect)
		pygame.display.update()
#--------------------------------------------------------------------------------------
def play():
	start = 0
	s=None
	pri = 0
	pause = False
	print = [None,None,None,None]
	while True:
		playable_interactive = []
		x = ((1280-(75*len(p[0].hand)))/2)+37.5
		screen.blit(BG_PLAY, (0, 0))

		mouse_pos = pygame.mouse.get_pos()


		font=pygame.font.Font("assets/Doctor Glitch.otf",28)	#Printing the accepted name
		text_name=font.render(name,True,(217,252,55))
		screen.blit(text_name,(470,675))

		for i in p[0].hand: #user's hand is converted to a button
			y=605
			playable_interactive.append(Button(i.image, (x,y), "", get_font(10), "white", "cyan"))
			x += 75
		for i in playable_interactive: #user's hand is printed on screen
			i.update(screen)

			
		if pause==False :
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN: #go to mainmenu if esc is pressed
					if event.key==pygame.K_ESCAPE:
						pygame.mixer.music.play()
						mainmenu()
				if event.type == pygame.MOUSEBUTTONDOWN:
					for count,card in enumerate(playable_interactive):
						if card.checkForInput(mouse_pos):
							if start==0: #when user starts the turn
								if print[3] == None :
									p[0].playable=p[0].hand
								else :	
									p[0].select_card_user(s, pri)

								a = None	
								for i in p[0].hand :
									if i.image == playable_interactive[count].image :
										a = i
								if a in p[0].playable :
									card_sound.play()
									print[0]=playable_interactive.pop(count)
									turn[0]=p[0].hand.pop(count)
									if turn[0].priority >= pri :
										pri = turn[0].priority
									if print[3] == None :
										s=turn[0].suit	
									if print[1]==None:
										start =1	
								else :
									wrong_card_sound.play()
									font=pygame.font.Font("freesansbold.ttf",30)
									text=font.render("Chose Another Card",True,(255,255,255))
									screen.blit(text,(500,320))
							
			if start != 0 : #when bot starts the the turn
				if pri==0 :
					if (len(p[start].hand)-1)>=0:
						turn[start]=p[start].hand.pop(randint(0,len(p[start].hand)-1))
					s=turn[start].suit
					pri=turn[start].priority
				else:
					turn[start]=p[start].select_card(s,pri)
					if turn[start].priority>=pri:
						pri = turn[start].priority

				print[start]=turn[start]
				card_sound.play()
				start = (start+1)%4
						 
			if ( print[1] != None and print[2] != None and print[3] != None and print[0] != None) : #to check for winner
				start = winner(turn,s)
				p[start].point+=1
				pause = True
				s,pri=None,0

			

		else:
			for event in pygame.event.get() :
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:	#continue game after each turn on pressing space
					if event.key==pygame.K_SPACE:
						pause = False
						print=[None,None,None,None]


			if(start==0):
				font=pygame.font.Font("assets/MARSONFree.otf",40)
				text=font.render("You win this turn",True,(255,255,255))
				screen.blit(text,(530,305))
			else:
				font=pygame.font.Font("assets/MARSONFree.otf",40)
				text=font.render("Winner of this turn is bot "+str(start-1),True,(255,255,255))
				screen.blit(text,(480,305))

			font=pygame.font.Font("assets/Gumela.ttf",30)
			text=font.render("Press SPACE to continue",True,(0,255,50))
			screen.blit(text,(472,340))


		if (p[0].point + p[1].point + p[3].point + p[2].point)==13 : #go to winner screen and calculate score
			score_setter()
			WinnerScreen()

		print_score(p[0].point,p[1].point,p[2].point,p[3].point)
		print_bid()
		print_card(print[0],print[1],print[2],print[3]) #print all the cards on screen
		pygame.display.update()    

#----------------------------------------------------------------------------------------

def rules():	#blit the help screen
	counter=0
	while True:
		mouse_pos=pygame.mouse.get_pos()
		if counter==0:
			screen.blit(BB_RULES1,(0,0))
		elif counter==1:
			screen.blit(BB_RULES2,(0,0))

		next_text=Button(None,(1250,415),">",get_font(55),"white","cyan")
		prev_text=Button(None,(40,415),"<",get_font(55),"white","cyan")
		close_text=Button(None,(1250,50),"X",get_font(55),"white","cyan")

		for i in [next_text,prev_text,close_text]:
			i.changeColor(mouse_pos)
			i.update(screen)

		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type==pygame.MOUSEBUTTONDOWN:
				if next_text.checkForInput(mouse_pos):
					counter=1
				if prev_text.checkForInput(mouse_pos):
					counter=0
				if close_text.checkForInput(mouse_pos):
					mainmenu()
		pygame.display.update()

# ----------------------------------------------------------------------------------------

def name_accept():
	global name

	while True:
		mouse_pos=pygame.mouse.get_pos()	
		screen.blit(name_screen,(0,0))

		next_text=Button(None,(880,400),"NEXT",get_font(30),"Black","Blue")
		back_text=Button(None,(405,400),"BACK",get_font(30),"Black","Blue")

		for i in [next_text,back_text]:
			i.changeColor(mouse_pos)
			i.update(screen)

		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type==pygame.MOUSEBUTTONDOWN:
				if next_text.checkForInput(mouse_pos):
					enter_bid()
				if back_text.checkForInput(mouse_pos):
					name=""
					mainmenu()
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_a:
					name=name+"A"
				if event.key==pygame.K_b:
					name=name+"B"
				if event.key==pygame.K_c:
					name=name+"C"
				if event.key==pygame.K_d:
					name=name+"D"
				if event.key==pygame.K_e:
					name=name+"E"
				if event.key==pygame.K_f:
					name=name+"F"
				if event.key==pygame.K_g:
					name=name+"G"
				if event.key==pygame.K_h:
					name=name+"H"
				if event.key==pygame.K_i:
					name=name+"I"
				if event.key==pygame.K_j:
					name=name+"J"
				if event.key==pygame.K_k:
					name=name+"K"
				if event.key==pygame.K_l:
					name=name+"L"
				if event.key==pygame.K_m:
					name=name+"M"
				if event.key==pygame.K_n:
					name=name+"N"
				if event.key==pygame.K_o:
					name=name+"O"
				if event.key==pygame.K_p:
					name=name+"P"
				if event.key==pygame.K_q:
					name=name+"Q"
				if event.key==pygame.K_r:
					name=name+"R"
				if event.key==pygame.K_s:
					name=name+"S"
				if event.key==pygame.K_t:
					name=name+"T"
				if event.key==pygame.K_u:
					name=name+"U"
				if event.key==pygame.K_v:
					name=name+"V"
				if event.key==pygame.K_w:
					name=name+"W"
				if event.key==pygame.K_x:
					name=name+"X"
				if event.key==pygame.K_y:
					name=name+"Y"
				if event.key==pygame.K_z:
					name=name+"Z"
				if event.key==pygame.K_BACKSPACE:
					name=name[:-1]


		font=pygame.font.Font("assets/Doctor Glitch.otf",28)
		text_name=font.render(name,True,(217,252,60))
		text_rect=text_name.get_rect(center=(640,292))
		screen.blit(text_name,text_rect)

		pygame.display.update()

#----------------------------------------------------------------------------------------


def enter_bid():
	while True:
		mouse_pos=pygame.mouse.get_pos()
		x = ((1280-(75*len(p[0].hand)))/2)+37.5
		screen.blit(bid_screen,(0,0))

		playable_interactive = []

		for i in p[0].hand: #user's hand is converted to a button
			y=605
			playable_interactive.append(Button(i.image, (x,y), "", get_font(10), "white", "cyan"))
			x += 75
		for i in playable_interactive: #user's hand is printed on screen
			i.update(screen)

		b_1=Button(None,(250,250),"1",get_font_d(40),"Black","White")
		b_2=Button(None,(530,250),"2",get_font_d(40),"Black","White")
		b_3=Button(None,(810,250),"3",get_font_d(40),"Black","White")
		b_4=Button(None,(1080,250),"4",get_font_d(40),"Black","White")	#button is created for 1-8
		b_5=Button(None,(250,360),"5",get_font_d(40),"Black","White")
		b_6=Button(None,(530,360),"6",get_font_d(40),"Black","White")
		b_7=Button(None,(810,360),"7",get_font_d(40),"Black","White")
		b_8=Button(None,(1080,360),"8",get_font_d(40),"Black","White")

		for i in [b_1,b_2,b_3,b_4,b_5,b_6,b_7,b_8]:
			i.changeColor(mouse_pos)
			i.update(screen)

		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type==pygame.MOUSEBUTTONDOWN:
				bid_setter()
				if b_1.checkForInput(mouse_pos):
					p[0].bid=1
					del playable_interactive
					play()
				if b_2.checkForInput(mouse_pos):
					p[0].bid=2
					del playable_interactive
					play()
				if b_3.checkForInput(mouse_pos):
					p[0].bid=3
					del playable_interactive
					play()
				if b_4.checkForInput(mouse_pos):
					p[0].bid=4
					del playable_interactive
					play()
				if b_5.checkForInput(mouse_pos):
					p[0].bid=5
					del playable_interactive
					play()
				if b_6.checkForInput(mouse_pos):
					p[0].bid=6
					del playable_interactive
					play()
				if b_7.checkForInput(mouse_pos):
					p[0].bid=7
					del playable_interactive
					play()
				if b_8.checkForInput(mouse_pos):
					p[0].bid=8
					del playable_interactive
					play()

		pygame.display.update()

#----------------------------------------------------------------------------------------
def mainmenu():
	while True:
		screen.blit(BG_MM,(0,0))

		mouse_pos=pygame.mouse.get_pos()

		play_text=Button(None,(650,415),"PLAY",get_font(55),"white","cyan")
		quit_text=Button(None,(770,525),"QUIT",get_font(35),"white","cyan")
		help_text=Button(None,(510,525),"HELP",get_font(35),"white","cyan")

		for i in [play_text,quit_text,help_text]:
			i.changeColor(mouse_pos)
			i.update(screen)

		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type==pygame.MOUSEBUTTONDOWN:
				if play_text.checkForInput(mouse_pos):
					pygame.mixer.music.pause()
					un_deck()
					distribue_cards()
					name_accept()
				if quit_text.checkForInput(mouse_pos):
					pygame.quit()
					sys.exit()
				if help_text.checkForInput(mouse_pos):
					rules()

		pygame.display.update()

name=""
mainmenu()