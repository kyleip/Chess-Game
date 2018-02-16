from board import *
from player import *

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


def Game(p1, p2, filemoves):
    errFlag = False
    b = Board(p1, p2)
    numofTurns = 0
    checkFlag = False
    lastMove = ""
    while True:

        if len(filemoves) == 0:       # if in interactive mode
            print(lastMove)
            print(stringifyBoard(b.symbolGrid))
            if b.isCheck(p1, p2):
                print('p2 in check')
                print('Available Moves:')
                p1.updatePiecePosList()
                p2.updatePiecePosList()
                mList = parseAvailableMoves(b.availableMoves(p1, p2))
                printAvailableMoves(mList)
            if b.isCheck(p2, p1):
                print('p1 in check')
                print('Available Moves:')
                p1.updatePiecePosList()
                p2.updatePiecePosList()
                mList = parseAvailableMoves(b.availableMoves(p2, p1))
                printAvailableMoves(mList)
            print(p1.printCapturedPieceList())
            print(p2.printCapturedPieceList())

            turnString = whoseTurn(numofTurns, p1, p2).case
            turnString += '> '
            move = input(turnString)
            if move == "quit":
                break
        else:                       # if in file mode
            if numofTurns == 400:

                lastMove += ' player action: '
                lastMove += move
                printEndGame(b, lastMove, p1, p2, numofTurns, errFlag)
            elif numofTurns >= len(filemoves):
                lastMove += ' player action: '
                lastMove += move
                printEndGame(b, lastMove, p1, p2, numofTurns, errFlag)
            move = filemoves[numofTurns]

        if numofTurns % 2 == 1:
            lastMove = p1.case
            attacker = p1
            defender = p2
        else:
            lastMove = p2.case
            attacker = p2
            defender = p1

        if moveIsValid(parseMove(move), attacker, checkFlag, b):    # if the move is valid
            posList = parseMove(move)
            if parseMove(move)[0] == ((-1, -1)):    # parseMove will return a (-1,-1) if move is invalid
                errFlag = True
                break

            if posList[0][0] == -100: # if it is a drop
                errFlag = True
                for each in attacker.capturedPieceSymbols:
                    if posList[0][1].lower() == each.lower(): # if a player doesn't have that piece, error
                        errFlag = False
                        break
                for each in attacker.capturedPieceList:
                    if each.symbol.lower() == posList[0][1].lower():
                        res = attacker.dropPiece(each, posList[1], b, attacker, defender)
                        if res == -1:                                   # res will be -1 if there's an error
                            errFlag = True                              # see dropPiece function in player.py
                            break

            # moves here are in the format (pos0, pos1)
            for i in range(len(attacker.pieceList)):
                if attacker.pieceList[i].pos == posList[0]:             # finds piece in pos0
                    p = attacker.pieceList[i]
                    if collision(p, posList, attacker, defender):       # if there's a collision (see collision function)
                        errFlag = True
                        break
                    attacker.pieceList[i].pos = posList[1]              # move piece to pos1
                    attacker.updatePiecePosList()
                    if (b.isCheck(defender, attacker)):                  # if that move puts attacker in check
                        if capture(posList[1], defender):
                            for j in range(len(defender.pieceList)):
                                if posList[1] == defender.pieceList[j].pos:
                                    attacker.updateCapturedPieceList(defender.pieceList[j])
                                    del defender.pieceList[j]
                                    defender.piecePosList.remove(posList[1])
                                    defender.updatePiecePosList()
                                    break
                        if (b.isCheck(defender, attacker)):             # if player is still in check
                            errFlag = True
                            break

                    if (attacker.pieceList[i].pos in attacker.promotionZone or posList[0] in attacker.promotionZone) \
                            and len(posList) > 2:
                        if (attacker.pieceList[i].isPromoted):
                            errFlag = True
                            break
                        if (hasattr(attacker.pieceList[i], 'promotion')):   # if piece is promotable
                            attacker.pieceList[i].promotion()           # promote piece
                            attacker.updatePiecePosList()
                        else:
                            errFlag = True
                            break
                    elif attacker.pieceList[i].pos in attacker.promotionZone \
                            and isinstance(attacker.pieceList[i], Pawn):
                        attacker.pieceList[i].promotion()
                        attacker.updatePiecePosList()
                        break
                    elif len(posList) > 2 and not hasattr(attacker.pieceList[i], 'promotion'):
                        errFlag = True
                        break
                    elif len(posList) > 2 and not attacker.pieceList[i].pos in attacker.promotionZone:
                        errFlag = True
                        break

                    if capture(posList[1], defender):                    # if that move is a capture
                        for j in range(len(defender.pieceList)):
                            if posList[1] == defender.pieceList[j].pos:       # delete piece and update positions
                                attacker.updateCapturedPieceList(defender.pieceList[j])
                                del defender.pieceList[j]
                                defender.piecePosList.remove(posList[1])
                                break

            if b.isCheck(attacker, defender):
                checkFlag = True
            else:
                checkFlag = False

        else:
            errFlag = True

        if errFlag is True:
            lastMove += ' player action: '
            lastMove += move
            printEndGame(b, lastMove, p1, p2, numofTurns, errFlag)
        if numofTurns % 2 == 1:   # update player
            p1 = attacker
            p2 = defender
        else:
            p2 = attacker
            p1 = defender
        b.updateGrid(p1, p2)     # update symbolGrid
        b.updatePlayers(p1, p2)
        p1.updatePiecePosList()
        p2.updatePiecePosList()
        numofTurns += 1           # increment number of turns

        if b.isCheckmate(p1, p2):
            lastMove += ' player action: '
            lastMove += move
            printEndGame(b, lastMove, p1, p2, numofTurns, errFlag)
        if b.isCheckmate(p2, p1):
            lastMove += ' player action: '
            lastMove += move
            printEndGame(b, lastMove, p1, p2, numofTurns, errFlag)


def parseMove(move):
    wordList = move.split()
    promotedFlag = False
    if wordList[0] == "move":
        pos1 = (int(wordList[1][1]), numDict[wordList[1][0]])
        pos2 = (int(wordList[2][1]), numDict[wordList[2][0]])
        if len(wordList) > 3:
            if wordList[3] == "promote":
                promotedFlag = True
            else:
                return False

    elif wordList[0] == "drop":
        pos1 = (-100, wordList[1])
        pos2 = (int(wordList[2][1]), numDict[wordList[2][0]])
    else:
        pos1 = (-1, -1)
        pos2 = (-1, -1)
    posList = [pos1, pos2]
    if promotedFlag:        # just add a dummy to be able to tell that we want a promotion
        posList += [(-100, -100)]
    return posList


# various checks to see if move is valid (not exhaustive)
def moveIsValid(posList, player, checkFlag, b):
    if posList[0] == posList[1]:      # can't move piece to its own position
        return False
    tempList = []
    for i in range(0, 2):
        tempList += [posList[i]]
    for each in tempList:
        x = each[0]
        y = each[1]
        if x == -100:             # if the move is a drop, it will be valid
            return True
        if x > 6 or x < 0:          # if the move is not on the board
            return False
        if y > 6 or y < 0:
            return False

    exists = False
    piece = None
    for each in player.pieceList:   # if the piece is owned by the player
        if each.pos == posList[0]:
            piece = each
            exists = True
            break

    if exists is False:
        return False

    if posList[1] not in piece.possibleMoves():      # if a piece cannot go there
        return False

    return True


def whoseTurn(numofTurns, p1, p2):      # function to return whose turn it is
    if numofTurns % 2 == 1:
        return p1
    else:
        return p2


# psymbol, pos1, pos2
def printAvailableMoves(moveList):
    moveList.sort(key=lambda tup: (tup[0], tup[1], tup[2]))
    for each in moveList:
        for i in range(0, len(each)):
            print(each[i], end='')
            if i == len(each)-1:
                print('')
            else:
                print(' ', end='')


def parseAvailableMoves(moveList):
    listMoves = list(moveList)
    resList = []
    for i in range(0, len(listMoves)):
        pos1 = ""
        pos2 = ""
        tWord = []
        list2Moves = list(listMoves[i])
        if list2Moves[2][1] == -100:     # if pos2 is -100, we know that it's a drop (see availableMoves function)
            pos1 += letterDict[str(list2Moves[1][1])]
            pos1 += str(list2Moves[1][0])
            tWord += ['drop']
            tWord += [list2Moves[0][0].lower()]
            tWord += [pos1]
            resList += [tWord]
        else:
            pos1 += letterDict[str(list2Moves[1][1])]
            pos2 += letterDict[str(list2Moves[2][1])]
            pos1 += str(list2Moves[1][0])
            pos2 += str(list2Moves[2][0])
            tWord += ['move']
            tWord += [pos1]
            tWord += [pos2]
            resList += [tWord]
    return resList


# if the end of a game, print the board and state of the game (won, draw, available moves)
def printEndGame(b, lastMove, p1, p2, numofTurns, errFlag):
    print(lastMove)
    print(stringifyBoard(b.symbolGrid))
    print(p1.printCapturedPieceList())
    print(p2.printCapturedPieceList(), end='\n\n')
    if b.isCheckmate(p2, p1) and not errFlag:
        turnString = 'lower player wins.  Checkmate.'
    elif b.isCheckmate(p1, p2) and not errFlag:
        turnString = 'UPPER player wins.  Checkmate.'
    elif numofTurns >= 200 and not errFlag:
        turnString = "Tie game.  Too many moves."
    elif errFlag is True:
        player = whoseTurn(numofTurns, p2, p1).case
        turnString = player + ' player wins.  Illegal move.'
    else:
        for each in p1.pieceList:
            kpos = p2.getKingPos()
            if kpos in each.possibleMoves() and not collision(each, [(each.pos), (kpos)], p1, p2):
                print('lower player is in check!')
                print('Available moves:')
                mList = parseAvailableMoves(b.availableMoves(p1, p2))
                printAvailableMoves(mList)
                break
        for each in p2.pieceList:
            kpos = p1.getKingPos()
            if kpos in each.possibleMoves() and not collision(each, [(each.pos), (kpos)], p2, p1):
                print('UPPER player is in check!')
                print('Available moves:')
                mList = parseAvailableMoves(b.availableMoves(p2, p1))
                printAvailableMoves(mList)
                break
        turnString = whoseTurn(numofTurns, p1, p2).case
        turnString += '> '
    print(turnString)
    exit(0)


if __name__ == "__main__":
    p1 = Player('UPPER')
    p2 = Player('lower')
    Game(p1, p2)
