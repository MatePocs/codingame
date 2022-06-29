import sys
import math

n = int(input())
lines = []
for i in range(n):
    line = input()
    lines.append(line)

def get_result_of_line(line):

    current_stack_heads = []

    for i, char in enumerate(line):

        # always going left to right, putting it in the first place we can
        
        placed_on_top_of_stack = False

        for j, stack_head_char in enumerate(current_stack_heads):
            if char <= stack_head_char:
                placed_on_top_of_stack = True
                current_stack_heads[j] = char
                break

        if not(placed_on_top_of_stack):
            current_stack_heads.append(char)

    return len(current_stack_heads)

for i in range(n):
    result = get_result_of_line(lines[i])
    print(result)
