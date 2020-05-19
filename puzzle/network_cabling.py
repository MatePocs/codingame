import sys
import math
import numpy as np

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# we do not actually need to keep track of x positions of houses, just minimum and maximum y

min_x = (2**30)
max_x = -(2**30)



n = int(input())
y_coord = np.zeros(n)
for i in range(n):
    x, y = [int(j) for j in input().split()]

    min_x = min(x, min_x)
    max_x = max(x, max_x)

    y_coord[i]=y

chosen_y_coord = np.median(y_coord)

distances_from_cable = np.abs(y_coord - chosen_y_coord).sum()

length = int(max_x- min_x + distances_from_cable)


print(length)
