import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

numerals = []
# it's going to be a list of h elements
# each element is a string, length is 20*l, rows of numerals

number_1_code = []
number_2_code = []
# similar structure, list of h element, but each of these is only
# l length

l, h = [int(i) for i in input().split()]
for i in range(h):
    numeral = input()
    numerals.append(numeral)
s1 = int(input())
for i in range(s1):
    num_1line = input()
    number_1_code.append(num_1line)
s2 = int(input())
for i in range(s2):
    num_2line = input()
    number_2_code.append(num_2line)
operation = input()

def does_number_code_match(number_code, number):
    """
    checks if a number_code matches a specific number in the numerals
    """
    match = True
    for i in range(h):
        if number_code[i] != numerals[i][number * l: (number+1) * l]:
            match = False
            break

    return match

def find_number(number_code):
    """
    takes in number in string format
    list of h elements, each element is a string
    length is l
    loops through 20 elements of numerals, checks if all the lines match
    """
    number = 0
    for i in range(20):
        if does_number_code_match(number_code, i):
            number = i
            break
    return number

number_1 = find_number(number_1_code)
number_2 = find_number(number_2_code)

print(str(number_1), file = sys.stderr)
print(operation, file = sys.stderr)
print(str(number_2), file = sys.stderr)

def calculate_result_number(number_1, number_2, operation):
    if operation == '+':
        result = number_1 + number_2
    elif operation == '-':
        result = number_1 - number_2
    elif operation == '*':
        result = number_1 * number_2
    elif operation == '/':
        result = number_1 / number_2

    return result

number_result = calculate_result_number(number_1, number_2, operation)

def convert_number_to_base_20(number):
    """
    converts the number to 20-system
    returns list of numbers, first is the factor with highest power of 20
    """

    result = []
    current_residual = number
    highest_power = round(math.log(number, 20)) // 1

    for i in range(highest_power, -1, -1):
        current_factor = int((current_residual / 20 ** i) // 1)
        current_residual = current_residual - current_factor * 20 ** i
        result.append(current_factor)

    return result

number_result_in_base_20 = convert_number_to_base_20(number_result)
print(str(number_result_in_base_20), file = sys.stderr)

def print_20_number(number):
    """
    prints out all the rows of a number
    """
    for i in range(h):
        print(numerals[i][number * l: (number+1) * l])


def print_20_number_list(list_of_numbers):
    """
    takes a list of integers
    starting from the first one, prints it on the screen
    """
    for i in range(len(list_of_numbers)):
        print_20_number(list_of_numbers[i])


print_20_number_list(number_result_in_base_20)
