# Information storage

class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],   
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.pawnMoves, 'R': self.rookMoves, 'N': self.knightMoves, 'B': self.bishopMoves, 'Q': self.queenMoves, 'K': self.kingMoves}
        self.whitesMove = True
        self.movesHistory = []
        self.whiteKLoc =  (7, 4)
        self.blackKLoc = (0, 4)
        self.inCheck = False
        self.checkMate = False
        self.staleMate = False
        self.EnPassantValidSq = ()
        self.pins = []
        self.checks = []
        #self.currentCastlingPrerogatives = CastlingPrerogatives(True, True, True, True)
        #self.castlePrerogativesHistory = [CastlingPrerogatives(self.currentCastlingPrerogatives.wk_side, self.currentCastlingPrerogatives.bk_side,
                                                               #self.currentCastlingPrerogatives.wq_side, self.currentCastlingPrerogatives.bq_side)]
    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoves
        self.movesHistory.append(move)
        self.whitesMove = not self.whitesMove

        if move.pieceMoves == "wK":
            self.whiteKLoc = (move.endRow, move.endCol)
        elif move.pieceMoves == "bK":
            self.blackKLoc = (move.endRow, move.endCol)
        
        if move.pawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoves[0] + 'Q'
            
        if move.isEnPassantPossible:
            self.board[move.startRow][move.endCol] = '--'
        if move.pieceMoves[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.EnPassantValidSq = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.EnPassantValidSq = ()
            
        # self.updateCastlePrerogatives(move)
        # self.castlePrerogativesHistory.append(CastlingPrerogatives(self.currentCastlingPrerogatives.wk_side, self.currentCastlingPrerogatives.bk_side,
        #                                                             self.currentCastlingPrerogatives.wq_side, self.currentCastlingPrerogatives.bq_side))
                     
        
    def undoMove(self):
        if len(self.movesHistory)!=0:
            move = self.movesHistory.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoves
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whitesMove = not self.whitesMove
            
            if move.pieceMoves == "wK":
                self.whiteKLoc == (move.startRow, move.startCol)
            elif move.pieceMoves == "bK":
                self.blackKLoc == (move.startRow, move.startCol)
                
            if move.isEnPassantPossible:
                self.board[move.endRow][move.endCol] = '--' 
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.EnPassantValidSq = (move.endRow, move.endCol)
            if move.pieceMoves[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.EnPassantValidSq = ()
            
            # self.castlePrerogativesHistory.pop()
            # self.currentCastlingPrerogatives = self.castlePrerogativesHistory[-1]
 
                
    # def updateCastlePrerogatives(self, move):
    #     if move.pieceMoves == 'wK':
    #         self.currentCastlingPrerogatives.wk_side = False
    #         self.currentCastlingPrerogatives.wq_side = False
    #     elif move.pieceMoves == 'bK':
    #         self.currentCastlingPrerogatives.bk_side = False
    #         self.currentCastlingPrerogatives.bq_side = False
    #     elif move.pieceMoved == 'wR':
    #         if move.startRow == 7:
    #             if move.startCol == 0:
    #                 self.currentCastlingPrerogatives.wq_side = False
    #             elif move.startCol == 7:
    #                 self.currentCastlingPrerogatives.wk_side = False
    #     elif move.pieceMoved == 'bR':
    #         if move.startRow == 0:
    #                 if move.startCol == 0:
    #                     self.currentCastlingPrerogatives.bq_side = False
    #                 elif move.startCol == 7:
    #                     self.currentCastlingPrerogatives.bk_side = False
            
    def validMoves(self):
        moves=[]
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whitesMove:
            kingRow = self.whiteKLoc[0]
            kingCol = self.whiteKLoc[1]
        else:
            kingRow = self.blackKLoc[0]
            kingCol = self.blackKLoc[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.allPossibilities()
                check =self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].pieceMoves[1]!='K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.kingMoves(kingRow, kingCol, moves)
        else:
            moves = self.allPossibilities()
        if moves == []:
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        return moves
    
    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whitesMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKLoc[0]
            startCol = self.whiteKLoc[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKLoc[0]
            startCol = self.blackKLoc[1]
        
        directions = ((-1, 0),(0, -1),(1, 0),(0, 1),(-1, -1),(-1, 1),(1, -1),(1, 1))
        for j in range(len(directions)):
            d = directions[j]
           
            possiblePin = ()
            for i in range(1, 8):
                
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor and endPiece[1]!='K':
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == 'R') or \
                            (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type =='p' and ((enemyColor == 'w') and 6 <= j <= 7) or (enemyColor == 'b' and 4<= j <= 5)) or \
                                    (type == 'Q') or (i == 1 and type == 'K'):
                                        if possiblePin == ():
                                            
                                            inCheck = True
                                            
                                            checks.append((endRow, endCol, d[0], d[1]))
                                            break
                                        else:
                                            pins.append(possiblePin)
                                            break
                        else:
                            break
                else:
                    break
        knightsMove = (((2, 1), (1, 2), (2, -1), (1, -2), (-2, 1), (-1, 2), (-2, -1), (-1, -2)))
        for m in knightsMove:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
       
        return inCheck, pins, checks
    
   
    
    def allPossibilities(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whitesMove) or (turn == 'b' and not self.whitesMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves
    
    def freeMovement(self, r, c, moves, direction, freedom, piecePinned, pinDirection, isKing):
        for dr, dc in direction:
            new_r, new_c = r + dr, c + dc
            while 0 <= new_r < 8 and 0 <= new_c < 8:
                if not piecePinned or pinDirection == (dr, dc) or pinDirection == (-dr, -dc):
                    if self.board[new_r][new_c] == "--":
                        moves.append(Move((r, c), (new_r, new_c), self.board))
                        if not freedom:
                            break;
                    else:
                        if (self.whitesMove and self.board[new_r][new_c][0] == 'b') or \
                        (not self.whitesMove and self.board[new_r][new_c][0] == 'w'):
                            moves.append(Move((r, c), (new_r, new_c), self.board))
                        break
                    new_r += dr
                    new_c += dc
                    
    
    def pawnMoves(self, r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        if self.whitesMove:
            if self.board[r-1][c] == "--":
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r,c),(r-1,c), self.board))
                    if r == 6 and self.board[r-2][c]=="--":
                        moves.append(Move((r,c),(r-2,c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r,c),(r-1,c-1), self.board))
                elif (r-1, c-1) == self.EnPassantValidSq:
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r,c),(r-1,c-1), self.board, isEnPassantMove = True))
                        
                        
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r,c),(r-1,c+1), self.board)) 
                elif (r-1, c+1) == self.EnPassantValidSq:
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r,c),(r-1,c+1), self.board, isEnPassantMove = True))
                        
        else:
            if self.board[r+1][c] == "--":
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r,c),(r+1,c), self.board))
                    if r == 1 and self.board[r+2][c]=="--":
                        moves.append(Move((r,c),(r+2,c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r,c),(r+1,c-1), self.board))
                elif (r+1, c-1) == self.EnPassantValidSq:
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r,c),(r+1,c-1), self.board, isEnPassantMove = True))
                        
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    if not piecePinned or pinDirection == (1,1):
                        moves.append(Move((r,c),(r+1,c+1), self.board)) 
                elif (r+1, c+1) == self.EnPassantValidSq:
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r,c),(r+1,c+1), self.board, isEnPassantMove = True))
                        
        
        
    def rookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "Q":
                    self.pins.remove(self.pins[i])
                break
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
        self.freeMovement(r,c,moves,directions, True, piecePinned, pinDirection, False)
    
    def bishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = [(1,1), (-1, -1), (1, -1), (-1, 1)] # right&down, left&up, left&down, right&up
        self.freeMovement(r,c,moves, directions, True, piecePinned, pinDirection, False)
        
    def knightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        directions = [(2, 1), (1, 2), (2, -1), (1, -2), (-2, 1), (-1, 2), (-2, -1), (-1, -2)]
        self.freeMovement(r,c,moves, directions, False, piecePinned, (), False)    
        
    def queenMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1,1), (-1, -1), (1, -1), (-1, 1)]
        self.freeMovement(r,c,moves, directions, True, piecePinned, pinDirection, False)
    
    def kingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whitesMove else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    if allyColor == 'w':
                        self.whiteKLoc = (endRow, endCol)
                    else:
                        self.blackKLoc = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    if allyColor == 'w':
                        self.whiteKLoc = (r,c)
                    else:
                        self.blackKLoc = (r,c)
                        
       # self.getCastleMoves(r, c, moves, allyColor)
        
    # def getCastleMoves(self, r, c, moves, allyColor):
    #     if self.
        
    
# class CastlingPrerogatives():
#     def __init__(self, wk_side, bk_side, wq_side, bq_side):
#             self.wk_side = wk_side
#             self.bk_side = bk_side
#             self.wq_side = wq_side
#             self.bk_side = bk_side
            
        
        
        
        
    
class Move():
    
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    
    
    def __init__(self, startSq, endSq, board, isEnPassantMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoves = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        
        
        self.pawnPromotion = (self.pieceMoves == 'wp' and self.endRow == 0) or (self.pieceMoves == 'bp' and self.endRow ==7)
        self.pawnPromotionPiece = 'Q'
            
        self.isEnPassantPossible = isEnPassantMove
        if self.isEnPassantPossible:
            self.pieceCaptured = 'wp' if self.pieceMoves == 'bp' else 'bp'
            #print(self.pieceMoves)
        
        #print(self.isEnPassantPossible)
        #print((self.startRow, self.startCol))
        #print("    ")
        
        
        self.moveID = self.startRow * 1000 + self.startCol *100 + self.endRow * 10 + self.endCol
        
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol);
        
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]