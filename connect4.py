import numpy as np
# from numpy.core.fromnumeric import size
import pygame
import math
import sys

RED=(255, 0, 0)
BLUE=(0, 0, 255)
GREEN=(0, 255, 0)
YELLOW=(255, 255, 0)
BLACK=(0, 0, 0)

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

def draw_board(board):
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (col*SQUARESIZE, row* SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE) )
            pygame.draw.circle(screen, BLACK, (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if board[row][col]==1 :
                pygame.draw.circle(screen, RED, (int(col*SQUARESIZE+SQUARESIZE/2), height- int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[row][col]==2 :
                pygame.draw.circle(screen, YELLOW, (int(col*SQUARESIZE+SQUARESIZE/2), height- int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    pygame.display.update()



    
# create a board
board= create_board()
print_board(board)
game_over=False
turn=0

pygame.init()
SQUARESIZE=100
RADIUS=int(SQUARESIZE/2 - 5)

width=COLUMN_COUNT*SQUARESIZE
height=(ROW_COUNT+1)* SQUARESIZE

size=(width, height)

screen=pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont=pygame.font.SysFont("monospace",100)

while not game_over:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()

        if event.type==pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx=event.pos[0]
            if turn==0:
                pygame.draw.circle(screen, RED,(posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW,(posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type==pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,BLACK, (0,0,width,SQUARESIZE))
            # print(event.pos)
            # # Ask input
            if turn==0:
                posx= event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                # print(col)
                if is_valid_loaction(board, col):
                    row=get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        # print("Player one wins!")
                        label=myfont.render("Player1 Won!", 1, GREEN)
                        screen.blit(label, (40,10))
                        game_over=True
            
            else:
                posx= event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                # print(col)
                if is_valid_loaction(board, col):
                    row=get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        # print("Player two wins!")
                        label=myfont.render("Player2 Won!", 1, GREEN)
                        screen.blit(label, (40,10))
                        game_over=True
            print_board(board)
            draw_board(board)

            turn+=1
            turn=turn%2

            if game_over:
                pygame.time.wait(3000)
