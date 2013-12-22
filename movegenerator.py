# define chess movement rules
from constants import *
from vector2D import Vec2d

RELMOVES_KNIGHT = set([
    Vec2d( 2, 1),
    Vec2d(-2, 1),
    Vec2d( 2,-1),
    Vec2d(-2,-1),
    Vec2d( 1, 2),
    Vec2d(-1, 2),
    Vec2d( 1,-2),
    Vec2d(-1,-2)])

MAINDIRS = [
        Vec2d( 1, 1),
        Vec2d(-1, 1),
        Vec2d( 1,-1),
        Vec2d(-1,-1),
        Vec2d( 0, 1),
        Vec2d( 0,-1),
        Vec2d( 1, 0),
        Vec2d(-1, 0)]

FORWARDDIR = {WHITE : -1, BLACK: 1}

PAWN_START = {WHITE : 6, BLACK: 1}

def allowed_move(piece, dir, forwarddir, victim, pstart):
    if dir == (0,0):
        return False
    rooklike = (dir.x == 0 or dir.y == 0)
    bishoplike = abs(dir.x) == abs(dir.y)
    if piece == ROOK:
        return rooklike
    elif piece == BISHOP:
        return bishoplike
    elif piece == QUEEN:
        return rooklike or bishoplike
    elif piece == KING:
        # XXX castling
        return abs(dir.x) <= 1 and abs(dir.y) <= 1
    elif piece == KNIGHT:
        return dir in RELMOVES_KNIGHT
    elif piece == PAWN:
        return (
                (dir.y == forwarddir and (
                    (dir.x == 0 and not victim) or
                    (abs(dir.x) == 1 and victim))) or
                (dir.y == 2 * forwarddir and pstart and dir.x == 0 and not victim))
    return False


def available_moves_on_empty_board(pos, piece):
    pass

def available_moves_relative(piece):
    pass

def attacks_on_pos(pos, piece):
    pass

def on_board(pos):
    return (pos.x >= 0 and
            pos.y >= 0 and
            pos.x < GRIDDIM.x and
            pos.y < GRIDDIM.y)

            

