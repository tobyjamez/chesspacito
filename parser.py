import chess
import re
import pickle
import chess


class Board(chess.Board):
    def __init__(self, dest, *args, **kwargs):
        super(Board, self).__init__()
        self.dest = dest

    def save(self, dest):
        with open(dest, 'wb') as f:
            pickle.dump(self, f)

def chess_help(board):
    print("Legal moves:\n")
    print(board.legal_moves)

def load_board(origin):
    """
    Load a saved chess board from a file
    """
    with open(origin, 'rb') as f:
        return pickle.load(f)

def parse(board, message):
    if message in command_dict.keys():
        command_dict[message](board)
    else:
        try:
            board.push_san(message)
            board.save(board.dest)
            return str(board)
        except(Exception) as e:
           print("oops") 

command_dict = {'print': print,
                '?': chess_help}

