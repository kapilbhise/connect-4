import numpy as np
# from numpy.core.fromnumeric import size
import random
import pygame
import sys
import math

# colors
RED = (255,0,0)
BLUE = (0,0,255)
GREEN=(0,255,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)

# rows and columns
ROW_COUNT = 6
COLUMN_COUNT = 7

# players
PLAYER = 0
AI = 1

# value at specific pint in matrix
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

# connect 4
WINDOW_LENGTH = 4

# function to create a board
def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

# function to drop piece
def drop_piece(board, row, col, piece):
	board[row][col] = piece

# function to check if location is valid
def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

# function to get next open row
def get_next_open_row(board, col):
	for row in range(ROW_COUNT):
		if board[row][col] == 0:
			return row

# function to print board
def print_board(board):
	print(np.flip(board, 0))

# winning move
def winning_move(board, piece):
	# Check horizontal locations 
	for col in range(COLUMN_COUNT-3):
		for row in range(ROW_COUNT):
			if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
				return True

	# Check vertical locations 
	for col in range(COLUMN_COUNT):
		for row in range(ROW_COUNT-3):
			if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
				return True

	# Check positive diaganols
	for col in range(COLUMN_COUNT-3):
		for row in range(ROW_COUNT-3):
			if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
				return True

	# Check negative diaganols
	for col in range(COLUMN_COUNT-3):
		for row in range(3, ROW_COUNT):
			if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
				return True

# function to find score for given window
def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

# Scoring positions
def score_position(board, piece):
	score = 0

	# score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	# score horizontal
	for row in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[row,:])]
		for col in range(COLUMN_COUNT-3):
			window = row_array[col:col+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	# score vertical
	for col in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,col])]
		for row in range(ROW_COUNT-3):
			window = col_array[row:row+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## score positive diagonal
	for row in range(ROW_COUNT-3):
		for col in range(COLUMN_COUNT-3):
			window = [board[row+i][col+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	# score negative diagonal
	for row in range(ROW_COUNT-3):
		for col in range(COLUMN_COUNT-3):
			window = [board[row+3-i][col+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

# check if it is terminal node
def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# minimax algo
def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

# function to get list of valid locations
def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

# function to pick best move
def pick_best_move(board, piece):

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

# function to draw board
def draw_board(board):
	for col in range(COLUMN_COUNT):
		for row in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (col*SQUARESIZE, row*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for col in range(COLUMN_COUNT):
		for row in range(ROW_COUNT):		
			if board[row][col] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(col*SQUARESIZE+SQUARESIZE/2), height-int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[row][col] == AI_PIECE: 
				pygame.draw.circle(screen, YELLOW, (int(col*SQUARESIZE+SQUARESIZE/2), height-int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)


turn = random.randint(PLAYER, AI)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			# print(event.pos)
			# player
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, PLAYER_PIECE)

					if winning_move(board, PLAYER_PIECE):
						label = myfont.render("Player 1 wins!!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True

					turn += 1
					turn = turn % 2

					print_board(board)
					draw_board(board)


	# AI
	if turn == AI and not game_over:				

		#col = random.randint(0, COLUMN_COUNT-1)
		#col = pick_best_move(board, AI_PIECE)
		col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

		if is_valid_location(board, col):
			#pygame.time.wait(500)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_PIECE)

			if winning_move(board, AI_PIECE):
				label = myfont.render("Player 2 wins!!", 1, YELLOW)
				screen.blit(label, (40,10))
				game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)