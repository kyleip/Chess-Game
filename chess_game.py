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
    'e': 5,
    'f': 6,
    'g': 7,
    'h': 8
}

letterDict = {
    '1': 'a',
    '2': 'b',
    '3': 'c',
    '4': 'd',
    '5': 'e',
    '6': 'f',
    '7': 'g',
    '8': 'h',
    '9': 'i'
}

p1=Player("UPPER")
p2=Player("lower")


filemoves = []

# initialize players using piece positions, and captured pieces list

Game(p1, p2, filemoves)

#to do:
# castling
# en passant