# -*- coding: utf-8 -*-
"""
Created on Wed Feb 07 04:37:34 2018

@author: pushkar
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 06 16:45:33 2018

@author: pushkar
"""

'''
This is version of the game that has only been created for the users to get familiar with the game .
There are a series of exercises that will allow you to get familiar with the settings of the game.
I request you to go down and uncomment that different parts of the game
'''
import pygame
import math
import time 
class PracticeBoxesandGridGame():
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
       #print 'value before coming',self.boardh
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
                print xpos,ypos
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
gridgame=PracticeBoxesandGridGame();
'''
 
Uncomment the following sections one after the other . Press Ctrl+C to break the game 
'''

'''
 Making a move.A move is made using make_move command. There are two examples that are given below.
Please uncomment them one after the other and run each block before running the next block.
'''
 #Block 1
move1=[0,1,0] # vertical move
gridgame.make_move(move1,1);

#Block2 
#move2=[1,0,1]# vertical move
#gridgame.make_move(move2,1);

#Block 3
#move3=[0,0,0]
#gridgame.make_move(move3,1)

'''
Checking the score associated with a given move
'''
  
# Block 4 

#gridgame.make_move([2,3,0],1)
#gridgame.make_move([3,3,0],1)
#gridgame.make_move([2,4,0],1)
#gridgame.make_move([3,4,0],1)
#gridgame.make_move([4,3,1],1) 
#gridgame.make_move([2,3,1],1)      
''' 
Getting the current state of the system 
'''
#Block 5
#h_matrix,v_matrix=gridgame.current_state()
#print ' Horizontal matrix', h_matrix
#print ' vertical matrix',v_matrix

'''
Finding the socre for a given move
'''
#Block 6
#next_move1=[3,3,1];
#score=gridgame.increment_score(next_move1,h_matrix,v_matrix);
#print 'Potential Score due to the move',score

#next_move2=[0,0,1];
#score=gridgame.increment_score(next_move2,h_matrix,v_matrix);
#print 'Potential Score due to the move',score


'''
List all possible future moves given the current state
'''
# Block 7
#possible_moves=gridgame.list_possible_moves(h_matrix,v_matrix)
#print 'possible moves',possible_moves

'''
List all the next states in a given a move
'''
#Block 8
#state_h,state_v,score=gridgame.next_state(next_move1,h_matrix,v_matrix)
#print 'horizontal matrix for the next state',state_h
#print 'vertical matrix for the next state', state_v
#print 'Potential score due the the next move', score


    
   
   
     
#bg=PracticeBoxesandGridGame();
while (1):
    gridgame.update();
  
    time.sleep(2)