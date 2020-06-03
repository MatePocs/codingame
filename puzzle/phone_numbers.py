import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

class Node:
    """
    an object that has one job: keeping track of its children
    """

    def __init__(self):
        self.children = {}
        # children are a dictionary, key is an integer, value is a node

    def add_child(self, key_of_child):
        """
        adds child to the dictionary of children
        """
        self.children[key_of_child] = Node()

    def add_children(self, key_of_child_list):
        """
        adds children in a tree format
        list is number of integers, goes deeper and deeper
        """
        current_node = self
        for i in range(len(key_of_child_list)):
            current_node.add_child(key_of_child_list[i])
            current_node = current_node.children[key_of_child_list[i]]

class PhoneBook:
    """
    main class, this will contain all the information
    phone numbers as a tree and number of elements stored
    """

    def __init__(self):
        self.number_of_elements = 0
        self.phone_numbers = {}
        # phone numbers are going to be a dictionary, key: integer, value: a node

    def process_new_number(self, phone_number):
        """
        adds phone number to somewhere in the PhoneBook tree
        phone_number is a string
        """

        numbers_list = self.convert_string_to_list_of_numbers(phone_number)

        #check if first is in phone_numbers
        if numbers_list[0] in self.phone_numbers:
            # if yes, go in and search
            current_node = self.phone_numbers[numbers_list[0]]
            for i in range(1, len(numbers_list)):
                # check if we can go one level deeper
                if numbers_list[i] in current_node.children:
                    # if it is in the current_node, great, move on
                    current_node = current_node.children[numbers_list[i]]
                    i += 1
                else:
                    # if not in the current node, need to add the remainder of 
                    # the list to the current node
                    current_node.add_children(numbers_list[i:])
                    break

            # and we know the number of new elements
            new_elements = len(numbers_list) - i

        else:
            # if not, adds the first one, and then adds all the children
            self.phone_numbers[numbers_list[0]] = Node()
            self.phone_numbers[numbers_list[0]].add_children(numbers_list[1:])

            new_elements = len(numbers_list)

        # adds the number of new items stored to the number_of_elements
        self.number_of_elements += new_elements

    def convert_string_to_list_of_numbers(self, phone_number):
        """
        takes in a string, returns a list of integers
        """
        result_list = []

        for char in phone_number:
            result_list.append(int(char))

        return result_list







phonebook = PhoneBook()

n = int(input())
for i in range(n):
    telephone = input()
    phonebook.process_new_number(telephone)




# The number of elements (referencing a number) stored in the structure.
print(phonebook.number_of_elements)
