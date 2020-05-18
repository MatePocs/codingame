# ******************
# Naive solution
# ******************

import sys
import math

# basically, what's the largest difference if you subtract from left to right

# ok, this will definitely not work with high n, but let's do a naive one first

n = int(input())

values = []

for i in input().split():
    v = int(i)
    values.append(v)

max_diff = 0

for i in range(len(values)):
    buy_price = values[i]
    for j in range(i, len(values)):
        sell_price = values[j]
        difference = sell_price - buy_price
        max_diff = min(max_diff, difference)

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr)

print(max_diff)


"""
Well, this worked for all cases, except for the large database, will need to adjust for that
"""


# ******************
# Optimised Solution
# ******************
