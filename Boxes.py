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
hoverlineh=pygame.transform.rotate(pygame.image.load("hoverline.png"), -90)
coollineh=pygame.transform.rotate(pygame.image.load("coolline.png"), -90)
board=[]
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
else:
	turn=False
while 1:
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
	screen.fill(0)
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
	mouse = pygame.mouse.get_pos()
	#left or right
	x=["","","",""]

	xpos = int(math.ceil((mouse[0]-32)/64.0))
	ypos = int(math.ceil((mouse[1]-32)/64.0))

	is_horizontal = abs(mouse[1] - ypos*64) < abs(mouse[0] - xpos*64)

	ypos = ypos - 1 if mouse[1] - ypos*64 < 0 and not is_horizontal else ypos
	xpos = xpos - 1 if mouse[0] - xpos*64 < 0 and is_horizontal else xpos

	print mouse, xpos, ypos, is_horizontal

	screen.blit(hoverlineh if is_horizontal else hoverlinev, [xpos*64, ypos*64])

	if pygame.mouse.get_pressed()[0] and turn==True:
		if is_horizontal:
			boardh[ypos][xpos] = True
		else:
			boardv[ypos][xpos] = True
		print {"hv":"h" if is_horizontal else "v","y":ypos, "x":xpos}
		c.Send({"action":"place", "hv":"h" if is_horizontal else "v", "y":ypos, "x":xpos})
		turn=False

	if 0:
		if mouse[0]%64<32:
			x[0] = "left"
			x[2] = 64-mouse[0]%64
		else:
			x[0] = "right"
			x[2] = mouse[0]%64
		if mouse[1]%64<32:
			x[1] = "top"
			x[3] = 64-mouse[1]%64
		else:
			x[1] = "bottom"
			x[3] = mouse[1]%64
		if x[2]<x[3]:
			if x[1]=="top":
				if (int(math.ceil(mouse[0]/64))) <= 6 and (int(math.ceil(mouse[1]/64)))<=6:
					screen.blit(hoverlineh, [(int(math.ceil(mouse[0]/64)))*64, (int(math.ceil(mouse[1]/64)))*64])
					if pygame.mouse.get_pressed()[0] and turn==True:
						boardh[(int(math.ceil(mouse[1]/64)))][(int(math.ceil(mouse[0]/64)))] = True
						print {"y":(int(math.ceil(mouse[1]/64))), "x":(int(math.ceil(mouse[0]/64)))}
						c.Send({"action":"place", "hv":"h", "y":(int(math.ceil(mouse[1]/64))), "x":(int(math.ceil(mouse[0]/64)))})
						turn=False
			elif x[1]=="bottom":
				if (int(math.ceil(mouse[0]/64))) <= 6 and (int(math.ceil(mouse[1]/64))+1)<=6:
					screen.blit(hoverlineh, [(int(math.ceil(mouse[0]/64)))*64, (int(math.ceil(mouse[1]/64))+1)*64])
					if pygame.mouse.get_pressed()[0] and turn==True:
						boardh[(int(math.ceil(mouse[1]/64)))+1][(int(math.ceil(mouse[0]/64)))] = True
						print {"action":"place", "hv":"h", "y":(int(math.ceil(mouse[1]/64)))+1, "x":(int(math.ceil(mouse[0]/64)))}
						c.Send({"action":"place", "hv":"h", "y":(int(math.ceil(mouse[1]/64)))+1, "x":(int(math.ceil(mouse[0]/64)))})
						turn=False
		else:
			if x[0]=="left":
				if (int(math.ceil(mouse[0]/64))) < 6 and (int(math.ceil(mouse[1]/64)))<6:
					screen.blit(hoverlinev, [(int(math.ceil(mouse[0]/64)))*64, (int(math.ceil(mouse[1]/64)))*64])
					if pygame.mouse.get_pressed()[0] and turn==True:
						boardv[(int(math.ceil(mouse[1]/64)))][(int(math.ceil(mouse[0]/64)))] = True
						print {"action":"place", "hv":"v", "y":(int(math.ceil(mouse[1]/64))), "x":(int(math.ceil(mouse[0]/64)))}
						c.Send({"action":"place", "hv":"v", "y":(int(math.ceil(mouse[1]/64))), "x":(int(math.ceil(mouse[0]/64)))})
						turn=False
			elif x[0]=="right":
				if (int(math.ceil(mouse[0]/64)))+1 < 6 and (int(math.ceil(mouse[1]/64)))<6:
					screen.blit(hoverlinev, [(int(math.ceil(mouse[0]/64))+1)*64, (int(math.ceil(mouse[1]/64)))*64])
					if pygame.mouse.get_pressed()[0] and turn==True:
						boardv[(int(math.ceil(mouse[1]/64)))][(int(math.ceil(mouse[0]/64)))+1] = True
						print {"action":"place", "hv":"v", "y":(int(math.ceil(mouse[1]/64))), "x":(int(math.ceil(mouse[0]/64)))+1}
						c.Send({"action":"place", "hv":"v", "y":(int(math.ceil(mouse[1]/64))), "x":(int(math.ceil(mouse[0]/64)))+1})
						turn=False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
	pygame.display.flip()