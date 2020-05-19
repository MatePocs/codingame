import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())
budgets = {}
c = int(input())
for i in range(n):
    b = int(input())
    budgets[i] = b

#budgets_sorted = sorted(budgets.items(), key = lambda x: x[1])

def current_budget_reached(index):
    return budgets[index] == result[index]

def increase(index):
    if index == n - 1:
        index = 0
    else:
        index +=1
    return index


def decrease(index):
    if index == 0:
        index = n-1
    else:
        index -=1
    return index

print('INPUT: ', file = sys.stderr)
print(c, budgets, file = sys.stderr)
print('\n', file = sys.stderr)

if sum(budgets.values()) < c:
    result = "IMPOSSIBLE"
else:
    result = [0] * n
    next_to_fill = n-1
    for i in range(c):
        #print(i, file = sys.stderr)
        # check if current budget is OK, increase next_to_fill until it is
        while current_budget_reached(next_to_fill):
            next_to_fill = decrease(next_to_fill)
        #print(next_to_fill, file = sys.stderr)
        result[next_to_fill] += 1
        next_to_fill = decrease(next_to_fill)


if result == "IMPOSSIBLE":        
    print(result)
else:
    for result_line in sorted(result):
        print(result_line)
