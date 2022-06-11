import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

w, h = [int(i) for i in input().split()]
start_row, start_col = [int(i) for i in input().split()]
n = int(input())
maps = []
for i in range(n):
    curr_map = []
    for j in range(h):
        map_row = input()
        curr_map.append(map_row)
    maps.append(curr_map)

# check of input
# for i in range(n):
#    print(maps[i], file=sys.stderr, flush=True)

# well we need to check the maps one by one
def number_of_steps_to_treasure(map):
    number_of_steps = 0
    covered_position = set() # a tuple, so we can keep track of points we already covered
    current_position_row = w
    current_position_col = h

    # ^, v, <, >

    while True:
        curr_symbol = map[current_position_row][current_position_col]
        if  curr_symbol == "^":
            current_position_row -= 1
        elif  curr_symbol == "v":
            current_position_row += 1
        elif  curr_symbol == "<":
            current_position_col -= 1
        elif  curr_symbol == ">":
            current_position_col -= 1


# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

print("mapIndex")
