import pygame
from constants import *
from parameters import MAXHP, REGEN, ATTACK, DELAY
from parameters import FIELDSIZE, piece_image
from vector2D import Vec2d
from draw import draw_arrow, draw_arrowline
from resources import load_image

class Piece(pygame.sprite.Sprite):

    def __init__(self, surf, piece, color, gridpos):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.surf = surf
        self.piece = piece
        self.color = color
        self.image, self.rect = load_image(piece_image(piece, color), -1)
        self.move_to(gridpos)
        self.delay = 0
        self.hitpoints = MAXHP[piece]
        self.maxhp = MAXHP[piece]
        self.promotion = None # promotion goal if eligible
        self.attackpos = None
        # cyclical attack frame counter for drawing
        self.attack_time = 0 

    def move_to(self, gridpos): 
        # promotion
        if self.piece == PAWN and (gridpos.y == 0 or gridpos.y == GRIDDIM.y - 1):
            self.piece = self.promotion
            self.image, self.rect = load_image(piece_image(self.piece, self.color), -1)
        # update 
        self.delay = DELAY
        self.gridpos = gridpos
        self.rect.center = gridpos * FIELDSIZE + 0.5 * FIELDSIZE
        self.attackpos = None

    def regen(self):
        self.hitpoints = min(self.hitpoints + REGEN, self.maxhp) 
        self.delay = max(0, self.delay - 1)

    def update(self, board):
        self.regen()
        # draw hitpoints
        topleft = self.gridpos * FIELDSIZE
        pygame.draw.rect(self.surf, (0,255,0), pygame.Rect(
            topleft + Vec2d(5, 5),
            ((FIELDSIZE.x - 10) * self.hitpoints / self.maxhp, 10)))
        # draw movement delay
        pygame.draw.rect(self.surf, (255,255,0), pygame.Rect(
            topleft + Vec2d(5, 17), 
            ((FIELDSIZE.x - 10) * self.delay / DELAY, 10)))
        self.continue_attack(board)

    def continue_attack(self, board):
        if self.attackpos is not None:
            if (board.in_between(self.gridpos, self.attackpos, self) or
                    board.grid.get(self.attackpos) is None or
                    board.grid[self.attackpos].color == self.color):
                self.attackpos = None
            else:
                victim = board.grid[self.attackpos]
                self.draw_attack(victim)
                victim.hitpoints -= (REGEN + ATTACK)
                if victim.hitpoints <= 0:
                    self.victim = None
                    board.killed(self, victim)

    def attack(self, attackpos):
        self.attackpos = attackpos

    def as_fen(self):
        code = FENCODE[self.piece]
        return code if self.color == WHITE else code.lower()

    def draw_attack(self, victim):
        offset = 10
        #pygame.draw.line(self.surf, (255,0,0), self.rect.center, victim.rect.center, 3)
        #draw_arrow(self.surf, self.rect.center, victim.rect.center, 20, (255,0,0))
        draw_arrowline(self.surf, self.rect.center, victim.rect.center, 
                5, offset, self.attack_time, (255,0,0))
        self.attack_time = (self.attack_time + 1) % offset

