import sys
import math

def character_value(character):
    """
    Returns the value of the character
    """
    if character in ['e', 'a', 'i', 'o', 'n', 'r', 't', 'l', 's', 'u']:
        value = 1
    elif character in ['d','g']:
        value = 2
    elif character in ['b', 'c', 'm', 'p']:
        value = 3
    elif character in ['f', 'h', 'v', 'w', 'y']:
        value = 4
    elif character in ['k']:
        value = 5
    elif character in ['j', 'x']:
        value = 8
    elif character in ['q', 'z']:
        value = 10

    return value

def word_value(word):
    """
    Returns the value of the word
    """
    total_value = 0
    for character in word:
        value = character_value(character)
        total_value += value

    return total_value

def convert_string_to_char_dict(word):
    """
    Converts string to dictionary in which
    keys are characters, values are frequencies
    """
    output_dict  = {}
    for character in word:
        current_freq = output_dict.get(character, 0)
        output_dict[character] = current_freq + 1
    return output_dict

def is_word_doable(word_char_freq, letters_freq):
    doable = True
    for char in word_char_freq:
        if word_char_freq[char] > letters_freq.get(char,0):
            doable = False
            break
    return doable

words = []

n = int(input())
for i in range(n):
    w = input()
    print(w, file = sys.stderr)
    words.append(w)
letters = input()

letters_freq = convert_string_to_char_dict(letters)

current_max_score = 0
current_best_word = ''

for word in words: 
    word_char_freq = convert_string_to_char_dict(word)
    if is_word_doable(word_char_freq, letters_freq):
        current_score = word_value(word)
        if current_score > current_max_score:
            current_max_score = current_score
            current_best_word = word

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr)

print(current_best_word)
