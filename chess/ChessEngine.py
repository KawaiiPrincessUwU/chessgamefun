"""
This class is responsible for storing all the information about the current state of a chess game. It will also be
responsible for determining the valid moves at the current state. It will also keep a move log
"""
class GameState:
    def __init__(self):
        #board is a 8x8 2d list, each element of the list has two characters
        #The first character represents the colour of pieces. 'B' or 'P'
        #The second character represents the type of the piece 'K', 'Q', 'R', 'B', 'N' or 'P'
        #Need to clean it up, check imaging to see if correct or not
        # "--" - represents an empty space with no piece.
        self.board = [
            ["Pt", "Ph", "Pb", "Pq", "Pq", "Pb", "Ph", "Pt"],
            ["Pp", "Pp", "Pp", "Pp", "Pp", "Pp", "Pp", "Pp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["B", "B", "B", "B", "B", "B", "B", "B"],
            ["Br", "Bn", "Bb", "Bq", "Bk", "Bb", "Bn", "Br"]]
        self.whiteToMove = True
        self.moveLog = []

    """
    Takes a Move as a parameter and executes it (this will not work for castling, pawn promotion and en-passant
    """

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  #log the move so we can undo later
        self.whiteToMove = not self.whiteToMove  # Swap players

    """
    Undo the last move made 
    """
    def undoMove(self):
        if len(self.moveLog) != 0:  #make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  #switch turns back

    """
    All moves considering checks 
    """
    def getValidMoves(self):
        return self.getAllPossibleMoves()  #for now, we will not worry about these

    """
    All moves without considering checks 
    """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  #number of rows
            for c in range(len(self.board[r])):  # number of cols in given now
                turn = self.board[r][c][0]
                if (turn == 'p' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookmoves(r, c, moves)
        return moves

    """
    Get all the pawn moves located at row, col and add these moves to the list
    """
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn moves
            if self.board[r-1][c] == "--":  #1 square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))



    """
    Get all the rook moves located at row, col and add these moves to the list
    """

    def getRookMoves(self, r, c, moves):
        pass





class Move:
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6":2,"7":1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

    """
    overriding the equals method 
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        # you can add to make this real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
