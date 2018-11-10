import chess
import pickle

def move(pos):
    board.push_san(pos)
    print(board)
    s = str(board.legal_moves)
    s=s.split('(')
    s1=s[1].split(')')
    if s1==['', '>']:
        print('Game Over')
    else: 
        print(s1[:-1])

def save(var,file):
    with open(file, 'wb') as f:
        pickle.dump(var, f)
        
                    
def load(var,file):
    with open(file,'rb') as f:
        var = pickle.load(f)
