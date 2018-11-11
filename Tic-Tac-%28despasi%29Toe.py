
# coding: utf-8

# In[ ]:

import os
import time 
import random


# In[ ]:

board = [" "," "," "," "," "," "," "," "," "," "]


# In[ ]:

def print_board():
    
    print(' '+board[1]+' | '+board[2]+' | '+board[3]+' ')
   
    print('---|---|---')
   
    print(' '+board[4]+' | '+board[5]+' | '+board[6]+' ')
    
    print('---|---|---')
    
    print(' '+board[7]+' | '+board[8]+' | '+board[9]+' ')
   


# In[ ]:

while True:
    os.system('clear')
    print_board()
    choiceX = input('Please choose a place to put X.')
    choiceX = int(choiceX)
    if board[choiceX] == " ":
        board[choiceX] = 'X'
    else:
        print('Invalid entry')
        time.sleep(1)
    if ((board[1] == 'X' and board[2] == 'X' and board[3] == 'X') 
        or (board[4] == 'X' and board[5] == 'X' and board[6] == 'X') 
        or (board[7] == 'X' and board[8] == 'X' and board[9] == 'X') 
        or (board[1] == 'X' and board[4] == 'X' and board[7] == 'X') 
        or (board[2] == 'X' and board[5] == 'X' and board[8] == 'X') 
        or (board[3] == 'X' and board[6] == 'X' and board[9] == 'X')
        or (board[1] == 'X' and board[5] == 'X' and board[9] == 'X')
        or (board[3] == 'X' and board[5] == 'X' and board[7] == 'X')):
        print_board()
        print('X wins!')
        
        break
        
    print_board()
    choiceO = input('Please choose a place to put O.')
    choiceO = int(choiceO)
    if board[choiceO] == " ":
        board[choiceO] = 'O'
    else:
        print('Invalid entry')
        time.sleep(1)
    if ((board[1] == 'O' and board[2] == 'O' and board[3] == 'O') 
        or (board[4] == 'O' and board[5] == 'O' and board[6] == 'O') 
        or (board[7] == 'O' and board[8] == 'O' and board[9] == 'O') 
        or (board[1] == 'O' and board[4] == 'O' and board[7] == 'O') 
        or (board[2] == 'O' and board[5] == 'O' and board[8] == 'O') 
        or (board[3] == 'O' and board[6] == 'O' and board[9] == 'O')
        or (board[1] == 'O' and board[5] == 'O' and board[9] == 'O')
        or (board[3] == 'O' and board[5] == 'O' and board[7] == 'O')):
        print_board()
        print('O wins!')
        
        break  


# In[ ]:



