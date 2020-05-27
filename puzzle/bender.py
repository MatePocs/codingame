import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

char_start = '@'
char_unbreakable_wall = '#'
char_breakable_wall = 'X'

map = []

starting_rownum = None
starting_colnum = None

l, c = [int(i) for i in input().split()]
for i in range(l):
    row = input()
    map.append(row)
    if starting_rownum is None: 
        for j in range(c):
            if row[j] == char_start:
                starting_rownum = i
                starting_colnum = j
                break

# map's first coord: which row, second: which col

class Bender:

    def __init__(self, starting_rownum, starting_colnum):
        self.rownum = starting_rownum
        self.colnum = starting_colnum
        self.moves_history = []
        self.inverted = False
        self.moveorder = ['SOUTH', 'EAST', 'NORTH', 'WEST']
        self.invert = False
        self.breaker_mode = False

    def move(self):
        # first, decide on direction
        direction = self.decide_direction

        # then, adjust position

        # checks what we stepped on, if X: break it, if T: teleport

        # and finally, add step to moves_history

    def decide_direction(self):
        # check if standing on direction_modifiers
        if map[self.rownum][self.colnum] == 'S':
            direction = 'SOUTH'
        elif map[self.rownum][self.colnum] == 'E':
            direction = 'EAST'
        elif map[self.rownum][self.colnum] == 'N':
            direction = 'NORTH'
        elif map[self.rownum][self.colnum] == 'W':
            direction = 'WEST'

        # if was not standing on direction modifiers

    def is_move_doable(self, move):
        # checks if the move is doable from the current position
        target_rownum, target_colnum = self.target_coordinates(move)

        target_char = map[target_rownum][target_colnum]

        if target_char == char_unbreakable_wall:
            doable = False
        elif target_char == char_breakable_wall and self.breaker_mode:
            doable = False
        else:
            doable = True

    
    def target_coordinates(self, move):
        # calculates target coordinates based on move and current position
        if move == 'SOUTH':
            target_rownum = self.rownum + 1
            target_colnum - self.colnum
        elif move == 'NORTH':
            target_rownum = self.rownum - 1
            target_colnum - self.colnum
        elif move == 'EAST':
            target_rownum = self.rownum
            target_colnum = self.colnum + 1
        elif move == 'WEST':
            target_rownum = self.rownum
            target_colnum = self.colnum - 1

        return target_rownum, target_colnum

while continues:


# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr)

print("answer")
