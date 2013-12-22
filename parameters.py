# gameplay parameters
from constants import *

SPEED = 0.4

REGEN = 1.0 * SPEED
DELAY = 100.0 / SPEED
ATTACK = 2.0 * SPEED

MAXHP = {
        PAWN   : 100.0,
        KNIGHT : 150.0,
        BISHOP : 150.0,
        ROOK   : 200.0,
        QUEEN  : 250.0,
        KING   : 300.0
        }

AI_DELAY = 0.3

# graphical parameters
FIELDSIZE = Vec2d(100,100)

def piece_image(piece, color):
    return "%s%s.png" % (COLORCODES[color], FENCODE[piece].lower())

