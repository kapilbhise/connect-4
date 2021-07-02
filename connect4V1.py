import numpy as np
from numpy.core.fromnumeric import size
import pygame

ROW_COUNT=6
COLUMN_COUNT=7
# function to create a board
def create_board():
    board=np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

# function to  drop a piece
def drop_piece(board, row, col, piece):
    board[row][col]=piece

# function to check if the loaction is valid
def is_valid_loaction(board, col):
    return board[ROW_COUNT-1][col]==0 

# function to get next open row
def get_next_open_row(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0 :
            return row

# function to print the board in required order
def print_board(board):
    print(np.flip(board,0))

def winning_move(board, piece):
    # check horizontal locations
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT):
            if board[row][col]==piece and board[row][col+1]== piece and board[row][col+2]==piece and board[row][col+3]==piece:
                return True

    # check horizontal locations
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT-3):
            if board[row][col]==piece and board[row+1][col]== piece and board[row+2][col]==piece and board[row+3][col]==piece:
                return True

    # check positive diagonals
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT-3):
            if board[row][col]==piece and board[row+1][col+1]== piece and board[row+2][col+2]==piece and board[row+3][col+3]==piece:
                return True

    # check negative diagonals
    for col in range(COLUMN_COUNT-3):
        for row in range(3, ROW_COUNT):
            if board[row][col]==piece and board[row-1][col+1]== piece and board[row-2][col+2]==piece and board[row-3][col+3]==piece:
                return True


    
# create a board
board= create_board()
print_board(board)
game_over=False
turn=0

# pygame.init()
# SQUARESIZE=100
# width=COLUMN_COUNT*SQUARESIZE
# height=(ROW_COUNT+1)* SQUARESIZE

# size=(width, height)

# screen=pygame.display.set_mode(size)

while not game_over:
    # Ask input
    if turn==0:
        # Ask player one input
        col=int(input("Player one make your selection- "))
        # print(col)
        if is_valid_loaction(board, col):
            row=get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

            if winning_move(board, 1):
                print("Player one wins!")
                game_over=True
    
    else:
        # Ask player two input
        col=int(input("Player two make your selection- "))
        # print(col)
        if is_valid_loaction(board, col):
            row=get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board, 2):
                print("Player two wins!")
                game_over=True

    print_board(board)
    turn+=1
    turn=turn%2
