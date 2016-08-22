# coding: utf-8
import sys
import pygame
from pygame.locals import *
from sys import exit
from random import *
import random


ROWNUM = 20    
COLNUM = 16    
CELLNUM = ROWNUM * COLNUM 
LEN = 32  
SCREEN_SIZE = ((COLNUM+5) * LEN, ROWNUM * LEN)
BG_COLOR = (0,0,0)
FONT_COLOR = (255,255,255)
ORIGIN_POS = 8

O = (
	[(0,0), (-1,0),(-1,1),(0,1)],
	(244,223,131),
	)

I = (
	[(0,0), (-2,0),(-1,0),(1,0)],
	[(0,0), (0,-1),(0,1),(0,2)],
	(218,117,189),
	)


L = (
	[(0,0), (-1,0),(1,0),(-1,1)],
	[(0,0), (0,1),(0,-1),(-1,-1)],
	[(0,0), (-1,0), (1,0), (1,-1)],
	[(0,0), (0,-1), (0,1), (1,1)],
	(100,180,120),
	)

J = (
	[(0,0), (-1,0),(1,0),(1,1)],
	[(0,0), (-1,1), (0,1), (0,-1)],
	[(0,0), (-1,-1), (-1,0), (1,0)],
	[(0,0), (0,1), (0,-1), (1,-1)],
	(104,213,255),
	)

Z = (
	[(0,0), (-1,0), (0,1), (1,1)],
	[(0,0), (1,-1), (1,0), (0,1)],
	(250,200,200),
	)

S = (
	[(0,0), (1,0), (-1,1), (0,1)],
	[(0,0), (0,-1), (1,0), (1,1)],
	(249,140,0),
	)

T = (
	[(0,0), (-1,0), (0,1), (1,0)],
	[(0,0), (-1,0), (0,-1), (0,1)],
	[(0,0), (-1,0), (0,-1), (1,0)],
	[(0,0), (0,-1), (0,1), (1,0)],
	(127,224,209),
	)

def block(pos, shape, state):
    board = [None] * CELLNUM
    for b in shape[state]:
        x, y = b
        if pos/COLNUM != (pos+x)/COLNUM:
            return None
        i = pos + x + y * COLNUM
        if i < 0:
            continue
        elif i >= COLNUM*ROWNUM:
            return None
        board[i] = str(shape)
    return board

def draw(board, pos=None):
	if pos:
		s = pos - 3 - 2 * COLNUM
		for m in range(0, COLNUM):
			n = s + m * COLNUM
			for i in range(n, n + 6):
				if 0 <= i < CELLNUM:
					if board[i]:
						c = eval(board[i])[-1]
					else:
						c = BG_COLOR
					x = i % COLNUM * LEN
					y = i / COLNUM * LEN
					screen.fill(c, (x, y, LEN, LEN))
	else:
		screen.fill(BG_COLOR)
		for i,j in enumerate(board):
			if j:
				if board[i]:
					c = eval(board[i])[-1]
				else:
					c = BG_COLOR
				x = i % COLNUM * LEN
				y = i / COLNUM * LEN  
				screen.fill(c, (x, y, LEN, LEN))
	
	pygame.display.flip()

def merge(board1, board2):
    board = board1[:]
    for i, j in enumerate(board2):
        if j:
            board[i] = j
    return board

def rotate(shape,state,times=1):
	for i in range(times):
		if len(shape)-2 == state:
			state = 0
		else:
			state = state + 1
		return state

def bump(board1,board2,pos):
    s = pos - COLNUM - 2
    for i in range(0, 4):
        m = s + i * COLNUM
        for j in range(m, m + 4):
        	try:
        		if board1[j] and board2[j]:
        			return False
        	except:
        		pass
    return True

def eliminate(board):
	n = 0
	for i in range(0,CELLNUM,COLNUM):
		if not None in board[i:i+COLNUM]:
			board = [None]*COLNUM + board[:i] + board[i+COLNUM:]
			n = n + 1
	return board,n

def printcores(n,score,scores):
	text = font.render("Scroes:" + str(scores), True, FONT_COLOR)
	screen.blit(text, ((COLNUM) * LEN, 0))

pygame.init() 
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
pygame.event.set_blocked(None)
pygame.event.set_allowed((KEYDOWN, QUIT))
pygame.key.set_repeat(75, 0)
pygame.display.set_caption('Tetris')
pygame.display.update()

board = [None] * CELLNUM

levels = [550,500,450,400,350,300,250,200,150,100]
index = 0

screen.fill(BG_COLOR)

font = pygame.font.SysFont("arial", 28)
losefont = pygame.font.SysFont("arial", 28)
score = 0
scores = 0
text = font.render("Scroes:" + str(scores), True, FONT_COLOR)
losetext = losefont.render("Game Over!", True, FONT_COLOR)
screen.blit(text, ((COLNUM) * LEN, 0))


while True:
	shape = random.choice((O,I,Z,L,S,J,T))
	state = 0
	pos = ORIGIN_POS
	level = levels[index]

	if not bump(board, block(pos,shape,state), pos):
		#screen.blit(losetext, ((COLNUM) * LEN, ROWNUM * LEN/2))
		pygame.time.delay(2000)
		break

	pygame.time.set_timer(KEYDOWN, level)
	pygame.draw.line(screen, FONT_COLOR, ((COLNUM)*LEN,0), (COLNUM*LEN,ROWNUM*LEN))

	while True:
		draw(merge(board, block(pos,shape,state)), pos)
		event = pygame.event.wait()
		if event.type == QUIT: sys.exit()
		try:
			result = {
                K_UNKNOWN: pos+COLNUM,
                K_UP: pos,
                K_DOWN: pos+COLNUM,
                K_LEFT: pos-1,
                K_RIGHT: pos+1,
            }[event.key]
		except KeyError:
			continue

		if event.key == K_UP:
			state = rotate(shape,state)

		elif event.key in (K_LEFT,K_RIGHT) and pos/COLNUM != result/COLNUM:
			continue

		blockresult = block(result,shape,state)
		if block(result,shape,state) and bump(board,blockresult,result):
			pos = result
		else:
			if event.key == K_UP:
				state = rotate(shape,state,times=3)
			elif not event.key in (K_LEFT, K_RIGHT):
				break

	board = merge(board,block(pos,shape,state))
	board,n = eliminate(board)
	if n != 0:
		draw(board)
		score = 100*n*n
		scores = scores + score
		index = scores/500
		if index >= 9:
			index = 9
	
	printcores(n,score,scores)