# -*- coding: utf-8 -*-
"""
Created on Sun Feb 04 03:02:59 2018

@author: pushkar
"""

import pygame
import math
import time 
class BoxesGame():
    def __init__(self):
        #initialize variables for the current state
        self.hColor=[[0 for x in range(6)] for y in range(7)]
        self.vColor=[[0 for x in range(7)] for y in range(6)]
        self.boardh = [[False for x in range(6)] for y in range(7)]
        self.boardv = [[False for x in range(7)] for y in range(6)]
        #initialize variables for tracking the score
        self.score_player1=0;
        self.score_player2=0;
    def update(self):
    

        print 'Player 2'
        self.player2();
        print 'Player1'
        self.player1();
        
    # A function to lost all the possible moves 
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
    # gives the current state of the system
    def current_state(self):
        return self.boardh,self.boardv
    #checks if the score has been updated by a given move or not
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
    # function to actulally make a move
    def make_move(self,move,player_id):
        #print 'value before coming',self.boardh
        xpos=move[0];
        ypos=move[1];
        print xpos,ypos
        if(move[2]==1):# Vertical Matrices
            
            self.boardh[xpos][ypos]=True;
            
        if(move[2]==0):
            self.boardv[xpos][ypos]=True;
        #self.boardh_temp = self.boardh
        #self.boardv_temp = self.boardv
        score=self.increment_score(move,self.boardh,self.boardv);
        if(player_id==0):
            self.score_player1=self.score_player1+self.increment_score(move,self.boardh,self.boardv);
            
        if(player_id==1):
            self.score_player2=self.score_player2+self.increment_score(move,self.boardh,self.boardv);
            
       
        
    # function for printing the next state of the system    
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
    # function for 
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
        
        next_move=self.list_possible_moves(temp_h,temp_v);
        #print self.boardh_temp,self.boardv_temp
        #print next_move
        best_move=next_move[0];
        best_score=0;
        #print 'before loop'
        for move in next_move:
            
            temp_h,temp_v,score=self.next_state(move,temp_h,temp_v);
            #print score
            if(score>best_score):
                best_score=score;
                best_move=move;
        
        #print 'Player 1  next moves', next_move_list
        #print 'Player 1  move made', next_move_list[0];
        self.make_move(best_move,0);
        #print 'move made by player1', best_move
        
        #if(make_move(next))
    def player2(self):
        temp_h=self.boardh
        temp_v=self.boardv
        '''
        Call the minimax/alpha-beta pruning  function to return the optimal move
        '''
        
        ## change the next line of minimax/ aplpha-beta pruning according to your input and output requirments
        next_move=self.minimax();
        next_move_alpha=self.alphabetapruning();
        
        
        self.make_move(next_move,1);
        print 'move_made by player 1',next_move
        
    '''
    Write down the code for minimax to a certain depth do no implement minimax all the way to the final state. 
    '''
    
    
    def minimax(self):
        
        return [0,0,0];  
    '''
    Chenge the alpha beta pruning function to return the optimal move .
    '''    
    def alphabetapruning(self):
        return [0,0,0];
     
bg=BoxesGame();
while (bg.game_ends(bg.boardh,bg.boardv)==False):
    bg.update();
    print 'Player1 :score',bg.score_player1;
    print 'Player2:score',bg.score_player2;
    time.sleep(2)
time.sleep(10)
pygame.quit()