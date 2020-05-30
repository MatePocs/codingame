import sys
import math

# map characters
char_start = '@'
char_unbreakable_wall = '#'
char_breakable_wall = 'X'
char_end = '$'

starting_direction = 'SOUTH'

my_map = []

starting_rownum = None
starting_colnum = None

l, c = [int(i) for i in input().split()]
for i in range(l):
    row = input()
    print(row, file = sys.stderr)
    my_map.append(row)
    if starting_rownum is None: 
        for j in range(c):
            if row[j] == char_start:
                starting_rownum = i
                starting_colnum = j
                break

# map's first coord: which row, second: which col

class Bender:

    def __init__(self, starting_rownum, starting_colnum, map):
        self.rownum = starting_rownum
        self.colnum = starting_colnum
        self.map = my_map
        self.current_direction = starting_direction
        self.direction_history = []
        self.inverted = False
        self.moveorder = ['SOUTH', 'EAST', 'NORTH', 'WEST']
        self.invert = False
        self.breaker_mode = False

    def move(self):
        # first, decide on direction
        direction = self.decide_direction()
        print(direction, file = sys.stderr)

        # then, adjust position
        self.current_direction = direction
        self.rownum, self.colnum = self.target_coordinates(direction)

        # checks what we stepped on
        # if X: break it 
        # if T: teleport

        # add direction to moves history
        self.direction_history.append(direction)

    def decide_direction(self):
        
        # as a first step, check if standing on direction modifier
        direction = self.check_for_direction_modifiers()
        # if we did not select a direction, go with the current direction
        if direction is None: direction = self.current_direction

        # at this point, we will have a direction, either from dirmod or the previous step
        # check if it's doable
        if self.is_move_doable(direction):
            return direction
        # if direction was not doable, check all 4 in move order, one will be doable
        else:
            for i in range(0,3):
                direction = self.moveorder[i]
                if self.is_move_doable(direction):
                    return direction

        # TODO: handle inversion
            

    def check_for_direction_modifiers(self):
        direction = None
        current_char = self.get_current_char_on_map()
        # check if standing on direction_modifiers
        if current_char == 'S':
            direction = 'SOUTH'
        elif current_char == 'E':
            direction = 'EAST'
        elif current_char == 'N':
            direction = 'NORTH'
        elif current_char == 'W':
            direction = 'WEST'

        return direction

    def get_current_char_on_map(self):
        return self.map[self.rownum][self.colnum]

    def is_move_doable(self, direction):
        # checks if the move is doable from the current position
        target_rownum, target_colnum = self.target_coordinates(direction)

        target_char = self.map[target_rownum][target_colnum]

        if target_char == char_unbreakable_wall:
            doable = False
        elif target_char == char_breakable_wall and not self.breaker_mode:
            doable = False
        else:
            doable = True

        return doable
    
    def target_coordinates(self, direction):
        # calculates target coordinates based on direction and current position
        if direction == 'SOUTH':
            target_rownum = self.rownum + 1
            target_colnum = self.colnum
        elif direction == 'NORTH':
            target_rownum = self.rownum - 1
            target_colnum = self.colnum
        elif direction == 'EAST':
            target_rownum = self.rownum
            target_colnum = self.colnum + 1
        elif direction == 'WEST':
            target_rownum = self.rownum
            target_colnum = self.colnum - 1

        return target_rownum, target_colnum

    def check_if_over(self):
        # over if stepped on ending character
        current_char = self.get_current_char_on_map()
        if current_char == char_end:
            return True
        else:
            return False
        # TODO also over if we reached a loop

bender = Bender(starting_colnum, starting_colnum, my_map)
game_over = False
while not game_over:
    bender.move()
    game_over = bender.check_if_over()

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr)

for direction in bender.direction_history:
    print(direction)
