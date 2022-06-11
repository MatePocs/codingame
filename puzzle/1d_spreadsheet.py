import sys
import math


debug_mode = True

# To debug: print("Debug messages...", file=sys.stderr, flush=True)

# collect input information
n = int(input())
operations = []
arg_1_values = []
arg_1_is_reference = []
arg_2_values = []
arg_2_is_reference = []
references = [set() for _ in range(n)]
for i in range(n):
    operation, arg_1, arg_2 = input().split()
    operations.append(operation)
    if arg_1[0] == "$":
        arg_1_values.append(int(arg_1[1:]))
        arg_1_is_reference.append(True)
        references[i].add(int(arg_1[1:]))
    else:
        arg_1_values.append(int(arg_1))
        arg_1_is_reference.append(False)
    if arg_2[0] == "$":
        arg_2_values.append(int(arg_2[1:]))
        arg_2_is_reference.append(True)
        references[i].add(int(arg_2[1:]))
    else:
        if arg_2 == "_": arg_2 = 0 
        arg_2_values.append(int(arg_2))
        arg_2_is_reference.append(False)

"""
print(operations, file=sys.stderr, flush=True)
print(arg_1_values, file=sys.stderr, flush=True)
print(arg_1_is_reference, file=sys.stderr, flush=True)
print(arg_2_values, file=sys.stderr, flush=True)
print(arg_2_is_reference, file=sys.stderr, flush=True)
"""

# collect results
result = [0] * n
uncalculated_cells = set(range(n))

def calculate_operation_result(curr_operation, curr_arg_1, curr_arg_2):
    curr_result = 0
    if curr_operation == "VALUE":
        curr_result = curr_arg_1
    elif curr_operation == "ADD":
        curr_result = curr_arg_1 + curr_arg_2
    elif curr_operation == "SUB":
        curr_result = curr_arg_1 - curr_arg_2
    elif curr_operation == "MULT":
        curr_result = curr_arg_1 * curr_arg_2
    return(curr_result)

# first loop: calculate ones that have no references
for i in range(n):
    # these are the ones that can simply be calculated
    if len(references[i]) == 0:
        curr_result = calculate_operation_result(
            operations[i], arg_1_values[i], arg_2_values[i])
        result[i] = curr_result
        uncalculated_cells.remove(i)
        print(f"handled cell: {i}, value: {curr_result}", file=sys.stderr, flush=True)

# now, loop in uncalculated cells until we find one 
# where the reference set is not in uncalc
# prob very inefficient

while len(uncalculated_cells) > 0:
    for cell in uncalculated_cells:
        # check if references have any overlap with the uncalculated_cells
        if len(uncalculated_cells.intersection(references[cell])) == 0:
            # if no intersection, all the references are calculated
            if arg_1_is_reference[cell]:
                curr_arg_1 = result[arg_1_values[cell]]
            else:
                curr_arg_1 = arg_1_values[cell]
            if arg_2_is_reference[cell]:
                curr_arg_2 = result[arg_2_values[cell]]
            else:
                curr_arg_2 = arg_2_values[cell]
            curr_result = calculate_operation_result(operations[cell], curr_arg_1, curr_arg_2)
            result[cell] = curr_result
            uncalculated_cells.remove(cell)
            print(f"cell: {cell}, value: {curr_result}, arg_1: {curr_arg_1},arg_2: {curr_arg_2}", 
                file=sys.stderr, flush=True)
            break

for i in range(n):

    print(result[i])
