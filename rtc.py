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
    board = Board(background, (WHITE,))
    allsprites = pygame.sprite.RenderPlain(board.grid.values())
    ai = AIThread(board, BLACK, AI_DELAY)
    ai.start()

#Main Loop
    while True:
        clock.tick(60)

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
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

        pygame.display.flip()

#Game Over
    ai.keep_running = False

#this calls the 'main' function when this script is executed
if __name__ == '__main__': 
    main()

