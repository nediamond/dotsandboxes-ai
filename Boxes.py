import pygame
import math
import client
from time import sleep

#connect to server while initing client
c = client.Client(raw_input("Address of server (localhost:8000):"))

#init python timing
pygame.init()
pygame.font.init()

width, height = 389, 500

#load images
normallinev=pygame.image.load("normalline.png")
coollinev=pygame.image.load("coolline.png")
normallineh=pygame.transform.rotate(pygame.image.load("normalline.png"), -90)
hoverlinev=pygame.image.load("hoverline.png")
redindicator=pygame.image.load("redindicator.png")
greenindicator=pygame.image.load("greenindicator.png")
greenplayer=pygame.image.load("greenplayer.png")
blueplayer=pygame.image.load("blueplayer.png")
winningscreen=pygame.image.load("youwin.png")
gameover=pygame.image.load("gameover.png")
hoverlineh=pygame.transform.rotate(pygame.image.load("hoverline.png"), -90)
coollineh=pygame.transform.rotate(pygame.image.load("coolline.png"), -90)

#square owner map
owner = [[0 for x in range(6)] for y in range(6)]
owner[0][0]=0
#utility function for calculating the score from the board
def calculate_score(board):
	me = 0
	otherplayer = 0
	for x in range(6):
		for y in range(6):
			if board[y][x]=="win":
				me+=1
			elif board[y][x]=="lose":
				otherplayer+=1
	return me, otherplayer
#is it my turn
turn = True

#initialize boards
#usage: boardX[x][y]
boardh = [[False for x in range(6)] for y in range(7)]
boardv = [[False for x in range(7)] for y in range(6)]

#initialize pygame screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Boxes")

#initialize player number
num=10

#initialize pygame clock
clock=pygame.time.Clock()

#server responses
c.input1=[]

#while loop until other player joins
stop=True
while stop:
	c.Loop()
	for event in c.input1:
		if event["action"]=="startgame":
			num=event["player"]
			gameid = event["gameid"]
			c.input1=[]
			stop=False
	sleep(0.01)

#determine attributes from player #
if num==0:
	turn=True
	marker = greenplayer
	othermarker = blueplayer
else:
	turn=False
	marker=blueplayer
	othermarker = greenplayer

#my score
me=0

# did i win?
didiwin=False

#other player's score
otherplayer=0

#game still running?
running=True
while running:

	# board full?
	if me+otherplayer==36:
		running=False
		didiwin=True if me>otherplayer else False

	#calculate score of board map
	me, otherplayer=calculate_score(owner)

	#clear the screen
	screen.fill(0)

	#sleep to make the game 60 fps
	clock.tick(60)

	#loop client qand recieve data from server
	c.Loop()

	#check queue for various server messages
	for event in c.input1:
		#my turn
		if event["action"]=="yourturn":
			#torf = short for true or false
			turn = event["torf"]
			#remove item from queue
			c.input1.remove(event)
		#placed line?
		if event["action"]=="place":
			#get attributes
			x = event["x"]
			y = event["y"]
			hv = event["hv"]

			#horizontal or vertical
			if hv=="h":
				boardh[y][x]=True
			else:
				boardv[y][x]=True
			#remove item from queue
			c.input1.remove(event)
		if event["action"]=="win":
			#set owner map
			owner[event["x"]][event["y"]]="win"
			boardh[event["y"]][event["x"]]=True
			boardv[event["y"]][event["x"]]=True
			boardh[event["y"]][event["x"]+1]=True
			boardv[event["y"]+1][event["x"]]=True
			#remove item from queue
			c.input1.remove(event)
			#add one point to my score
			me+=1
		if event["action"]=="lose":
			#set owner map to lost
			owner[event["x"]][event["y"]]="lose"
			boardh[event["y"]][event["x"]]=True
			boardv[event["y"]][event["x"]]=True
			boardh[event["y"]][event["x"]+1]=True
			boardv[event["y"]+1][event["x"]]=True
			#remove item from queue
			c.input1.remove(event)
			#add one to other players score
			otherplayer+=1
		if event["action"]=="close":
			exit()

	# draw the owner map
	for x in range(6):
		for y in range(6):
			if owner[x][y]!=0:
				if owner[x][y]=="win":
					screen.blit(marker, (x*64, y*64))
				if owner[x][y]=="lose":
					screen.blit(othermarker, (x*64, y*64))

	# This draws all of the lines other than the edges.
	for x in range(6):
		for y in range(6):
			if not boardh[y][x]:
				screen.blit(normallineh, [(x)*64, (y)*64])
			else:
				screen.blit(coollineh, [(x)*64, (y)*64])
			if not boardv[y][x]:
				screen.blit(normallinev, [(x)*64, (y)*64])
			else:
				screen.blit(coollinev, [(x)*64, (y)*64])
	# This draws the bottom and right edges.
	for edge in range(6):
		if not boardh[6][edge]:
			screen.blit(normallineh, [edge*64, 6*64])
		else:
			screen.blit(coollineh, [edge*64, 6*64])
		if not boardv[edge][6]:
			screen.blit(normallinev, [6*64, edge*64])
		else:
			screen.blit(coollinev, [6*64, edge*64])
	#HUD
	#create font
	myfont = pygame.font.SysFont(None, 32)
	#create text surface
	label = myfont.render("Your Turn:", 1, (255,255,255))
	#draw surface
	screen.blit(label, (10, 395))
	#same thing here
	myfont = pygame.font.SysFont(None, 64)
	score = myfont.render(str(me), 1, (255,255,255))
	myfont = pygame.font.SysFont(None, 20)
	scoretext = myfont.render("You", 1, (255,255,255))
	screen.blit(scoretext, (10, 425))
	screen.blit(score, (10, 435))
	myfont = pygame.font.SysFont(None, 64)
	score = myfont.render(str(otherplayer), 1, (255,255,255))
	myfont = pygame.font.SysFont(None, 20)
	scoretext = myfont.render("Other Player", 1, (255,255,255))
	screen.blit(scoretext, (220, 425))
	screen.blit(score, (300, 435))
	#draw indicator
	screen.blit(greenindicator if turn else redindicator, (195, 395))
	#get mouse position
	mouse = pygame.mouse.get_pos()
	#left or right
	x=["","","",""]
	#find x position, y position, and horizontal or vertical
	xpos = int(math.ceil((mouse[0]-32)/64.0))
	ypos = int(math.ceil((mouse[1]-32)/64.0))

	is_horizontal = abs(mouse[1] - ypos*64) < abs(mouse[0] - xpos*64)

	ypos = ypos - 1 if mouse[1] - ypos*64 < 0 and not is_horizontal else ypos
	xpos = xpos - 1 if mouse[0] - xpos*64 < 0 and is_horizontal else xpos

	#draw hover line for mouse
	board=boardh if is_horizontal else boardv 
	isoutofbounds=False
	try: 
		if not board[ypos][xpos]: screen.blit(hoverlineh if is_horizontal else hoverlinev, [xpos*64, ypos*64])
	except:
		isoutofbounds=True
		pass
	#place a line if it hasn't already been placed
	if pygame.mouse.get_pressed()[0] and turn==True and not isoutofbounds:
		alreadyplaced=False
		if is_horizontal:
			if boardh[ypos][xpos]==True:
				alreadyplaced=True
			else:
				# boardh[ypos][xpos] = True
				pass
		else:
			if boardv[ypos][xpos]==True:
				alreadyplaced=True
			else:
				# boardv[ypos][xpos] = True
				pass
		turn=False
		if not alreadyplaced:
			#send place of line to server
			c.Send({"action":"place", "hv":"h" if is_horizontal else "v", "y":ypos, "x":xpos, "gameid": gameid, "player": num})
	for event in pygame.event.get():
		#quit if the quit button was pressed
		if event.type == pygame.QUIT:
			exit()
	#update the screen
	pygame.display.flip()
screen.blit(gameover if not didiwin else winningscreen, (0,0))
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
	pygame.display.flip()