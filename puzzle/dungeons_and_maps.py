import sys
import math

debug_mode = True

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



# well we need to check the maps one by one
def get_number_of_steps_to_treasure(map, mapid):

    number_of_steps = 1
    covered_position = set() # set of tuples, so we can keep track of points we already covered
    current_position_row = start_row
    current_position_col = start_col

    # TODO add a step to check if we have already been there 

    while True:

        # first, check if we are still inside the map
        if not(current_position_row in range(w)) or not(current_position_col in range(h)):
            if debug_mode:
                print("went out of bound",  file=sys.stderr, flush=True)
            number_of_steps = -1
            break

        current_coord = (current_position_row, current_position_col)

        if current_coord in covered_position:
            number_of_steps = -1
            break
        else:
            covered_position.add(current_coord)

        curr_symbol = map[current_position_row][current_position_col]

        if debug_mode: 
            print(f"current symbol: {curr_symbol}", file=sys.stderr, flush=True)

        # if we arrived at a T, then we can get out of the loop, and the map is valid
        if curr_symbol == "T":
            break
        
        # otherwise, we have to check if we arrived at a proper path value
        if curr_symbol == "^":
            current_position_row -= 1
        elif  curr_symbol == "v":
            current_position_row += 1
        elif  curr_symbol == "<":
            current_position_col -= 1
        elif  curr_symbol == ">":
            current_position_col += 1
        # if none of these, we can break, the map is invalid
        else:
            number_of_steps = -1
            break

        # if we are still here, that means we can continue
        number_of_steps += 1

    return number_of_steps

def get_map_with_least_number_of_steps(maps, mapsize):

    mapid_with_shortest_route = None
    minimum_steps = mapsize ** 2

    for mapid, map in enumerate(maps):
        current_number_of_steps = get_number_of_steps_to_treasure(map, mapid)

        if debug_mode:
            print(f"on mapid {mapid} the number of steps: {current_number_of_steps}", file=sys.stderr, flush=True)

        if current_number_of_steps < minimum_steps and current_number_of_steps > 0:
            mapid_with_shortest_route = mapid
            minimum_steps = current_number_of_steps

    if mapid_with_shortest_route is None:
        mapid_with_shortest_route = "TRAP"

    return mapid_with_shortest_route


mapid_with_shortest_route = get_map_with_least_number_of_steps(maps, n)


# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

print(mapid_with_shortest_route)
