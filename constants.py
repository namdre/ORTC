"""
author: jakob.erdmann@gmail.com
license: GPL 3.0 or newer
"""
from vector2D import Vec2d

GRIDDIM = Vec2d(8,8)

PIECES = range(6)
PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING = PIECES

COLORS = range(2)
WHITE, BLACK = COLORS

COLORNAMES = {WHITE : "White", BLACK : "Black"}
COLORCODES = {WHITE : "w", BLACK : "b"}

FENCODE = {
        PAWN   : 'P',
        KNIGHT : 'N',
        BISHOP : 'B',
        ROOK   : 'R',
        QUEEN  : 'Q',
        KING   : 'K'
        }

FEN2PIECE = dict([(v,k) for k,v in FENCODE.items()])


def other_color(color):
    return 1 - color
