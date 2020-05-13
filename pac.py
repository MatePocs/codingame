import sys
import math
from enum import Enum

# Grab the pellets as fast as you can!

# *************
# INITIAL DATA STEP
# *************

map_of_arena = []
# width: size of the grid
# height: top left corner is (x=0, y=0)
width, height = [int(i) for i in input().split()]
for i in range(height):
    row = input()  # one line of the grid: space " " is floor, pound "#" is wall

#map's first coordinate is y, second is x
map_of_arena.append(row)

# *************
# CLASSES
# *************

class Player(Enum):
    ME =1
    OPPONENT = 2

class CommandType(Enum):
    MOVE = 1

class CoOrdinate:
    """
    has two attributes, x and y, which are integers
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Pac:

    def __init__(self, pac_id, owner , coord, speed_turns_left, ability_cooldown):
        self.pac_id = pac_id
        self.owner = owner
        self.coord = coord
        self.speed_turns_left = speed_turns_left
        self.ability_cooldown = ability_cooldown

class Pellet:

    def __init__(self, coord, value):
        self.coord = coord
        self.value = value

class DistanceCalculator:
    """
    contains various code versions to calculate distance between two points
    """
    def __init__(self):
        pass

    def calculate_manhattan_distance(self, coord1, coord2):
        """
        inputs are CoOrdinate objects
        """
        return abs(coord1.x - coord2.x) + abs(coord1.y - coord2.y)

    def find_minimum_manhattan_distance_coordinates(self, coord, list_of_coords):
        """
        returns a list of coordinates, a subset of list_of_coords, that have
        minimum manhattan distance 
        also returns the minimum distance that we calculated
        """
        result_list = []
        current_minimum_distance = width + height

        for coord_to_check in list_of_coords:
            coord_to_check_distance = \
            self.calculate_manhattan_distance(coord, coord_to_check)
            if  coord_to_check_distance < current_minimum_distance:
                result_list = []
                result_list.append(coord_to_check)
                current_minimum_distance = coord_to_check_distance
            elif coord_to_check_distance == current_minimum_distance: 
                result_list.append(coord_to_check)

        return result_list, current_minimum_distance

    def extract_coordinates_of_pellets(self, pellets):
        pellet_coords = []
        for pellet in pellets:
            pellet_coords.append(pellet.coord)
        return pellet_coords

class Command():

    def __init__(self, cmd_type, source, target):
        self.type = cmd_type # Enum
        self.source = source # the id of pac
        self.target = target # a coordinate
        self.string_command = self.convert_to_string()

    def convert_to_string(self):
        if self.type == CommandType.MOVE:
            x = self.target.x
            y = self.target.y
            return 'MOVE ' + str(self.source) + ' ' + str(x) + ' ' + str(y)

class MultipleCommandsCombiner():
    """
    takes in list of string commands, combines them into one command that 
    can be used as final output for the round
    """

    def __init__(self):
        pass

    def combine_commands(self, multiple_string_commands) :
        result_string = ''
        for command in multiple_string_commands:
            result_string = result_string + command + ' | '

        # take out last | symbol

        result_string = result_string[:-2]
        return result_string

class Agent():
    """
    responsible for moving pacmans, only thing is: whose
    """

    def __init__(self, owner):
        self.owner = owner

    def respond(self, gamestate):
        """
        returns list of commands based on game state for next round in string format
        """

        # First Strategy: send pac to nearest pellet

        command_strings = []

        for pac in gamestate.my_pacs:

            pellet_coords = distance_calculator.extract_coordinates_of_pellets(gamestate.pellets)
            target = distance_calculator.find_minimum_manhattan_distance_coordinates(pac.coord, pellet_coords)[0][0]
            command = Command(cmd_type = CommandType.MOVE, source = pac.pac_id, target = target)

            command_string = command.convert_to_string()
            command_strings.append(command_string)

        return command_strings


class GameState():
    """
    collects pacs and pellets
    """

    def __init__(self, my_pacs, opponent_pacs, pellets):
        self.my_pacs = my_pacs
        self.opponent_pacs = opponent_pacs
        self.pellets = pellets


# *************
# ENVIRONMENT
# *************

distance_calculator = DistanceCalculator()
agent = Agent(owner = Player.ME)
multiple_commands_combiner = MultipleCommandsCombiner()


# *************
# GAME LOOP STARTS
# *************



while True:

# *************
# DATA
# *************

    my_score, opponent_score = [int(i) for i in input().split()]

    # DATA 1 - Setting up Pacs

    my_pacs = []
    opponent_pacs = []

    visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
    for i in range(visible_pac_count):
        # pac_id: pac number (unique within a team)
        # mine: true if this pac is yours
        # x: position in the grid
        # y: position in the grid
        # type_id: unused in wood leagues
        # speed_turns_left: unused in wood leagues
        # ability_cooldown: unused in wood leagues
        pac_id, mine, x, y, type_id, speed_turns_left, ability_cooldown = input().split()
        pac_id = int(pac_id)
        mine = mine != "0"
        x = int(x)
        y = int(y)
        speed_turns_left = int(speed_turns_left)
        ability_cooldown = int(ability_cooldown)

        if mine:
            owner = Player.ME
        else:
            owner = Player.OPPONENT

        coord = CoOrdinate(x, y)
        pac = Pac(pac_id, owner , coord, speed_turns_left, ability_cooldown)

        if mine:
            my_pacs.append(pac)
        else:
            opponent_pacs.append(pac)

    # DATA 2 - Setting up Pellets

    pellets = []

    visible_pellet_count = int(input())  # all pellets in sight
    for i in range(visible_pellet_count):
        # value: amount of points this pellet is worth
        x, y, value = [int(j) for j in input().split()]

        coord = CoOrdinate(x, y)
        pellet = Pellet(coord, value)

        pellets.append(pellet)

    gamestate = GameState(my_pacs = my_pacs, opponent_pacs = opponent_pacs, pellets = pellets)

# *************
# STRATEGY
# *************

    commands = agent.respond(gamestate)
    print(commands, file = sys.stderr)
    commands_string = multiple_commands_combiner.combine_commands(commands)


    # MOVE <pacId> <x> <y>
    print(commands_string)
