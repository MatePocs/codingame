import sys
import math
from collections import defaultdict


table = []
w = int(input())
h = int(input())
for i in range(h):
    line = input()
    table.append(line)

neighbour_mine_counts = defaultdict(int)
mine_locations = set()


for i in range(h):
    for j in range(w):
        if table[i][j] == "x":
            # first of all, add it to the mine locations
            mine_locations.add((i,j))
            # then, increase corresponding counters
            # note: won't really care about checking borders, we will just have items in neighbour_mine_counts that we don't use
            neighbour_mine_counts[(i-1, j)] += 1
            neighbour_mine_counts[(i-1, j-1)] += 1
            neighbour_mine_counts[(i-1, j+1)] += 1
            neighbour_mine_counts[(i, j-1)] += 1
            neighbour_mine_counts[(i, j+1)] += 1
            neighbour_mine_counts[(i+1, j)] += 1
            neighbour_mine_counts[(i+1, j-1)] += 1
            neighbour_mine_counts[(i+1, j+1)] += 1


# and now, populate the final table
result_table = [["." for _ in range(w)] for _ in range(h)]

# first with counters
for i in range(h):
    for j in range(w):
        if neighbour_mine_counts[(i,j)] > 0:
            result_table[i][j] = neighbour_mine_counts[(i,j)]

# then put in mine locations - those are always empty
for mine_location in mine_locations:
    result_table[mine_location[0]][mine_location[1]] = "."


for i in range(h):
    current_line = result_table[i]
    current_line_string = [str(i) for i in current_line]
    print(''.join(current_line_string))
