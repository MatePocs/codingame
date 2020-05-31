import sys
import math

# map characters
char_start = '@'
char_unbreakable_wall = '#'
char_breakable_wall = 'X'
char_end = '$'
char_breaker = 'B'
char_empty_space = ' '
char_inverter = 'I'
char_teleport = 'T'

starting_direction = 'SOUTH'

my_map = []

starting_rownum = None
starting_colnum = None

teleport_rownums = []
teleport_colnums = []

l, c = [int(i) for i in input().split()]
for i in range(l):
    row = input()
    print(row, file = sys.stderr)
    my_map.append(row)
    # checks for teleport gates
    for j in range(c):
        if row[j] == char_teleport:
            teleport_rownums.append(i)
            teleport_colnums.append(j)
    # checks for starting rownum
    if starting_rownum is None: 
        for j in range(c):
            if row[j] == char_start:
                starting_rownum = i
                starting_colnum = j
                break

# printing teleport gates
print(teleport_rownums, file = sys.stderr)
print(teleport_colnums, file = sys.stderr)

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
        self.breaker_mode = False
        self.log = []
        self.record_in_log()

    def move(self):
        # first, decide on direction
        direction = self.decide_direction()
        #print(direction, file = sys.stderr)

        # then, adjust position
        self.current_direction = direction
        self.rownum, self.colnum = self.target_coordinates(direction)

        # checks what we stepped on
        self.handle_space_stepped_on()

        # add direction to moves history
        self.direction_history.append(direction)

        # add current state to log history
        self.record_in_log()

    def record_in_log(self):
        # records current state
        current_state = self.construct_state()
        self.log.append(current_state)

    def construct_state(self):
        # returns a tuple with the current state
        return (self.current_direction,self.rownum, self.colnum, self.inverted, self.breaker_mode)

    def reset_log(self):
        # resets log, e.g. after wall break
        self.log = []

    def check_if_state_is_in_log(self):
        # checks if the current state was already in the log
        found_in_log = False
        current_state = self.construct_state()
        for i in range(0, len(self.log)-1):
            if self.log[i] == current_state:
                found_in_log = True
                break

        return found_in_log

    def handle_space_stepped_on(self):
        current_char = self.get_current_char_on_map()
        # if B: change breakable mode
        if current_char == char_breaker:
            self.switch_breaker_mode()
        # if X: break it and re-set log
        elif current_char == char_breakable_wall:
            self.break_current_space_wall()
            self.reset_log()
        # if I: invert
        elif current_char == char_inverter:
            self.switch_inverted()
        # if T: teleport
        elif current_char == char_teleport:
            self.teleport()

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
        # depending on the inversion, can be 0 to 3 or 3 to 0
        else:
            for i in range(0,3):
                if self.inverted:
                    direction = self.moveorder[3-i]
                else:
                    direction = self.moveorder[i]
                if self.is_move_doable(direction):
                    return direction

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

    def break_current_space_wall(self):
        # sets the current character position to char_empty_space
        current_row = self.map[self.rownum]
        current_row = current_row[:self.colnum] + char_empty_space +current_row[self.colnum+1:]
        self.map[self.rownum] = current_row

    def switch_breaker_mode(self):
        # changes breaker mode to false if it was true and vica versa
        if self.breaker_mode == True:
            self.breaker_mode = False
            print("Breaker Mode False", file = sys.stderr)
        else:
            self.breaker_mode = True
            print("Breaker Mode True", file = sys.stderr)
    
    def switch_inverted(self):
        # changes breaker mode to false if it was true and vica versa
        if self.inverted == True:
            self.inverted = False
        else:
            self.inverted = True

    def teleport(self):
        # uses teleport_rownums and teleport_colnums, move to other
        #print("Teleporting from: " + str(self.rownum) + ', ' + str(self.colnum), file = sys.stderr)
        if self.rownum == teleport_rownums[0] and self.colnum == teleport_colnums[0]:
            self.rownum = teleport_rownums[1]
            self.colnum = teleport_colnums[1]
        elif self.rownum == teleport_rownums[1] and self.colnum == teleport_colnums[1]:
            self.rownum = teleport_rownums[0]
            self.colnum = teleport_colnums[0]
        #print("Teleporting to " + str(self.rownum) + ', ' + str(self.colnum), file = sys.stderr)

    def is_move_doable(self, direction):
        # checks if the move is doable from the current position
        #print("Checking if direction " + direction + " is doable", file = sys.stderr)
        target_rownum, target_colnum = self.target_coordinates(direction)
        #print("Target rownum, target_colnum = " + str(target_rownum) + ", " + str(target_colnum), file = sys.stderr)
        target_char = self.map[target_rownum][target_colnum]
        #print("Target char is " + target_char, file = sys.stderr)
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
            return 'Reached_Finish'
        elif self.check_if_state_is_in_log():
            return 'Loop'
        else:
            return 'Not'
        # TODO also over if we reached a loop

bender = Bender(starting_rownum, starting_colnum, my_map)
game_over = False

round_number = 1

while not game_over:
    print("Current Round: " + str(round_number), file = sys.stderr)
    bender.move()
    print("Bender Moves to :" + bender.current_direction, file = sys.stderr)
    print("Current row and colnum: " + str(bender.rownum) + ', ' + str(bender.colnum), file = sys.stderr)
    game_over_state = bender.check_if_over()
    if game_over_state != 'Not':
        game_over = True
    round_number += 1

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr)
if game_over_state == 'Loop':
    print('LOOP')
else:
    for direction in bender.direction_history:
        print(direction)
