Open Real-Time Chess (ORTC)
====

Rules
-----
The ancient game you all love is now a lot faster! Every piece may attack and
move simultaneously. Once the move delay (yellow bar) has disappeared the piece
may move again but it may commence its attack immediately after moving. If the
hitpoints of a piece (green bar) are reduced to zero, the piece is removed from
the board. While attacking a piece may switch targets at any time. 

Strategy
--------
* Hitpoints generate slowly over time so a strategic withdrawal is often a good idea.
* Some Pieces have more hitpoints than others. If a pawn attacks the King, the
  King can fight back and win!
* Attacking and defeating a piece causes a piece to move to the victims location
  regardless of the current move delay. This can be used to get out of a tight
  spoit


Requirements
------------
* python 2.7 (python.org)
* pygame (pygame.org)
* chess engine stockfish (stockfishchess.org) accessible via commandline 'stockfish'


Customization
-------------
AI-difficulty can be customized by increasing the value of AI_DELAY in parameters.py
