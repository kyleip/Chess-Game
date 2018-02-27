from utils import *
from piece import *
from player import *

pieceSymbols = {
	"R": "Rook",
	"B": "Bishop",
	"S": "SilverGeneral",
	"G": "GoldenGeneral",
	"K": "King",
	"P": "Pawn"
}

numDict = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 6,
    'g': 7,
    'h': 8
}

#board is a grid of the symbols of the pieces in play
class Board(object):
    symbolGrid = [[None] * 8 for i in range(8)]
    numofTurns = 0
    piecePosList = []
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

        for x in range(0,8):
            for y in range(0,8):
                self.symbolGrid[x][y] = ''

        for each in self.p1.pieceList:
            x = each.pos[1] - 1
            y = each.pos[0] - 1
            self.symbolGrid[x][y] = each.symbol
            self.piecePosList += [x, y]
        for each in self.p2.pieceList:
            x = each.pos[1] - 1
            y = each.pos[0] - 1
            self.symbolGrid[x][y] = each.symbol
            self.piecePosList += [x, y]

    def __len__(self, board):
        return len(board[0])

    def turn(self):
        self.numofTurns += 1

    def updateGrid(self, p1, p2):
        self.symbolGrid = [[''] * 8 for i in range(8)]
        for each in p1.pieceList:
            x=each.pos[1] - 1
            y=each.pos[0] - 1
            self.symbolGrid[x][y]=each.symbol
        for each in p2.pieceList:
            x = each.pos[1] - 1
            y = each.pos[0] - 1
            self.symbolGrid[x][y] = each.symbol
        self.piecePosList=p1.piecePosList
        self.piecePosList+=p2.piecePosList


    # function to tell whether a player's king's position is in the possible move list of the other player's pieces
    def isCheck(self, p1, p2):      # p2 is defender!!
        for each in p1.pieceList:
            kpos = p2.getKingPos()
            if kpos in each.possibleMoves() and not collision(each, [(each.pos), (kpos)], p1, p2):
                return True

        return False

    #function to tell if a player is in checkmate
    def isCheckmate(self, p1, p2):
        if not self.isCheck(p1, p2):
            return False
        if (len(self.availableMoves(p1, p2)) == 0):
            return True
        else:
            return False

    #function that gives all the moves a player can make that allow them to not be in check
    #returns moves in the format (symbol, pos1, pos2). if a drop, pos2 will be (-100, -100)
    def availableMoves(self, p1, p2):
        p1.updatePiecePosList()
        p2.updatePiecePosList()
        posList = []
        for i in range(0, len(p2.pieceList)):       # look at every piece in p2
            temp = p2.pieceList[i].pos
            for one in p2.pieceList[i].possibleMoves():    #look at every move for that piece
                captureFlag = False

                p2.pieceList[i].pos = one       #move that piece (will be moved back)
                p2.updatePiecePosList()
                if capture(one, p1):        #if that move is a capture
                    captureFlag = True
                    tempPiece = None
                    for j in range(len(p1.pieceList)):  #go through pieces of p1
                        if one == p1.pieceList[j].pos:
                            tempPiece = p1.pieceList[j]
                            del p1.pieceList[j]         #capture that piece
                            p1.piecePosList.remove(one)
                            p1.updatePiecePosList()
                            captureFlag = True
                            p2.pieceList[i].pos = one
                            break

                if not self.isCheck(p1, p2):        #if this move results in a not check
                    pSymbol = p2.pieceList[i].symbol
                    posList += [(pSymbol, temp, one)] #push that move into posList
                if captureFlag:
                    p1.pieceList += [tempPiece]   #if a piece was captured put it back
                    p1.piecePosList += [one]
                    p1.updatePiecePosList()

            p2.pieceList[i].pos = temp      #move the piece back
            p2.updatePiecePosList()

        for i in range(1, 6):            # tests to see if a drop will bring that player out of check
            for j in range(1, 6):
                tPos = (i, j)
                if not (tPos in p1.piecePosList or tPos in p2.piecePosList):
                    p2.piecePosList += [tPos]
                    if not self.isCheck(p1, p2):
                        for each in p2.capturedPieceSymbols:        # if so, return it with a [symbol, pos, (-100,-100)]
                            posList += [(each, tPos, (-100, -100))]
                    p2.piecePosList.remove(tPos)
        return posList

    def updatePlayers(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

def capture(pos, p1): # tests if a move is a capture or not
    if pos in p1.piecePosList:
        return True
    else:
        return False


def collision(piece, posList, p1, p2): # tests if a move involves a piece jumping another piece

    if (isinstance(piece, Knight)):
        # print('asdfas')
        return False

    if not (isinstance(piece, Bishop) or isinstance(piece, Rook)): # only rooks and bishops can do that
        return False

    xdiff = posList[0][0] - posList[1][0]
    ydiff = posList[0][1] - posList[1][1]

    x0 = posList[0][0]
    y0 = posList[0][1]

    if xdiff < 0: #whether slope is + or -
        dx = 1
    else:
        dx = -1

    if ydiff<0:
        dy = 1
    else:
        dy = -1

    if isinstance(piece, Rook):         # tests if there are pieces within the rook's path from pos1 to pos2
        if xdiff == 0:
            if ydiff > 0:
                for i in range(posList[0][1] - 1, posList[1][1], -1):
                    if ((posList[0][0], i)) in p1.piecePosList or ((posList[0][0], i)) in p2.piecePosList:
                        return True
            else:
                for i in range(posList[0][1] + 1, posList[1][1], 1):
                    if ((posList[0][0], i)) in p1.piecePosList or ((posList[0][0], i)) in p2.piecePosList:
                        return True

        if ydiff == 0:
            if xdiff > 0:
                for i in range (posList[0][0] - 1, posList[1][0], -1):
                    if ((i, posList[0][1])) in p1.piecePosList or ((i, posList[0][1])) in p2.piecePosList:
                        return True
            else:
                for i in range (posList[0][0] + 1, posList[1][0], 1):
                    if ((i, posList[0][1])) in p1.piecePosList or ((i, posList[0][1])) in p2.piecePosList:
                        return True


    if isinstance(piece, Bishop):       # tests if there are pieces within the bishop's path from pos1 to pos2
        if ydiff == 0 and (xdiff == 1 or xdiff == -1):
            return False
        if xdiff == 0 and (ydiff == 1 or ydiff == -1):
            return False
        posBefore = ((posList[1][0] - dx,posList[1][1] - dy))
        while ((x0,y0) != posBefore):
            x0 += dx
            y0 += dy
            if ((x0, y0) in p1.piecePosList or (x0, y0) in p2.piecePosList):
                return True

    return False
