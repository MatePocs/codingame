import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


def sign1_beats_sign2(sign1, sign2):
    result = False
    if sign1 == 'R':
        if sign2 == 'L' or sign2 == 'C':
            result = True
    elif sign1 == 'P':
        if sign2 == 'R' or sign2 == 'S':
            result = True
    elif sign1 == 'C':
        if sign2 == 'P' or sign2 == 'L':
            result = True
    elif sign1 == 'L':
        if sign2 == 'S' or sign2 == 'P':
            result = True
    elif sign1 == 'S':
        if sign2 == 'C' or sign2 == 'R':
            result = True

    return result

players_num = []
players_sign = {}

players_matchhistory = {}

n = int(input())
for i in range(n):
    numplayer, signplayer = input().split()
    numplayer = int(numplayer)
    players_num.append(numplayer)
    players_sign[numplayer] = signplayer
    players_matchhistory[numplayer] = ''

number_of_rounds = int(math.log2(n))

for i in range(number_of_rounds):
    players_nextround = []
    for j in range(int(len(players_num)/2 )):
        index_1 = j * 2
        index_2 = index_1 + 1
        num_1 = players_num[index_1]
        num_2 = players_num[index_2]
        sign_1 = players_sign[num_1]
        sign_2 = players_sign[num_2]
        players_matchhistory[num_1] = players_matchhistory[num_1] + str(num_2) + ' '
        players_matchhistory[num_2] = players_matchhistory[num_2] + str(num_1) + ' '
        if sign1_beats_sign2(sign_1, sign_2):
            players_nextround.append(num_1)
        elif sign1_beats_sign2(sign_2, sign_1):
            players_nextround.append(num_2)
        elif num_1 < num_2:
            players_nextround.append(num_1)
        else:
            players_nextround.append(num_2)

    players_num = players_nextround.copy()

winner = players_num[0]
#players_matchhistory[winner] = players_matchhistory[winner][0:len(players_matchhistory[winner]-1)]

print(winner)
print(players_matchhistory[winner][0:-1])