#!/usr/bin/env python
import os, sys
import pygame
from pygame.locals import *
from vector2D import Vec2d
from resources import load_image, load_sound, Sounds
from constants import *
from parameters import FIELDSIZE, AI_DELAY
from board import Board
from draw import draw_outlined_text
from ai import AIThread
#import autopdb

def new_game(background, oldAI=None):
    board = Board(background, (WHITE,))
    allsprites = pygame.sprite.RenderPlain(board.grid.values())
    if oldAI is not None:
        oldAI.keep_running = False
    ai = AIThread(board, BLACK, AI_DELAY)
    ai.start()
    return board, allsprites, ai

def main():
#Initialize Everything

    pygame.init()
    Sounds.whiff = load_sound('whiff.wav')
    Sounds.punch = load_sound('punch.wav')
    Sounds.boom = load_sound('boom.wav')
    Sounds.cosmic = load_sound('secosmic_lo.wav')

    screen = pygame.display.set_mode(GRIDDIM * FIELDSIZE + Vec2d(2,2)
            )#, pygame.FULLSCREEN)
    pygame.display.set_caption('Real Time Chess')
    #pygame.mouse.set_visible(0)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()

#Prepare Game Objects
    clock = pygame.time.Clock()
    board, allsprites, ai = new_game(background)

#Main Loop
    while True:
        clock.tick(60)

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_r and board.winner is not None:
                board, allsprites, ai = new_game(background, ai)
            elif event.type == MOUSEBUTTONDOWN:
                board.handle_click(pygame.mouse.get_pos())

        allsprites.update(board)

    #Draw Everything
        screen.blit(background, (0, 0))
        board.redraw()
        allsprites.draw(screen)
        if board.winner is not None:
            draw_outlined_text(screen, background.get_rect().center,
                    "Player %s wins" % COLORNAMES[board.winner], 64,
                    3, (0,0,0), (255,0,0))
            draw_outlined_text(screen, Vec2d(0, 64) + background.get_rect().center,
                    "Press 'R' to continue or 'Esc' to quit", 24,
                    1, (255,255,255), (0,0,0))

        pygame.display.flip()

#Game Over
    ai.keep_running = False

#this calls the 'main' function when this script is executed
if __name__ == '__main__': 
    main()

