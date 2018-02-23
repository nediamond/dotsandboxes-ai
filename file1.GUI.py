# -*- coding: utf-8 -*-
"""
Created on Tue Feb 06 16:45:33 2018

@author: pushkar
"""

import pygame
import math
import time 
from random import choice
from pprint import pprint as pp
class BoxesandGridsGame():
	def __init__(self):
		pass
		#1
		pygame.init()
		pygame.font.init()
		width, height = 389, 489
		#2
		self.hColor=[[0 for x in range(6)] for y in range(7)]
		self.vColor=[[0 for x in range(7)] for y in range(6)]
		#initialize the screen
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Boxes")
		#3
		#initialize pygame clock
		self.clock=pygame.time.Clock()
		self.boardh = [[False for x in range(6)] for y in range(7)]
		self.boardv = [[False for x in range(7)] for y in range(6)]
		self.boardh_temp = self.boardh
		self.boardv_temp = self.boardv
		self.initGraphics();
		self.drawBoard();
		self.hColor=[[0 for x in range(6)] for y in range(7)]
		self.vColor=[[0 for x in range(7)] for y in range(6)]
		
		self.goal_x=6;
		self.goal_y=5;
		self.initial_move=[0,0,0];
		
		
		self.score_player1=0;
		self.score_player2=0;
		
	def update(self):
	#sleep to make the game 60 fps
		self.clock.tick(60)

	#clear the screen
		self.screen.fill(0)
		self.drawBoard()
		self.drawHUD()

		for event in pygame.event.get():
		#quit if the quit button was pressed
			if event.type == pygame.QUIT:
				exit()
		print 'before making a move'
		self.player2();
		print 'move made player 2'
		self.player1();
		print 'move made player 1'
	#update the screen
	
		pygame.display.flip()
	def initGraphics(self):
		self.normallinev=pygame.image.load("normalline.png")
		self.normallineh=pygame.transform.rotate(pygame.image.load("normalline.png"), -90)
		self.bar_donev=pygame.image.load("bar_done.png")
		self.bar_doneh=pygame.transform.rotate(pygame.image.load("bar_done.png"), -90)
		self.bar_donev_r=pygame.image.load("bar_done_red.png")
		self.bar_doneh_r=pygame.transform.rotate(pygame.image.load("bar_done_red.png"), -90)
		self.bar_donev_g=pygame.image.load("bar_done_green.png")
		self.bar_doneh_g=pygame.transform.rotate(pygame.image.load("bar_done_green.png"), -90)
		self.bar_donev_r_l=pygame.image.load("bar_done_light_red.png")
		self.bar_doneh_r_l=pygame.transform.rotate(pygame.image.load("bar_done_light_red.png"), -90)
		self.bar_donev_g_l=pygame.image.load("bar_done_light_green.png")
		self.bar_doneh_g_l=pygame.transform.rotate(pygame.image.load("bar_done_light_green.png"), -90)
		self.hoverlinev=pygame.image.load("hoverline.png")
		self.hoverlineh=pygame.transform.rotate(pygame.image.load("hoverline.png"), -90)
		self.separators=pygame.image.load("separators.png")
		self.redindicator=pygame.image.load("redindicator.png")
		self.greenindicator=pygame.image.load("greenindicator.png")
		self.greenplayer=pygame.image.load("greenplayer.png")
		self.blueplayer=pygame.image.load("blueplayer.png")
		self.winningscreen=pygame.image.load("youwin.png")
		self.gameover=pygame.image.load("gameover.png")
		self.score_panel=pygame.image.load("score_panel.png")
	def drawBoard(self):
		for x in range(6):
			for y in range(7):
				
				if  (self.hColor[y][x]==-1):
					self.screen.blit(self.bar_doneh_r, [(x)*64+5, (y)*64])
				elif  self.hColor[y][x]==1:
					self.screen.blit(self.bar_doneh_g, [(x)*64+5, (y)*64])
				else:
					self.screen.blit(self.bar_doneh, [(x)*64+5, (y)*64])
					
		for x in range(7):
			for y in range(6):
				
				if  (self.vColor[y][x]==-1):
					self.screen.blit(self.bar_donev_r, [(x)*64, (y)*64+5])
				elif  self.vColor[y][x]==1:
					self.screen.blit(self.bar_donev_g, [(x)*64, (y)*64+5])
				else:
					self.screen.blit(self.bar_donev, [(x)*64, (y)*64+5])
		  
				  
		for x in range(7):
			for y in range(7):
				self.screen.blit(self.separators, [x*64, y*64])
				
	def drawHUD(self):
	#draw the background for the bottom:
		self.screen.blit(self.score_panel, [0, 389])
		#create font
		myfont = pygame.font.SysFont(None, 32)

		#create text surface
		label = myfont.render("Player 1:", 1, (255,255,255))

		#draw surface
		self.screen.blit(label, (10, 400))
		#same thing here
		myfont64 = pygame.font.SysFont(None, 64)
		myfont20 = pygame.font.SysFont(None, 20)

		scoreme = myfont64.render(str(self.score_player1), 1, (255,255,255))
		scoreother = myfont64.render(str(self.score_player2), 1, (255,255,255))
		scoretextme = myfont20.render("Player1", 1, (255,255,255))
		scoretextother = myfont20.render("Player2", 1, (255,255,255))
		
		self.screen.blit(scoretextme, (10, 425))
		self.screen.blit(scoreme, (10, 435))
		self.screen.blit(scoretextother, (280, 425))
		self.screen.blit(scoreother, (340, 435))
	def finished(self):
		self.screen.blit(self.winningscreen, (0,0))
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
			pygame.display.flip()   
		  

	def next_possible_moves(self,move):
		#make the move true if the last move is not true to be true in the psuedo list
		if(move[2]==1):
			self.boardh_temp[move[0]][move[1]]=True;
		elif(move[2]==0):
			self.boardv_temp[move[0]][move[1]]=True;
		else: 
			print ("Invalid move");
		next_moves=[];
		
		for x in range (7):
			for y in range(6):
				if(self.boardh_temp[x][y]==False):
					next_moves.append([x,y,1]); # append all horizontal moves
				
		for x in range (6):
			for y in range(7):
				if(self.boardv_temp[x][y]==False):
					next_moves.append([x,y,0]); # append all horizontal moves
		
				
		return next_moves 
	def list_possible_moves(self,state_h,state_v):
		#make the move true if the last move is not true to be true in the psuedo list
		
		next_moves=[];
		for x in range (7):
			for y in range(6):
				if(state_h[x][y]==False):
					next_moves.append([x,y,1]); # append all horizontal moves
				
				
				
		for x in range (6):
			for y in range(7):
				if(state_v[x][y]==False):
					next_moves.append([x,y,0]); # append all horizontal moves
				
		
				
		return next_moves
	def current_state(self):
		return self.boardh,self.boardv
	
	def increment_score(self,move,h_matrix,v_matrix):
		temp_score=0;
		xpos=move[0];
		ypos=move[1];
		if(move[2]==0): # vertical matrices
			if(ypos==0):# left most edge
				if(h_matrix[xpos][ypos]==True and h_matrix[xpos+1][ypos]==True and v_matrix[xpos][ypos+1]==True):
					temp_score=1;
			elif(ypos==6):# left most edge   
				if(h_matrix[xpos][ypos-1]==True and h_matrix[xpos+1][ypos-1]==True and v_matrix[xpos][ypos-1]==True):
					temp_score=1;     
			else:
				if(h_matrix[xpos][ypos]==True and h_matrix[xpos+1][ypos]==True and v_matrix[xpos][ypos+1]==True):
					temp_score=temp_score+1;
				if(h_matrix[xpos][ypos-1]==True and h_matrix[xpos+1][ypos-1]==True and v_matrix[xpos][ypos-1]==True):
					temp_score=temp_score+1;
					
		if(move[2]==1): # horizontal matrices
			if(xpos==0):
				if(v_matrix[xpos][ypos]==True and v_matrix[xpos][ypos+1]==True and h_matrix[xpos+1][ypos]==True):
					temp_score=1;
			elif(xpos==6):
				if(v_matrix[xpos-1][ypos]==True and v_matrix[xpos-1][ypos+1]==True and h_matrix[xpos-1][ypos]==True):
					temp_score=1;
				
			else:
				if(v_matrix[xpos][ypos]==True and v_matrix[xpos][ypos+1]==True and h_matrix[xpos+1][ypos]==True):
					temp_score=temp_score+1;
				if(v_matrix[xpos-1][ypos]==True and v_matrix[xpos-1][ypos+1]==True and h_matrix[xpos-1][ypos]==True):
					temp_score=temp_score+1;
				
				
			
		return temp_score;
	def make_move(self,move,player_id):
		print 'value before coming',self.boardh
		xpos=move[0];
		ypos=move[1];
		#print xpos,ypos
		if(move[2]==1):# Vertical Matrices
			
			self.boardh[xpos][ypos]=True;
			
		if(move[2]==0):
			self.boardv[xpos][ypos]=True;
		self.boardh_temp = self.boardh
		self.boardv_temp = self.boardv
		#score=self.increment_score(move,self.boardh,self.boardv);
		#print self.boardh,self.boardv
		### Leave space here for player color change 
		
		
		if(player_id==0):
			self.score_player1=self.score_player1+self.increment_score(move,self.boardh,self.boardv);
			if(move[2]==1):
				self.hColor[xpos][ypos]=-1;
			if(move[2]==0):
				self.vColor[xpos][ypos]=-1;
			
		if(player_id==1):
			self.score_player2=self.score_player2+self.increment_score(move,self.boardh,self.boardv);
			if(move[2]==1):
				self.hColor[xpos][ypos]=1;
			if(move[2]==0):
				self.vColor[xpos][ypos]=1;
	def next_state(self,move,state_h,state_v):
		xpos=move[0];
		ypos=move[1];
		score=self.increment_score(move,state_h,state_v);
		if(move[2]==0):#vetical matrices
			state_v[xpos][ypos]=True;
			self.boardv[xpos][ypos]=False
		if(move[2]==1):#horizontal matrices
			state_h[xpos][ypos]=True;
			self.boardh[xpos][ypos]=False
		return state_h,state_v,score;
	def game_ends(self,temp_h,temp_v):
		count=True;
		for x in range(6):
			for y in range(7):
				if not temp_h[y][x]:
					count=False;
		for x in range(7):
			for y in range(6):
				if not temp_v[y][x]:
					count=False;
		return count;
	
	def player1(self):
		temp_h=self.boardh
		temp_v=self.boardv
		next_move=self.other_minimax();

		#next_move_alpha=self.alphabetapruning();
		
		
		self.make_move(next_move,0);
		print 'move_made by player 1',next_move
		# next_move=self.list_possible_moves(temp_h,temp_v);
		
		# best_move=next_move[0];
		# best_score=0;
		
		# for move in next_move:
			
		#     temp_h,temp_v,score=self.next_state(move,temp_h,temp_v);
			
		#     if(score>best_score):
		#         best_score=score;
		#         best_move=move;
		
		
		# self.make_move(best_move,0);
		
	'''
	You will make changes to the code from this part onwards
	'''
	def player2(self):
		temp_h=self.boardh
		temp_v=self.boardv
		'''
		Call the minimax/alpha-beta pruning  function to return the optimal move
		'''
		
		## change the next line of minimax/ aplpha-beta pruning according to your input and output requirments
		next_move=self.minimax(1, 1)[0];
		#next_move_alpha=self.alphabetapruning();
		
		
		self.make_move(next_move,1);
		print 'move_made by player 2',next_move
		
	'''
	Write down the code for minimax to a certain depth do no implement minimax all the way to the final state. 
	'''
	
	# def pos_next_state_generator(move,state_h,state_v):
	#     temp_h=self.boardh
	#     temp_v=self.boardv
	#     for x,y in product(range(len(state_h)),range(len(state_v))):
	#         if state_h[x][y] == False:
	#             yield self.next_state([x, y, 1],temp_h,temp_v):
	#         if state_v[x][y] == False:

	# needs to return just move, not tuple
	# todo: examine this guys helper functions (possible moves, incrmentscore)
	# USE STACK NOT RECURSION!!
	# Pruning strat: dynamic depth based on len(pos_moves)?
	# Maybe evluate should always eval wrt to player two
	# Deep cutoff, iterative deepening?
	def minimax(self, depth, player_id, pmove=None):
		if pmove:
			self.make_move_noviz(pmove, (player_id+1)%2)

		pos_moves = self.list_possible_moves(self.boardh,self.boardv)

		if len(pos_moves) == 1:
			score = self.score_player2 if player_id else self.score_player1
			retval = (pos_moves[0], (score*4)+4)

		elif depth == 0:
			move = max(pos_moves, key=lambda move: self.evaluate(move,self.boardh,self.boardv))
			self.make_move_noviz(move, player_id)
			score = self.score_player2 if player_id else self.score_player1
			retval = (move, (score*4)+self.evaluate(move,self.boardh,self.boardv))
			self.unmake_move_noviz(move, player_id)

		else:
			op_moves = map(lambda x: self.minimax(depth-1, (player_id+1)%2, pmove=x), pos_moves)
			move = pos_moves[op_moves.index(min(op_moves, key=lambda x:x[1]))]
			self.make_move_noviz(move, player_id)
			score = self.score_player2 if player_id else self.score_player1
			retval = (move, (score*4)+self.evaluate(move,self.boardh,self.boardv))
			self.unmake_move_noviz(move, player_id)

		if pmove:
			self.unmake_move_noviz(pmove, (player_id+1)%2)

		return retval

	def make_move_noviz(self, move, player_id):
		self.make_move_noscore(move)
		if(player_id==0):
			self.score_player1 += self.increment_score(move,self.boardh,self.boardv)
		if(player_id==1):
			self.score_player2 += self.increment_score(move,self.boardh,self.boardv)


	def unmake_move_noviz(self, move, player_id):
		self.unmake_move(move)
		if(player_id==0):
			self.score_player1 -= self.increment_score(move,self.boardh,self.boardv)
		if(player_id==1):
			self.score_player2 -= self.increment_score(move,self.boardh,self.boardv)


	def other_minimax(self):
		temp_h=self.boardh
		temp_v=self.boardv
		pos_moves = self.list_possible_moves(temp_h,temp_v);
		ratings = map(lambda move: self.evaluate(move, temp_h, temp_v), pos_moves)

		return pos_moves[ratings.index(max(ratings))]
	# def other_minimax(self):
	#     temp_h=self.boardh
	#     temp_v=self.boardv
	#     pos_moves = self.list_possible_moves(temp_h,temp_v);
	#     best_moves, ratings = zip(*self.alphabetapruning(pos_moves, ratings))
	#     exp_scores = []
	#     for move in best_moves:
	#         move_q = [move]
	#         pos_moves.remove(move)

	#         for _move in move_q:
	#             pos_moves.append(_move)

	#     return choice(best_moves)
	# '''
	# Chenge the alpha beta pruning function to return the optimal move .
	# '''    
	# def alphabetapruning(self, moves, ratings):
	# 	max_rating = max(ratings)
	# 	#best_moves = filter(lambda x: x[1]>=max_rating-2, zip(moves, ratings))
	# 	best_moves = filter(lambda x: x[1]==max_rating, zip(moves, ratings))

	# 	return best_moves;
	
	'''
	Write down you own evaluation strategy in the evaluation function

	open to tweaking:
	+3 for each new completed square
	+1 for each new half completed square
	-2 for each new 3/4 completed square
	'''
	def _evaluate(self, numsides):
		if numsides == 4: return 4
		if numsides == 2: return 1
		if numsides == 3: return -2 # is making 2 threes better than making 1 three?
		if numsides == 1: return 0

	# can simplify/remove if statements here
	def evaluate(self, move,state_h,state_v):
		x = move[0]
		y = move[1]
		if move[2]==0: # Vertical, need to check top and bottom squares
			square_1 = 1 # Left Square
			if y > 0 and x < len(state_h)-1 : 
				square_1 += state_h[x][y-1] + state_h[x+1][y-1] + state_v[x][y-1]
			elif y > 0 and x < len(state_h): 
				square_1 += state_h[x][y-1] + state_v[x][y-1]

			square_2 = 1 # Right Square
			if (x < len(state_h) and y < len(state_h[0])):
				square_2 += state_h[x][y]
				if x < len(state_h)-1:
					square_2 += state_h[x+1][y]
				if x < len(state_v) and y < len(state_v[0])-1:
					square_2 += state_v[x][y+1]

		elif move[2]==1:
			square_1 = 1 # Top Square
			if x > 0 and y < len(state_v[0])-1: 
				square_1 += state_h[x-1][y] + state_v[x-1][y] + state_v[x-1][y+1]
			elif x > 0 and y < len(state_v[0]): 
				square_1 += state_h[x-1][y] + state_v[x-1][y]

			square_2 = 1 # Bottom Square
			if (x < len(state_v) and y < len(state_v[0])):
				square_2 += state_v[x][y]
				if x < len(state_h)-1 and y < len(state_h[0]):
					square_2 += state_h[x+1][y]
				if y < len(state_v[0])-1:
					square_2 += state_v[x][y+1]
		try:
			if square_1 == 3 and square_2 == 3:
				return 3
			return self._evaluate(square_1) + self._evaluate(square_2)
		except NameError:
			raise Exception("Unexpected Orientation Value When Evaluating Move")

	def make_move_noscore(self, move):
		xpos=move[0];
		ypos=move[1];

		if(move[2]==1):
			self.boardh[xpos][ypos]=True;
		if(move[2]==0):
			self.boardv[xpos][ypos]=True;

	def unmake_move(self, move):
		xpos=move[0];
		ypos=move[1];

		if(move[2]==1):
			self.boardh[xpos][ypos]=False;
		if(move[2]==0):
			self.boardv[xpos][ypos]=False;

	# Independently evaluates a set of moves after another set of moves have been applied
	def evaluate_moves_after_moves(self, prev_move_queue, movelist, state_h, state_v):
		for pmove in prev_move_queue:
			self.make_move_noscore(pmove)

		retval = map(lambda move: self.evaluate(move, state_h, state_v), movelist)

		for pmove in prev_move_queue:
			self.unmake_move(pmove)

		return retval

	def list_moves_after_moves(self, prev_move_queue, state_h, state_v):
		for pmove in prev_move_queue:
			self.make_move_noscore(pmove)
		
		retval = self.list_possible_moves(state_h, state_v)

		for pmove in prev_move_queue:
			self.unmake_move(pmove)

		return retval


	 
bg=BoxesandGridsGame();
while (bg.game_ends(bg.boardh,bg.boardv)==False):
	bg.update();
	print 'Player1 score:',bg.score_player1;
	print 'Player2 score:',bg.score_player2;
	time.sleep(2)
time.sleep(10)
pygame.quit()