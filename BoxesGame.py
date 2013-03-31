import pygame, client, math
from time import sleep
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


class BoxesGame():
	def __init__(self):
		self.c = client.Client(raw_input("Address of server (localhost:8000):"))
		pygame.init()
		pygame.font.init()
		#load images
		self.normallinev=pygame.image.load("normalline.png")
		self.coollinev=pygame.image.load("coolline.png")
		self.normallineh=pygame.transform.rotate(pygame.image.load("normalline.png"), -90)
		self.hoverlinev=pygame.image.load("hoverline.png")
		self.redindicator=pygame.image.load("redindicator.png")
		self.greenindicator=pygame.image.load("greenindicator.png")
		self.greenplayer=pygame.image.load("greenplayer.png")
		self.blueplayer=pygame.image.load("blueplayer.png")
		self.winningscreen=pygame.image.load("youwin.png")
		self.gameover=pygame.image.load("gameover.png")
		self.hoverlineh=pygame.transform.rotate(pygame.image.load("hoverline.png"), -90)
		self.coollineh=pygame.transform.rotate(pygame.image.load("coolline.png"), -90)
		width, height = 389, 500
		#is it my turn
		self.turn = True

		#initialize boards
		#usage: boardX[x][y]
		self.boardh = [[False for x in range(6)] for y in range(7)]
		self.boardv = [[False for x in range(7)] for y in range(6)]

		#initialize pygame screen
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Boxes")
		#square owner map
		self.owner = [[0 for x in range(6)] for y in range(6)]

		#initialize player number
		self.num=0

		#initialize pygame clock
		self.clock=pygame.time.Clock()

		#server responses
		self.c.input1=[]

		#while loop until other player joins
		stop=True

		while stop:
			self.c.Loop()
			for event in self.c.input1:
				if event["action"]=="startgame":
					self.num=event["player"]
					self.gameid = event["gameid"]
					self.c.input1=[]
					stop=False
			sleep(0.01)

		#determine attributes from player #
		if self.num==0:
			self.turn=True
			self.marker = self.greenplayer
			self.othermarker = self.blueplayer
		else:
			self.turn=False
			self.marker=self.blueplayer
			self.othermarker = self.greenplayer

		#my score
		self.me=0

		# did i win?
		self.didiwin=False

		#other player's score
		self.otherplayer=0

		#game still running?
		self.running=True

		#did the user place a line between ten frames ago and now?
		self.justplaced=10
	def update(self):
		self.justplaced-=1
		# board full?
		if self.me+self.otherplayer==36:
			self.didiwin=True if self.me>self.otherplayer else False
			return 1

		#calculate score of board map
		self.me, self.otherplayer=calculate_score(self.owner)

		#clear the screen
		self.screen.fill(0)

		#sleep to make the game 60 fps
		self.clock.tick(60)

		#loop client qand recieve data from server
		self.c.Loop()

		#check queue for various server messages
		for event in self.c.input1:
			#my turn
			if event["action"]=="yourturn":
				#torf = short for true or false
				self.turn = event["torf"]
				#remove item from queue
				self.c.input1.remove(event)
			#placed line?
			if event["action"]=="place":
				#get attributes
				x = event["x"]
				y = event["y"]
				hv = event["hv"]

				#horizontal or vertical
				if hv=="h":
					self.boardh[y][x]=True
				else:
					self.boardv[y][x]=True
				#remove item from queue
				self.c.input1.remove(event)
			if event["action"]=="win":
				#set owner map
				self.owner[event["x"]][event["y"]]="win"
				self.boardh[event["y"]][event["x"]]=True
				self.boardv[event["y"]][event["x"]]=True
				self.boardh[event["y"]+1][event["x"]]=True
				self.boardv[event["y"]][event["x"]+1]=True
				#remove item from queue
				self.c.input1.remove(event)
				#add one point to my score
				self.me+=1
			if event["action"]=="lose":
				#set owner map to lost
				self.owner[event["x"]][event["y"]]="lose"
				self.boardh[event["y"]][event["x"]]=True
				self.boardv[event["y"]][event["x"]]=True
				self.boardh[event["y"]+1][event["x"]]=True
				self.boardv[event["y"]][event["x"]+1]=True
				#remove item from queue
				self.c.input1.remove(event)
				#add one to other players score
				self.otherplayer+=1
			if event["action"]=="close":
				exit()

		# draw the owner map
		for x in range(6):
			for y in range(6):
				if self.owner[x][y]!=0:
					if self.owner[x][y]=="win":
						self.screen.blit(self.marker, (x*64, y*64))
					if self.owner[x][y]=="lose":
						self.screen.blit(self.othermarker, (x*64, y*64))

		# This draws all of the lines other than the edges.
		for x in range(6):
			for y in range(6):
				if not self.boardh[y][x]:
					self.screen.blit(self.normallineh, [(x)*64, (y)*64])
				else:
					self.screen.blit(self.coollineh, [(x)*64, (y)*64])
				if not self.boardv[y][x]:
					self.screen.blit(self.normallinev, [(x)*64, (y)*64])
				else:
					self.screen.blit(self.coollinev, [(x)*64, (y)*64])
		# This draws the bottom and right edges.
		for edge in range(6):
			if not self.boardh[6][edge]:
				self.screen.blit(self.normallineh, [edge*64, 6*64])
			else:
				self.screen.blit(self.coollineh, [edge*64, 6*64])
			if not self.boardv[edge][6]:
				self.screen.blit(self.normallinev, [6*64, edge*64])
			else:
				self.screen.blit(self.coollinev, [6*64, edge*64])
		#HUD
		#create font
		myfont = pygame.font.SysFont(None, 32)
		#create text surface
		label = myfont.render("Your Turn:", 1, (255,255,255))
		#draw surface
		self.screen.blit(label, (10, 395))
		#same thing here
		myfont = pygame.font.SysFont(None, 64)
		score = myfont.render(str(self.me), 1, (255,255,255))
		myfont = pygame.font.SysFont(None, 20)
		scoretext = myfont.render("You", 1, (255,255,255))
		self.screen.blit(scoretext, (10, 425))
		self.screen.blit(score, (10, 435))
		myfont = pygame.font.SysFont(None, 64)
		score = myfont.render(str(self.otherplayer), 1, (255,255,255))
		myfont = pygame.font.SysFont(None, 20)
		scoretext = myfont.render("Other Player", 1, (255,255,255))
		self.screen.blit(scoretext, (220, 425))
		self.screen.blit(score, (300, 435))
		#draw indicator
		self.screen.blit(self.greenindicator if self.turn else self.redindicator, (195, 395))
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
		board=self.boardh if is_horizontal else self.boardv 
		isoutofbounds=False
		try: 
			if not board[ypos][xpos]: self.screen.blit(self.hoverlineh if is_horizontal else self.hoverlinev, [xpos*64, ypos*64])
		except:
			isoutofbounds=True
			pass
		#place a line if it hasn't already been placed
		if pygame.mouse.get_pressed()[0] and self.turn==True and not isoutofbounds and self.justplaced<=0:
			#wait ten frames before checking again.
			self.justplaced=10
			alreadyplaced=False
			if is_horizontal:
				if self.boardh[ypos][xpos]==True:
					alreadyplaced=True
				else:
					# boardh[ypos][xpos] = True
					pass
			else:
				if self.boardv[ypos][xpos]==True:
					alreadyplaced=True
				else:
					# boardv[ypos][xpos] = True
					pass
			self.turn=False
			if not alreadyplaced:
				#send place of line to server
				self.c.Send({"action":"place", "hv":"h" if is_horizontal else "v", "y":ypos, "x":xpos, "gameid": self.gameid, "player": self.num})
		for event in pygame.event.get():
			#quit if the quit button was pressed
			if event.type == pygame.QUIT:
				exit()
		#update the screen
		pygame.display.flip()
	def finished(self):
		self.screen.blit(self.gameover if not self.didiwin else self.winningscreen, (0,0))
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
			pygame.display.flip()	

bg=BoxesGame()
while 1:
	if bg.update()==1:
		break
bg.finished()

