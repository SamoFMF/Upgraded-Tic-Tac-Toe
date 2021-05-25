# Logic for the game

# CONSTANTS
PLAYER1 = 1
PLAYER2 = 2
EMPTY = 0

TIE = 3
NOT_OVER = 4

DIM = 3
NUM_SIZES = 3
NUM_EACH_SIZE = 2
MAX_MOVES = NUM_SIZES * NUM_EACH_SIZE * 2

def opponent(player):
    if player == PLAYER1:
        return PLAYER2
    elif player == PLAYER2:
        return PLAYER1
    else:
        assert False, f"neveljaven nasprotnik: {player}"

class Logic:
    threes = [tuple((j,i) for j in range(DIM)) for i in range(DIM)] \
            + [tuple((i,j) for j in range(DIM)) for i in range(DIM)] \
            + [((0,0), (1,1), (2,2))]
    def __init__(self, toMove = PLAYER1):
        # Create board
        self.board = [[EMPTY] * DIM for _ in range(DIM)]

        # Determine whos turn it is
        self.toMove = toMove

        # Move history
        self.history = []

        # Number of moves
        self.moveCount = 0

        # Available figures for each player
        self.figures = [{i+1: NUM_EACH_SIZE for i in range(NUM_SIZES)} for _ in range(2)]
        
        # Highest available figure
        self.highestFigure = [NUM_SIZES, NUM_SIZES]

        # Current state of the game
        self.currentState = NOT_OVER
        self.winningThree = None
    
    def copy(self):
        '''Returns a copy of the instance.'''
        G = Logic(self.toMove)
        G.board = [[i for i in j] for j in self.board]
        G.history = [i for i in self.history]
        G.moveCount = self.moveCount
        G.figures = [i.copy() for i in self.figures]
        G.highestFigure = [i for i in self.highestFigure]
        G.currentState = self.currentState
        G.winningThree = [i for i in self.winningThree] if self.winningThree is not None else None
        return G
    
    def getLegalMoves(self):
        moves = []
        for x in range(DIM):
            for y in range(DIM):
                if self.board[x][y] == EMPTY:
                    threshold = 0
                elif self.board[x][y][0] == self.toMove:
                    continue
                else:
                    threshold = self.board[x][y][1]
                for figure in self.figures[self.toMove-1]:
                    if figure > threshold:
                        moves.append((x,y,figure))
        return moves
    
    def playMove(self, p):
        x,y,z = p

        # Save previous
        prev = self.board[x][y]

        # Place the move on the board
        self.board[x][y] = (self.toMove, z)
        self.moveCount += 1

        # Add it to history
        self.history.append((x,y,(self.toMove,z),prev))

        # Update figures
        self.figures[self.toMove-1][z] -= 1
        if self.figures[self.toMove-1][z] == 0:
            del self.figures[self.toMove-1][z]
            # self.availableFigures[self.toMove-1].remove(z)
            if z == self.highestFigure[self.toMove-1]:
                for i in range(z-1,0,-1):
                    if i in self.figures[self.toMove-1] and self.figures[self.toMove-1][i] > 0:
                        self.highestFigure[self.toMove-1] = i
                        break
                else:
                    # No figures left
                    self.highestFigure[self.toMove-1] = 0
        
        # Check if game is over
        winner, three = self.getCurrentState()

        if winner == NOT_OVER:
            # Game continues
            self.toMove = opponent(self.toMove)
        else:
            # Game is over
            self.toMove = None
            self.currentState = winner
            self.winningThree = three
        
        return winner, three
    
    def undoMove(self):
        '''Undo last move in the history.'''
        if len(self.history) == 0: # No moves to undo
            return
        
        # Get last move from history
        x,y,p,prev = self.history.pop()

        # Undo the move on the board
        self.board[x][y] = prev
        self.moveCount -= 1

        toMove, figure = p
        self.toMove = toMove

        # Update figures
        if figure in self.figures[self.toMove-1]:
            self.figures[self.toMove-1][figure] += 1
        else:
            self.figures[self.toMove-1][figure] = 1
        self.highestFigure[self.toMove-1] = max(self.highestFigure[self.toMove-1], figure)

        # Undo current state if needed or not
        self.currentState = NOT_OVER
        self.winningThree = None
    
    def getCurrentState(self):
        '''Returns current state of the game.'''
        for three in Logic.threes:
            x,y = three[0]
            if self.board[x][y] == EMPTY:
                continue
            player = self.board[x][y][0]
            x1,y1 = three[1]
            x2,y2 = three[2]
            if self.board[x1][y1] != EMPTY and self.board[x1][y1][0] == player and self.board[x2][y2] != EMPTY and self.board[x2][y2][0] == player:
                return player, three
        if self.moveCount == MAX_MOVES:
            return TIE, None
        else:
            return NOT_OVER, None