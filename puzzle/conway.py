import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

r = int(input())
l = int(input())

r = str(r)

def create_next_conway(input_number):
    """
    input string is converted to the next step
    """
    numbers_list = input_number.split(' ')
    output_string = ''

    currently_counted_number = numbers_list[0]
    current_count = 0
    for i in range(len(numbers_list)):
        current_number = numbers_list[i]
        if current_number == currently_counted_number:
            current_count += 1
        else:
            output_string = output_string + str(current_count) + ' ' + currently_counted_number + ' '
            currently_counted_number = current_number
            current_count = 1

    #and one last time
    output_string = output_string + str(current_count) + ' ' + currently_counted_number

    return output_string

for i in range(l-1):
    r = create_next_conway(r)

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr)

print(r)

