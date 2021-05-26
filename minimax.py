from logic import *

class Minimax:
    def __init__(self, depth):
        self.depth = depth
        self.game: Logic = None
        self.me = None

        self.WIN = 1000
        self.LOSE = -1000
    
    def evalState(self):
        # TODO
        return 1
    
    def key(self, move):
        # TODO
        return 1
    
    def k(self):
        return 1 - self.game.moveCount / MAX_MOVES / 2
    
    def hash(self, state):
        return tuple(tuple(i) for i in state)
    
    def negamax(self, depth, alpha, beta, color):
        # Check if game is over
        winner = self.game.currentState
        if winner != NOT_OVER:
            # Game is over
            if winner == self.me:
                return None, color * self.WIN * self.k()
            elif winner == TIE:
                return None, 0
            else:
                return None, color * (-self.WIN) * self.k()
        elif depth == 0:
            # Max depth
            return None, color * self.evalState()
        else:
            # Search deeper
            maxVal = -float("inf")
            bestMove = None
            for p in sorted(self.game.getLegalMoves(), key=self.key):
                self.game.playMove(p)
                _, value = self.negamax(depth-1, -beta, -alpha, -color)
                value = -value
                self.game.undoMove()
                if value > maxVal:
                    maxVal = value
                    bestMove = p
                    if value > alpha:
                        alpha = value
                if alpha >= beta:
                    break
            return bestMove, maxVal