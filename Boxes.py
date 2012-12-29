import pygame
import math
import copy
import client
pygame.init()
c = client.Client()
width, height = 389, 500
normallinev=pygame.image.load("normalline.png")
coollinev=pygame.image.load("coolline.png")
normallineh=pygame.transform.rotate(pygame.image.load("normalline.png"), -90)
hoverlinev=pygame.image.load("hoverline.png")
redindicator=pygame.image.load("redindicator.png")
greenindicator=pygame.image.load("greenindicator.png")
greenplayer=pygame.image.load("greenplayer.png")
blueplayer=pygame.image.load("blueplayer.png")
hoverlineh=pygame.transform.rotate(pygame.image.load("hoverline.png"), -90)
coollineh=pygame.transform.rotate(pygame.image.load("coolline.png"), -90)
board=[]
win = [[0 for x in range(6)] for y in range(6)]
turn = True
boardh = [[False for x in range(6)] for y in range(7)]
boardv = [[False for x in range(7)] for y in range(6)]
#usage: boardX[x][y]
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bunnies and Badgers")
num=10
clock=pygame.time.Clock()
while 1:
	c.Loop()
	if c.input1["action"]=="receivedata":
		num=c.input1["player"]
		break
if num==0:
	turn=True
	marker = greenplayer
	othermarker = blueplayer
else:
	turn=False
	marker=blueplayer
	othermarker = greenplayer
while 1:
	screen.fill(0)
	clock.tick(48)
	c.Loop()
	if c.input1["action"]=="place":
		turn=True
		x = c.input1["x"]
		y = c.input1["y"]
		hv = c.input1["hv"]
		if hv=="h":
			boardh[y][x]=True
		else:
			boardv[y][x]=True
		c.input1 = {"action":"None"}
	elif c.input1["action"]=="win":
		win[c.input1["x"]][c.input1["y"]]=num
		turn = False
	elif c.input1["action"]=="lose":
		if num==2:
			win[c.input1["x"]][c.input1["y"]]=1
		elif num==1:
			win[c.input1["x"]][c.input1["y"]]=2
		turn=True
	for x in range(6):
		for y in range(6):
			if win[x][y]==num+1:
				screen.blit(greenplayer if not num else blueplayer, (x*64, y*64))
				print "win"
			if win[x][y]!=num+1 and win[x][y]!=0:
				print "lose"
				screen.blit(greenplayer if num else blueplayer, (x*64, y*64))
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
	myfont = pygame.font.SysFont("monospace", 32)
	label = myfont.render("Your Turn:", 1, (255,255,255))
	screen.blit(label, (10, 395))
	screen.blit(greenindicator if turn else redindicator, (195, 395))
	mouse = pygame.mouse.get_pos()
	#left or right
	x=["","","",""]

	xpos = int(math.ceil((mouse[0]-32)/64.0))
	ypos = int(math.ceil((mouse[1]-32)/64.0))

	is_horizontal = abs(mouse[1] - ypos*64) < abs(mouse[0] - xpos*64)

	ypos = ypos - 1 if mouse[1] - ypos*64 < 0 and not is_horizontal else ypos
	xpos = xpos - 1 if mouse[0] - xpos*64 < 0 and is_horizontal else xpos


	screen.blit(hoverlineh if is_horizontal else hoverlinev, [xpos*64, ypos*64])

	if pygame.mouse.get_pressed()[0] and turn==True:
		if is_horizontal:
			boardh[ypos][xpos] = True
		else:
			boardv[ypos][xpos] = True
		c.Send({"action":"place", "hv":"h" if is_horizontal else "v", "y":ypos, "x":xpos})
		turn=False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
	pygame.display.flip()