import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

width_area_lengths = []
height_area_lengths = []

w, h, count_x, count_y = [int(i) for i in input().split()]

# populate width measurements
curr_width_area_sum = 0
for i in input().split():
    x = int(i)
    width_area_lengths.append(x - curr_width_area_sum)
    curr_width_area_sum = x
# as a last step, also add the remaining bit
width_area_lengths.append(w - sum(width_area_lengths))

print(width_area_lengths, file=sys.stderr, flush=True)

# well this is annoying
# so the measurements should also include any potential sums
# e.g. if we have a measurement 2 and 3 next to each other, we also have a 5
combination_width_area_lengths = []
for i in range(len(width_area_lengths)):
    for j in range(i+1,len(width_area_lengths)):
        print(f"i: {i}, j: {j}, sum: {sum(width_area_lengths[i:j+1])}", file=sys.stderr, flush=True)
        combination_width_area_lengths.append(sum(width_area_lengths[i:j+1]))

width_area_lengths.extend(combination_width_area_lengths)

print(width_area_lengths, file=sys.stderr, flush=True)



# same logic with height measurements
curr_height_area_sum = 0
for i in input().split():
    x = int(i)
    height_area_lengths.append(x - curr_height_area_sum)
    curr_height_area_sum = x
height_area_lengths.append(h - sum(height_area_lengths))

print(height_area_lengths, file=sys.stderr, flush=True)

combination_height_area_lengths = []
for i in range(len(height_area_lengths)):
    for j in range(i+1,len(height_area_lengths)):
        print(f"i: {i}, j: {j}, sum: {sum(height_area_lengths[i:j+1])}", file=sys.stderr, flush=True)
        combination_height_area_lengths.append(sum(height_area_lengths[i:j+1]))

height_area_lengths.extend(combination_height_area_lengths)

print(height_area_lengths, file=sys.stderr, flush=True)


# now loop over bost measurements, collect the number of such measurements in a dictionary
# dictionary key: measurement length, value: list with two elements, first is number it appears in width list, second is number it appears in height list

count_dict = {}

for are_length in width_area_lengths:

    if are_length in count_dict:
        count_dict[are_length][0] += 1
    else:
        count_dict[are_length] = [1,0]

for are_length in height_area_lengths:

    if are_length in count_dict:
        count_dict[are_length][1] += 1
    else:
        # note we don't really need this for the task, but it would annoy me not to have this path
        count_dict[are_length] = [0,1]

number_of_squares = 0

for number_of_cuts in count_dict.values():

    number_of_squares += number_of_cuts[0] * number_of_cuts[1]


# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

print(number_of_squares)
