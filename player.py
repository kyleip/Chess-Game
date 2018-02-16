from piece import *
from board import *

class Player(object):

    def __init__(self, case):
        self.case = case
        self.capturedPieceList = []
        self.capturedPieceSymbols = []
        if self.case == "UPPER":
            self.R = Rook((5, 1), self)
            self.B = Bishop((5, 2), self)
            self.S = SilverGeneral((5, 3), self)
            self.G = GoldenGeneral((5, 4), self)
            self.K = King((5, 5), self)
            self.P = Pawn((4, 5), self)
            self.pieceList = [self.R, self.B, self.S, self.G, self.K, self.P]
            self.piecePosList = [self.R.pos, self.B.pos, self.S.pos, self.G.pos, self.K.pos, self.P.pos]
            self.promotionZone = []
            for i in range(1, 6):
                self.promotionZone += [(1, i)]
        else:
            self.R = Rook((1, 5), self)
            self.B = Bishop((1, 4), self)
            self.S = SilverGeneral((1, 3), self)
            self.G = GoldenGeneral((1, 2), self)
            self.K = King((1, 1), self)
            self.P = Pawn((2, 1), self)
            self.pieceList = [self.R, self.B, self.S, self.G, self.K, self.P]
            self.piecePosList = [self.R.pos, self.B.pos, self.S.pos, self.G.pos, self.K.pos, self.P.pos]
            self.promotionZone = []
            for i in range(1, 6):
                self.promotionZone += [(5, i)]

    def getKingPos(self):
        for each in self.pieceList:
            if isinstance(each, King):
                return each.pos

    def clearPieces(self):  # clears the players pieces (only used when doing file mode)
        del self.R
        del self.B
        del self.S
        del self.G
        del self.K
        del self.P
        self.pieceList = []
        self.piecePosList = []

    def updatePiecePosList(self):   # updates the piece position list of the player
        self.piecePosList = []
        for each in self.pieceList:
            self.piecePosList += [each.pos]


    def updateCapturedPieceList(self, p):   # updates the captured piece list of the player
        self.capturedPieceList += [p]
        tempSymbol = p.symbol
        if tempSymbol[0] == '+':
            tempSymbol = tempSymbol[1]
        if self.case == "UPPER":
            tempSymbol = tempSymbol.upper()
        else:
            tempSymbol = tempSymbol.lower()
        p.symbol = tempSymbol
        p.isPromoted = False
        self.capturedPieceSymbols += [tempSymbol]


    def printCapturedPieceList(self):
        resLine = "Captures "
        resLine += self.case
        resLine += ":"
        for each in self.capturedPieceSymbols:
            resLine += ' '
            resLine += each
        if len(self.capturedPieceSymbols) == 0:
            resLine += ' '
        return resLine

    def dropPiece(self, capturedPiece, pos, b, p1, p2):     # returns -1 if invalid drop
        pawnFlag = False
        if self.case == "UPPER":
            capturedPiece.symbol = capturedPiece.symbol.upper()
        else:
            capturedPiece.symbol = capturedPiece.symbol.lower()

        if (len(self.capturedPieceList) == 0):                  # if player doesn't have any captured pieces
            return -1
        if not capturedPiece.symbol in self.capturedPieceSymbols:   # if player tries to drop a piece they don't have
            return -1
        if pos in p1.piecePosList or pos in p2.piecePosList:    # if dropped on top of an existing piece
            return -1
        if isinstance(capturedPiece, Pawn):
            if pos in self.promotionZone:       # cannot drop pawn in promotion zone
                return -1
            for each in self.pieceList:         # cannot drop pawn in same column as another
                if isinstance(each, Pawn):
                    if each.pos[1] == pos[1]:
                        return -1
            pawnFlag = True
            # cannot be dropped onto immediate checkmate
            # cannot be dropped onto same column as pawn of same player

        p = capturedPiece
        p.pos = pos
        self.piecePosList += [p.pos]
        self.pieceList += [p]
        self.updatePiecePosList()
        p.player = self
        if hasattr(p, 'diff'):
            if self.case == "UPPER":
                p.diff = -1
            else:
                p.diff = 1
        if pawnFlag and b.isCheckmate(p1, p2):   # pawn cannot be dropped in a way that results in checkmate
            return -1
        self.capturedPieceSymbols.remove(capturedPiece.symbol)
        self.capturedPieceList.remove(capturedPiece)
        del capturedPiece




