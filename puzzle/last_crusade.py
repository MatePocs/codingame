import sys
import math
from enum import Enum

direction_up = 'UP'
direction_down = 'DOWN'
direction_left = 'LEFT'
direction_right = 'RIGHT'

class Room:
    """
    Main reason for class is to keep track of entrances
    and exits in a dictionary
    """

    def __init__(self, roomtype):
        """
        setting up the dictionary
        keys are input directions
        values are output directions
        """
        roomtype = int(roomtype)

        self.move_direction = {}
        if roomtype == 1:
            self.move_direction[direction_up] = direction_down
            self.move_direction[direction_left] = direction_down
            self.move_direction[direction_right] = direction_down
        elif roomtype == 2:
            self.move_direction[direction_left] = direction_right
            self.move_direction[direction_right] = direction_left
        elif roomtype == 3:
            self.move_direction[direction_up] = direction_down
        elif roomtype == 4:
            self.move_direction[direction_up] = direction_left
            self.move_direction[direction_right] = direction_down
        elif roomtype == 5:
            self.move_direction[direction_up] = direction_right
            self.move_direction[direction_left] = direction_down
        elif roomtype == 6:
            self.move_direction[direction_left] = direction_right
            self.move_direction[direction_right] = direction_left
        elif roomtype == 7:
            self.move_direction[direction_up] = direction_down
            self.move_direction[direction_right] = direction_down
        elif roomtype == 8:
            self.move_direction[direction_left] = direction_down
            self.move_direction[direction_right] = direction_down
        elif roomtype == 9:
            self.move_direction[direction_up] = direction_down
            self.move_direction[direction_left] = direction_down
        elif roomtype == 10:
            self.move_direction[direction_up] = direction_left
        elif roomtype == 11:
            self.move_direction[direction_up] = direction_right
        elif roomtype == 12:
            self.move_direction[direction_right] = direction_down
        elif roomtype == 13:
            self.move_direction[direction_left] = direction_down

class MapFunctions:
    """
    just keeping track of different functions
    """

    @staticmethod
    def opposite_direction(direction):
        """
        Returns the opposite direction
        """
        if direction == direction_down:
            opposite_direction = direction_up
        elif direction == direction_up:
            opposite_direction = direction_down
        elif direction == direction_left:
            opposite_diretions = direction_right
        elif direction == direction_right:
            opposite_direction = direction_left
        
        return opposite_direction

    @staticmethod
    def coordinates_after_move(direction, current_row, current_col):
        """
        Returns the row and column after moving in a certain direction
        """
        if direction == direction_down:
            new_row = current_row + 1
            new_col = current_col
        elif direction == direction_up:
            new_row = current_row - 1
            new_col = current_col
        elif direction == direction_left:
            new_row = current_row
            new_col = current_col - 1
        elif direction == direction_right:
            new_row = current_row
            new_col = current_col + 1

        return new_row, new_col

    @staticmethod
    def convert_pos_to_direction(pos):
        """
        converts the string pos to direction enum
        """
        if pos == 'TOP':
            direction = direction_up
        elif pos == 'LEFT':
            direction = direction_left
        elif pos == 'RIGHT':
            direction = direction_right
        
        return direction

my_map = []

# w: number of columns.
# h: number of rows.
w, h = [int(i) for i in input().split()]
for i in range(h):
    line = input()  
    # represents a line in the grid and contains W integers. 
    # Each integer represents one room of a given type.
    line = line.split()
    my_map.append(line)
    # my_map's first coordinate: rows from 0 to h-1
    # second coordinate: column from 0 to w-1
    

ex = int(input())  # the coordinate along the X axis of the exit (not useful for this first mission, but must be read).

# game loop
while True:
    xi, yi, pos = input().split()
    xi = int(xi)
    yi = int(yi)

    # x is the col num, left to right
    # y is the row num, up to down

    current_room_type = my_map[yi][xi]
    print("Current x: " + str(xi), file = sys.stderr)
    print("Current y: " + str(yi), file = sys.stderr)
    print("Current room type: " + str(current_room_type), file = sys.stderr)
    current_room = Room(current_room_type)
    enter_direction = MapFunctions.convert_pos_to_direction(pos)
    exit_direction = current_room.move_direction[enter_direction]
    new_row, new_col = MapFunctions.coordinates_after_move(exit_direction, yi, xi)

    output = str(new_col) + ' ' + str(new_row)

    # One line containing the X Y coordinates of the room in which you believe Indy will be on the next turn.
    print(output)
