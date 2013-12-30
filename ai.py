from subprocess import Popen, PIPE, STDOUT
import threading
import time
from constants import FEN2PIECE
from vector2D import Vec2d
from board import InvalidMove
import piece

class AIThread(threading.Thread):
    def __init__(self, board, color, delay=0.7):
        super(AIThread, self ).__init__()
        self.daemon = True
        self.board = board
        self.color = color
        self.delay = delay # seconds
        self.keep_running = True

    def restart_on_timeout(self):
        if self.timeout:
            pass

    def run(self):
        ai = AI(self.color)
        while self.keep_running and self.board.winner is None:
            time.sleep(self.delay)
            #t = threading.Timer(30, self.restart_on_timeout())
            #t.start()
            self.timeout = True
            ai.try_move(self.board)
            self.timeout = False 


class AI:
    def __init__(self, color, thinking_time=10000, uci_engine="stockfish"):
        self.color = color
        self.thinking_time = thinking_time
        self.uci_engine = uci_engine
        self.process = None
        self._start_process()

    def _start_process(self):
        if self.process is not None:
            self.process.terminate()
        self.process = Popen([self.uci_engine], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        self.process.stdin.write("uci\n")
        self._read_until("uciok")
        print("engine is ready")

    def _read_until(self, keyword):
        last_line = None
        line = None
        while not (line == "" and last_line == ""):
            last_line = line
            line = self.process.stdout.readline()
            #print line
            if keyword in line:
                return line
        print("engine terminated unexpectedly")
        self._start_process()
        return "no response"

    def compute_move(self, board):
        fen = board.as_fen(self.color)
        self.process.stdin.write("""position fen %s
go wtime %s winc 0 btime %s binc 0
""" % (fen, self.thinking_time, self.thinking_time))
        self.response = self._read_until("bestmove").split()
        print "fen:", fen
        print "response:", self.response
        if len(self.response) == 4:
            bestmove = self.response[1]
            if bestmove == '(none)':
                return None
            else:
                return self.decode_move(bestmove)
        else:
            return None

    def decode_move(self, move):
        """return frompos,topos,promotion"""
        return (Vec2d(ord(move[0]) - ord('a'), 8 - int(move[1])),
                Vec2d(ord(move[2]) - ord('a'), 8 - int(move[3])),
                None if len(move) == 4 else FEN2PIECE[move[4].upper()])

    def try_move(self, board):
        # stockfish does not return king-killing moves
        try:
            if board.attack_king(self.color):
                return
        except InvalidMove as e:
            frompos, topos, promotion = move
            print("cannot execute king attack from %s to %s" % (frompos, topos))
        move = self.compute_move(board)
        if move is not None:
            try:
                board.move(*move)
            except InvalidMove as e:
                frompos, topos, promotion = move
                print("cannot execute engine move from %s to %s (%s)" % (frompos, topos, e))


