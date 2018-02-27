from piece import *
from board import *

class Player(object):

    def __init__(self, case):
        self.case = case
        self.capturedPieceList = []
        self.capturedPieceSymbols = []
        if self.case == "UPPER":
            self.R1 = Rook((8, 1), self)
            self.R2 = Rook((8, 8), self)
            self.B1 = Bishop((8, 3), self)
            self.B2 = Bishop((8, 6), self)
            self.Q = Queen((8,4), self)
            self.K = King((8, 5), self)
            self.Kn1 = Knight((8,2), self)
            self.Kn2 = Knight((8,7), self)
            self.P1 = Pawn((7, 8), self)
            self.P2 = Pawn((7, 7), self)
            self.P3 = Pawn((7, 6), self)
            self.P4 = Pawn((7, 5), self)
            self.P5 = Pawn((7, 4), self)
            self.P6 = Pawn((7, 3), self)
            self.P7 = Pawn((7, 2), self)
            self.P8 = Pawn((7, 1), self)
        else:
            self.R1 = Rook((1, 1), self)
            self.R2 = Rook((1, 8), self)
            self.B1 = Bishop((1, 3), self)
            self.B2 = Bishop((1, 6), self)
            self.K = King((1, 5), self)
            self.Kn1 = Knight((1,2), self)
            self.Kn2 = Knight((1,7), self)
            self.Q = Queen((1,4), self)
            self.P1 = Pawn((2, 8), self)
            self.P2 = Pawn((2, 7), self)
            self.P3 = Pawn((2, 6), self)
            self.P4 = Pawn((2, 5), self)
            self.P5 = Pawn((2, 4), self)
            self.P6 = Pawn((2, 3), self)
            self.P7 = Pawn((2, 2), self)
            self.P8 = Pawn((2, 1), self)

        self.pieceList = [self.R1, self.R2, self.B1, self.B2, self.K, self.Q, self.P1, self.P2, self.P3, self.P4, self.P5,
                          self.P6, self.P7, self.P8, self.Kn1, self.Kn2]
        self.piecePosList = [self.R1.pos, self.R2.pos, self.B1.pos, self.B2.pos, self.K.pos, self.P1.pos, self.P2.pos,
                             self.P3.pos, self.P4.pos, self.P5.pos, self.P6.pos, self.P7.pos, self.P8.pos, self.Q.pos,
                             self.Kn1.pos, self.Kn2.pos]
        self.promotionZone = []
        # for i in range(1, 6):
        #     self.promotionZone += [(5, i)]

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
        del self.P1
        del self.P2
        del self.P3
        del self.P4
        del self.P5
        del self.P6
        del self.P7
        del self.P8
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




