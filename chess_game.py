from game import *
from piece import *
from utils import *
import argparse

# Tested and working on python3.6

numDict = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5
}

letterDict = {
    '1': 'a',
    '2': 'b',
    '3': 'c',
    '4': 'd',
    '5': 'e',
    '6': 'f'
}

parser = argparse.ArgumentParser(description='a chess game.')
parser.add_argument('-i', dest='interactive', action='store_true', help='plays in interactive mode')
parser.add_argument('-cpu', dest='file', type=str)
args = parser.parse_args()

p1=Player("UPPER")
p2=Player("lower")

if args.file == None: #if playing in interactive mode, no moves passed into the game
    filemoves = []
else:
    gameDict = parseTestCase(args.file)
    filemoves = gameDict['moves']
    initialPositions = gameDict['initialPieces']
    upperCaptures = gameDict['upperCaptures']
    lowerCaptures = gameDict['lowerCaptures']

    p1.clearPieces()
    p2.clearPieces()
    for each in initialPositions:
        promotionFlag=False
        temp = each['position']
        pos1 = (int(temp[1]), numDict[temp[0]])
        if each['piece'].isupper():
            tplayer=p1
        else:
            tplayer=p2

        psymbol = each['piece']
        if psymbol[0]=='+':         #initialize pieces
            promotionFlag=True
            psymbol = psymbol[1]
        if psymbol.upper() == 'R':
            tempPiece = Rook(pos1, tplayer)
        if psymbol.upper() == 'B':
            tempPiece = Bishop(pos1, tplayer)
        if psymbol.upper() == 'S':
            tempPiece = SilverGeneral(pos1, tplayer)
        if psymbol.upper() == 'G':
            tempPiece = GoldenGeneral(pos1, tplayer)
        if psymbol.upper() == 'K':
            tempPiece = King(pos1, tplayer)
        if psymbol.upper() == 'P':
            tempPiece = Pawn(pos1, tplayer)

        tempPiece.symbol = each['piece']
        if promotionFlag:
            tempPiece.isPromoted = True
        if each['piece'].isupper():
            tempPiece.player = p1
            p1.pieceList += [tempPiece]
        else:
            tempPiece.player = p2
            p2.pieceList += [tempPiece]

    for each in upperCaptures:       # initialize captures
        tempPiece = Piece()
        psymbol = each
        if psymbol == 'R':
            tempPiece = Rook(pos1, tplayer)
        if psymbol == 'B':
            tempPiece = Bishop(pos1, tplayer)
        if psymbol == 'S':
            tempPiece = SilverGeneral(pos1, tplayer)
        if psymbol == 'G':
            tempPiece = GoldenGeneral(pos1, tplayer)
        if psymbol == 'K':
            tempPiece = King(pos1, tplayer)
        if psymbol == 'P':
            tempPiece = Pawn(pos1, tplayer)
        p1.updateCapturedPieceList(tempPiece)

    for each in lowerCaptures:
        tempPiece = Piece()
        psymbol = each
        if psymbol == 'r':
            tempPiece = Rook(pos1, tplayer)
        if psymbol == 'b':
            tempPiece = Bishop(pos1, tplayer)
        if psymbol == 's':
            tempPiece = SilverGeneral(pos1, tplayer)
        if psymbol == 'g':
            tempPiece = GoldenGeneral(pos1, tplayer)
        if psymbol == 'k':
            tempPiece = King(pos1, tplayer)
        if psymbol == 'p':
            tempPiece = Pawn(pos1, tplayer)
        p2.updateCapturedPieceList(tempPiece)

    p2.updatePiecePosList()
    p1.updatePiecePosList()
# initialize players using piece positions, and captured pieces list

Game(p1, p2, filemoves)