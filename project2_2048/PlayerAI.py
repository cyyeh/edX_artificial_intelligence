from random import randint
from BaseAI import BaseAI
 
class PlayerAI(BaseAI):
    def getMove(self, grid):
        moves = grid.getAvailableMoves()
        return moves[randint(0, len(moves) - 1)] if moves else None