# each piece has a symbol, a player, a promotion attribute, and function that returns a list of its possile moves
class Piece(object):

    def __init__(self, pos, player):
        self.pos = pos
        self.player = player
        self.isPromoted = False
        self.isSupported = False
        if player.case == 'UPPER':
            self.diff = -1
        else:
            self.diff = 1

    def checksOpponent(self, player):
        if player.kingpos in self.possibleMoves():
            return True
        else:
            return False

    def ownedbyPlayer(self, player):
        if (self.player == player):
            return True
        else:
            return False

    def posInbound(self, pos):
        x = pos[0]
        y = pos[1]
        # print(x, y)
        if x > 5 or x < 1:
            return False
        if y > 5 or y < 1:
            return False
        return True

    def removeTeamPos(self, posList, piecePosList):     # remove teams positions from possible moves
        for each in posList:
            if each in piecePosList:
                posList.remove(each)
        return posList

    def addSupportingMoves(self):
        resList = []
        ans = list(self.pos)
        for each in self.player.pieceList:
            if each.pos == (ans[0] - self.diff, ans[1]):
                resList += each.possibleMoves()
                print("added moves", resList)
        # print('hi')
        return resList
        # update player piece pos list


class Rook(Piece):
    def __init__(self, pos, player):
        super().__init__(pos, player)
        if player.case == 'UPPER':
            self.symbol = 'R'
        else:
            self.symbol = 'r'

    def promotion(self):
        self.isPromoted = True
        self.symbol = '+' + self.symbol

    def possibleMoves(self):
        posList = ([])
        for i in range (1,6):
            posList+=[(i, self.pos[1])]
            posList+=[(self.pos[0], i)]

        resList = self.removeTeamPos(posList, self.player.piecePosList)

        if self.isPromoted:
            ans = list(self.pos)
            res = resList
            for i in range(1, 4):
                for j in range(1, 4):
                    res += [(ans[0] + i - 2, ans[1] + j - 2)]
            resList = self.removeTeamPos(res, self.player.piecePosList)
            return resList
        resList += self.addSupportingMoves()
        return(resList)


class Bishop(Piece):

    def __init__(self, pos, player):
        super().__init__(pos, player)
        if (player.case == 'UPPER'):
            self.symbol = 'B'
        else:
            self.symbol = 'b'

    def promotion(self):
        self.isPromoted = True
        self.symbol = '+' + self.symbol

    def possibleMoves(self):
        #how to find this!!!
        posList = []
        diags = self.diagIntersects()
        temp = diags[0]

        x = temp[0]
        y = temp[1]
        while (self.posInbound( (x, y) )):
            posList += [(x, y)]
            x += 1
            y += 1
        temp = diags[1]
        x = temp[0]
        y = temp[1]
        while (self.posInbound( (x, y) )):
            posList += [(x, y)]
            x += 1
            y -= 1

        resList = self.removeTeamPos(posList, self.player.piecePosList)
        if self.isPromoted:
            ans = list(self.pos)
            res = posList

            for i in range(1, 4):
                for j in range(1, 4):
                    res += [(ans[0] + i - 2, ans[1] + j - 2)]
            resList = self.removeTeamPos(res, self.player.piecePosList)
        resList += self.addSupportingMoves()
        # print(resList)
        return resList

    def diagIntersects(self):
        res = list(self.pos)
        # print(res)
        x = res[0]
        y = res[1]
        while (x > 1 and y > 1):
            x -= 1
            y -= 1
        posList = [(x, y)]

        x = res[0]
        y = res[1]
        while (x > 1 and y < 5):
            x -= 1
            y += 1
        posList += [(x, y)]
        return posList

class SilverGeneral(Piece):

    def __init__(self, pos, player):
        super().__init__(pos, player)
        if (player.case == 'UPPER'):
            self.symbol = 'S'
        else:
            self.symbol = 's'

    def promotion(self):
        self.isPromoted = True
        self.symbol = '+' + self.symbol

    def possibleMoves(self):
        if not self.isPromoted:
            ans = list(self.pos)
            res = [(ans[0], ans[1])]
            for i in range (-1, 2):
                for j in range (-1, 2):
                    res += [(ans[0] + i, ans[1] + j)]
            res.remove((ans[0], ans[1] - self.diff))
            res.remove((ans[0], ans[1] + self.diff))
            res.remove((ans[0] - self.diff, ans[1]))
            resList = self.removeTeamPos(res, self.player.piecePosList)
        else:
            ans = list(self.pos)
            res = []
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if self.posInbound((ans[0] + i, ans[1] + j)):
                        if ((ans[0] + i, ans[1] + j) not in self.player.piecePosList):
                            res += [(ans[0] + i, ans[1] + j)]

            if (ans[0] - self.diff, ans[1] - self.diff) in res:
                res.remove((ans[0] - self.diff, ans[1] - self.diff))
            if (ans[0] - self.diff, ans[1] + self.diff) in res:
                res.remove((ans[0] - self.diff, ans[1] + self.diff))
        resList += self.addSupportingMoves()
        return res

class GoldenGeneral(Piece):

    def __init__(self, pos, player):
        super().__init__(pos, player)
        if (player.case == 'UPPER'):
            self.symbol = 'G'
        else:
            self.symbol = 'g'

    def possibleMoves(self):
        ans = list(self.pos)
        res = [(ans[0], ans[1])]
        for i in range (-1, 2):
            for j in range (-1, 2):
                if(self.posInbound((ans[0]+i,ans[1]+j))):
                    if ((ans[0]+i,ans[1]+j) not in self.player.piecePosList):
                        res+=[(ans[0]+i,ans[1]+j)]
        if (ans[0]-self.diff, ans[1]-self.diff) in res:
            res.remove((ans[0]-self.diff, ans[1]-self.diff))
        if (ans[0]-self.diff, ans[1]+self.diff) in res:
            res.remove((ans[0]-self.diff, ans[1]+self.diff))
        resList = self.removeTeamPos(res, self.player.piecePosList)
        resList += self.addSupportingMoves()
        return resList

class King(Piece):
    def __init__(self, pos, player=None):
        super().__init__(pos, player)
        if (player.case == 'UPPER'):
            self.symbol = 'K'
        else:
            self.symbol = 'k'

    def possibleMoves(self):
        ans = list(self.pos)
        res = []
        for i in range (-1, 2):
            for j in range (-1, 2):
                if self.posInbound((ans[0] + i, ans[1] + j)):
                    if (ans[0] + i, ans[1] + j) not in self.player.piecePosList:
                        res += [(ans[0] + i, ans[1] + j)]

        resList = self.removeTeamPos(res, self.player.piecePosList)
        resList += self.addSupportingMoves()
        return resList

class Pawn(Piece):
    def __init__(self, pos, player):
        super().__init__(pos, player)
        if (player.case == 'UPPER'):
            self.symbol = 'P'
        else:
            self.symbol = 'p'

    def possibleMoves(self):
        if not self.isPromoted:
            ans = list(self.pos)
            ans[0] += self.diff
            if (ans[0], ans[1]) in self.player.piecePosList:
                return []
            res = [tuple(ans)]
            return res
        else:
            ans = list(self.pos)
            res = [(ans[0], ans[1])]
            for i in range(-1, 2):
                for j in range(-1, 2):
                    res += [(ans[0] + i, ans[1] + j)]
            res.remove((ans[0] - self.diff, ans[1] - self.diff))
            res.remove((ans[0] - self.diff, ans[1] + self.diff))
            resList = self.removeTeamPos(res, self.player.piecePosList)

        resList += self.addSupportingMoves()
        return resList

    def promotion(self):
        self.isPromoted = True
        self.symbol = '+' + self.symbol
