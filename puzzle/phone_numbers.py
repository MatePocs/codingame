import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

telephone_numbers = []

n = int(input())
for i in range(n):
    telephone = input()
    telephone_numbers.append(telephone)

number_of_elements = 0
number_of_elements += len(telephone_numbers[0])

def is_number_sequence_in_list(number_sequence, list_of_numbers):
    """
    checks if there are any elements in the list_of_numbers that
    start with the number_sequence
    """
    print(number_sequence, file = sys.stderr)
    print(list_of_numbers, file = sys.stderr)
    match = False
    length_of_sequence = len(number_sequence)
    for i in range(len(list_of_numbers)):
        if list_of_numbers[i][:length_of_sequence] == number_sequence:
            print(list_of_numbers[i][:length_of_sequence], file = sys.stderr)
            match = True
            break   
    return match


for i in range(1, len(telephone_numbers)):
    current_number = telephone_numbers[i]
    # for each length, check if there is another phone number already in the list 
    # that starts with that sequence
    # at the first length where we find no number: we need to store the rest
    numer_of_characters_with_no_match = 0
    for j in range(0, len(current_number)):
        if is_number_sequence_in_list(current_number[:j+1],telephone_numbers[:i]):
            pass
        else:
            numer_of_characters_with_no_match = len(current_number) - j
            break
    number_of_elements += numer_of_characters_with_no_match

# The number of elements (referencing a number) stored in the structure.
print(number_of_elements)
