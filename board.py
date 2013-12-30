import pygame
from constants import *
from parameters import FIELDSIZE
from vector2D import Vec2d
from piece import Piece
from resources import Sounds
import movegenerator as mgen

class InvalidMove(Exception):
    def __init__(self, comment):
        self.comment = comment
    def __str__(self):
        return self.comment



def draw_squares(surf, colors):
    # draw vertical lines
    for x in range(GRIDDIM.x):
        for y in range(GRIDDIM.y):
            pygame.draw.rect(surf, 
                    colors[(x % 2 + y % 2) % 2],
                    pygame.Rect(Vec2d(x,y) * FIELDSIZE, FIELDSIZE))


class EmptySpace:
    def as_fen(self):
        return "1"


class Board:
    EMPTY_SPACE = EmptySpace()

    def __init__(self, surf, human_controlled):
        self.surf = surf
        self.grid = {}
        self.human_controlled = human_controlled
        self.selected = None
        self.winner = None
    
        # init pieces
        self.default_setup()
        #self.debug_setup()


    def default_setup(self):
        for col in range(GRIDDIM.x - 0):
            self.add_piece((col, 6), PAWN, WHITE)
            self.add_piece((col, 1), PAWN, BLACK)
        # ROOK
        self.grid[Vec2d(0, 7)] = Piece(self.surf, ROOK, WHITE, Vec2d(0, 7))
        self.grid[Vec2d(7, 7)] = Piece(self.surf, ROOK, WHITE, Vec2d(7, 7))
        self.grid[Vec2d(0, 0)] = Piece(self.surf, ROOK, BLACK, Vec2d(0, 0))
        self.grid[Vec2d(7, 0)] = Piece(self.surf, ROOK, BLACK, Vec2d(7, 0))
        # KNIGHT
        self.grid[Vec2d(1, 7)] = Piece(self.surf, KNIGHT, WHITE, Vec2d(1, 7))
        self.grid[Vec2d(6, 7)] = Piece(self.surf, KNIGHT, WHITE, Vec2d(6, 7))
        self.grid[Vec2d(1, 0)] = Piece(self.surf, KNIGHT, BLACK, Vec2d(1, 0))
        self.grid[Vec2d(6, 0)] = Piece(self.surf, KNIGHT, BLACK, Vec2d(6, 0))
        # BISHOP
        self.grid[Vec2d(2, 7)] = Piece(self.surf, BISHOP, WHITE, Vec2d(2, 7))
        self.grid[Vec2d(5, 7)] = Piece(self.surf, BISHOP, WHITE, Vec2d(5, 7))
        self.grid[Vec2d(2, 0)] = Piece(self.surf, BISHOP, BLACK, Vec2d(2, 0))
        self.grid[Vec2d(5, 0)] = Piece(self.surf, BISHOP, BLACK, Vec2d(5, 0))
        # KING & QUEEN
        self.grid[Vec2d(3, 7)] = Piece(self.surf, QUEEN, WHITE, Vec2d(3, 7))
        self.grid[Vec2d(4, 7)] = Piece(self.surf, KING,  WHITE, Vec2d(4, 7))
        self.grid[Vec2d(3, 0)] = Piece(self.surf, QUEEN, BLACK, Vec2d(3, 0))
        self.grid[Vec2d(4, 0)] = Piece(self.surf, KING,  BLACK, Vec2d(4, 0))


    def debug_setup(self):
        for col in range(GRIDDIM.x - 0):
            #self.grid[Vec2d(col, 1)] = Piece(self.surf, PAWN, WHITE, Vec2d(col, 1))
            self.grid[Vec2d(col, 6)] = Piece(self.surf, PAWN, BLACK, Vec2d(col, 6))
        # ROOK
        #self.grid[Vec2d(0, 7)] = Piece(self.surf, ROOK, WHITE, Vec2d(0, 7))
        #self.grid[Vec2d(7, 7)] = Piece(self.surf, ROOK, WHITE, Vec2d(7, 7))
        #self.grid[Vec2d(0, 0)] = Piece(self.surf, ROOK, BLACK, Vec2d(0, 0))
        #self.grid[Vec2d(7, 0)] = Piece(self.surf, ROOK, BLACK, Vec2d(7, 0))
        ## KNIGHT
        #self.grid[Vec2d(1, 7)] = Piece(self.surf, KNIGHT, WHITE, Vec2d(1, 7))
        #self.grid[Vec2d(6, 7)] = Piece(self.surf, KNIGHT, WHITE, Vec2d(6, 7))
        #self.grid[Vec2d(1, 0)] = Piece(self.surf, KNIGHT, BLACK, Vec2d(1, 0))
        #self.grid[Vec2d(6, 0)] = Piece(self.surf, KNIGHT, BLACK, Vec2d(6, 0))
        ## BISHOP
        self.grid[Vec2d(3, 4)] = Piece(self.surf, BISHOP, WHITE, Vec2d(3, 4))
        #self.grid[Vec2d(5, 7)] = Piece(self.surf, BISHOP, WHITE, Vec2d(5, 7))
        #self.grid[Vec2d(2, 0)] = Piece(self.surf, BISHOP, BLACK, Vec2d(2, 0))
        #self.grid[Vec2d(5, 0)] = Piece(self.surf, BISHOP, BLACK, Vec2d(5, 0))
        ## KING & QUEEN
        self.add_piece((2, 0), QUEEN, WHITE)
        self.add_piece((6, 0), QUEEN, WHITE)
        self.add_piece((4, 2), QUEEN, WHITE)

        self.grid[Vec2d(4, 3)] = Piece(self.surf, KING,  WHITE, Vec2d(4, 3))
        #self.grid[Vec2d(3, 0)] = Piece(self.surf, QUEEN, BLACK, Vec2d(3, 0))
        self.grid[Vec2d(4, 0)] = Piece(self.surf, KING,  BLACK, Vec2d(4, 0))

    def add_piece(self, gridpos, piece, color):
        self.grid[Vec2d(gridpos)] = Piece(self.surf, piece, color, Vec2d(gridpos))

    def handle_click(self, pos):
        if self.winner is not None:
            Sounds.cosmic.play()
            return
        gridpos = Vec2d(map(round, Vec2d(pos) / FIELDSIZE))
        if self.selected is None:
            if gridpos in self.grid and self.grid[gridpos].color in self.human_controlled:
                self.selected = gridpos
        elif self.selected != gridpos:
            if gridpos in self.grid and self.grid[gridpos].color == self.grid[self.selected].color:
                self.selected = gridpos
            else:
                try:
                    self.move(self.selected, gridpos)
                except InvalidMove as e:
                    print("cannot move from %s to %s (%s)" % (self.selected, gridpos, e))
                    Sounds.whiff.play() #miss

    def redraw(self):
        self.surf.fill((250, 250, 250))
        draw_squares(self.surf, ((255,255,255), (200,200,200)))
        if self.selected is not None:
            pygame.draw.rect(self.surf, (200,255,200), pygame.Rect(self.selected * FIELDSIZE, FIELDSIZE))

    def move(self, frompos, topos, promotion=QUEEN):
        assert(frompos != topos)
        piece = self.grid.get(frompos)
        if piece is None:
            # could have been killed in between
            raise InvalidMove("no piece at frompos")
        piece.promotion = promotion
        victim = self.grid.get(topos)
        pstart = frompos.y == mgen.PAWN_START[piece.color]
        if not mgen.allowed_move(piece.piece, 
                topos - frompos, mgen.FORWARDDIR[piece.color], 
                victim is not None,
                pstart):
            raise InvalidMove("illegal direction for %s" % FENCODE[piece.piece]) 

        if self.in_between(frompos, topos, piece):
            raise InvalidMove("position in between occupied")

        if victim is not None:
            if victim.color == piece.color:
                raise InvalidMove("occupied by own color")
            else:
                piece.attack(topos)
        else:
            if piece.delay == 0:
                self.relocate(frompos, topos)

    def killed(self, attacker, victim):
        Sounds.boom.play()
        victim.kill()
        self.relocate(attacker.gridpos, victim.gridpos)
        if victim.piece == KING:
            self.winner = attacker.color

    def relocate(self, frompos, topos):
        piece = self.grid[frompos]
        if piece.color in self.human_controlled:
            # human moves
            self.selected = topos
        elif self.selected == topos:
            # selected piece is killed
            self.selected = None
        piece.move_to(topos)
        self.grid[topos] = piece
        del self.grid[frompos]

    def in_between(self, frompos, topos, piece):
        if piece.piece == KNIGHT:
            return False
        direction = (topos - frompos).normalized_manhatten()
        #print "checking from %s to %s, dir=%s" % (frompos, topos, direction)
        pos = frompos + direction
        while pos != topos:
            if pos in self.grid:
                return True
            #print "  nothing on %s" % pos
            pos += direction
        return False

    def as_fen(self, color):
        # no castling and no en-passant attacks
        return ('/'.join([self._as_fen_row(y) for y in range(GRIDDIM.y)]) + 
                " %s - - 0 1" % COLORCODES[color])
        
    def _as_fen_row(self, y):
        # no run-length encoding of empty spaces
        return ''.join([self._as_fen_gridpos(x,y) for x in range(GRIDDIM.x)])

    def _as_fen_gridpos(self, x, y):
        return self.grid.get((x,y), Board.EMPTY_SPACE).as_fen()

    def attack_king(self, attacker_color):
        target_color = other_color(attacker_color)
        for gridpos, piece in self.grid.items():
            if piece.piece == KING and piece.color == target_color:
                frompos = self.attack_on_pos(gridpos, attacker_color)
                if frompos is None:
                    return False
                else:
                    #print("king attack: from %s to %s" % (frompos, gridpos))
                    #print attacker_color, target_color
                    self.move(frompos, gridpos)
                    return True

    def attack_on_pos(self, gridpos, attacker_color):
        """returns the first possible attack at gridpos"""
        for kdir in mgen.RELMOVES_KNIGHT:
            frompos = gridpos + kdir
            cand = self.grid.get(frompos)
            if cand is not None and cand.piece == KNIGHT and cand.color == attacker_color:
                return frompos
        for dir in mgen.MAINDIRS:
            frompos = gridpos + dir
            while mgen.on_board(frompos) and not frompos in self.grid:
                frompos += dir
            if mgen.on_board(frompos):
                attacker = self.grid[frompos]
                if attacker.color == attacker_color and mgen.allowed_move(attacker.piece, 
                        gridpos - frompos, 
                        mgen.FORWARDDIR[attacker.color], 
                        True, False):
                    return frompos
        return None

