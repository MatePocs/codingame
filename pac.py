import sys
import math
from enum import Enum

debugging = True

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
        self.label = str(x) + ',' + str(y)

class MyMap:
    """
    used to store the floor type coordinates
    created from the distancecalculator object
    """

    def __init__(self, map_of_arena):
        """
        map_of_arena is the input we get from the game system
        a list of lists, containing '#' for wall and ' ' for floor
        """
        # this map is seldom used
        self.map_of_arena = map_of_arena

        self.populate_floor_coordinates()
        
    def populate_floor_coordinates(self):
        """
        creates dictionary, where keys are coordinate labels, values are coordinates
        """
        self.floor_coordinates = {}

        for rownum, row in enumerate(self.map_of_arena):
            for columnum, item in enumerate(row):
                if item == ' ':
                    # the item is a valid coord, add it to the dictionary
                    current_coord = CoOrdinate(x = columnum, y = rownum)
                    self.floor_coordinates[current_coord.label] = current_coord


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

    @staticmethod
    def extract_coordinates_of_pellets(pellets):
        """
        returns the coordinates as labels
        """
        pellet_coords = []
        for pellet in pellets:
            pellet_coords.append(pellet.coord.label)
        return pellet_coords

class DistanceCalculator:
    """
    contains various methods to calculate distance between two points
    throughout this class, coord is used as the tuple label, the key in 
    my_map.floor_coordinates
    if we need the actual coordinates, we use the dictionary to convert to 
    a coordinate object
    """
    def __init__(self, map_of_arena):
        self.map_of_arena = map_of_arena

        # first step: create a map object
        # this will keep track of available floor corrdinates
        self.my_map = MyMap(map_of_arena)

        self.shortest_distances_between_coords = {}
        # example: shortest_distance_between_coords[('3,1','11,8'): [8, routes]]
        # where routes is : [route1, route2,..]
        # where route is : ['3,1', ..., '11,8']

        self.closest_coordinates = {}
        # example: closedt_coordinates[('3,1', 8)]: routes
        # where routes are efficient 8-distance routes starting from '3,1'

        # then, we populate two dictionaries, the shortest_distance_between_coords
        # and the closest_coordinates
        self.calculate_shortest_distances()

    def find_minimum_distance_coordinates(self, start_coord, list_of_end_coords):
        """
        takes a coord and a list of coords, both labels
        returns a sublist of list_of_coords that are of minimum distance and the min distance
        """
        result_list = []
        current_minimum_distance = 99999
        
        for end_coord in list_of_end_coords:
            current_distance = self.shortest_distances_between_coords[(start_coord, end_coord)][0]
            if current_distance < current_minimum_distance:
                result_list = []
                result_list.append(end_coord)
                current_minimum_distance = current_distance
            elif current_distance == current_minimum_distance:
                result_list.append(end_coord)

        return current_minimum_distance, result_list


    def calculate_shortest_distances(self):
        """
        populate the two route dictionaries
        """

        # first step: calculate 0-distance routes
        self.populate_0_coords()

        # now we have the coordinates, add more step by step

        found_at_least_one_new_route = True
        distance = 0

        while found_at_least_one_new_route:
            print(distance, file = sys.stderr)
            found_at_least_one_new_route = False
            distance += 1
            found_at_least_one_new_route = self.populate_distance_coords(distance = distance)
        

    def populate_0_coords(self):
        """
        sets up the shortest distance calculations by populating the 0-distance routes
        """

        for coord in self.my_map.floor_coordinates:
            current_route = []
            current_route.append([coord])

            self.shortest_distances_between_coords[(coord, coord)] = \
                (0, current_route)
            self.closest_coordinates[(coord, 0)] = current_route

    def populate_distance_coords(self, distance):
        """
        assuming we have everything mapped up until distance - 1, 
        updates shortest_distances_between_coords and closest_coordinates  
        returns if we found at least one new route for this distance
        """

        found_at_least_one_new_route = False

        # loop through floor coordinates
        for coord in self.my_map.floor_coordinates:
            shorter_routes = self.closest_coordinates.get((coord, distance - 1), None)
            if shorter_routes is not None:
                # there is a list of routes with a distance -1
                for shorter_route in shorter_routes:
                    end_coord = shorter_route[-1]
                    # check if we can move in any of the four directions from end_coord
                    valid_neighbors = self.collect_valid_neighbors(end_coord)
                    # from these potential next steps, only take the ones that are not already
                    # in the shorter route (loops will never be efficient)
                    next_steps = []
                    for valid_neighbor in valid_neighbors:
                        if valid_neighbor not in shorter_route:
                            next_steps.append(valid_neighbor)

                    # now we have to check all the valid neighbors and add them to the relevant 
                    # dictionaries
                    for next_step in next_steps:
                        current_route = shorter_route.copy()
                        current_route.append(next_step)

                        # now we have a possible route, current route, see if it should be added
                        # to the dictionaries

                        new_route_added = \
                        self.potentially_add_current_route(current_route)
                        if new_route_added: found_at_least_one_new_route = True

        return found_at_least_one_new_route

    def potentially_add_current_route(self, current_route):
        """
        check if current_route should be added to the relevant dictionaries
        returns boolean that tells if route was added
        """
        new_route_added = False

        start_coord = current_route[0]
        end_coord = current_route[-1]
        distance = len(current_route) - 1

        # first, check shortest_distances_between_coords
        # there might already be other routes of equal distance in start_coord, end_coord
        currently_known_min_distance, currently_known_min_distance_routes = \
        self.shortest_distances_between_coords.get((start_coord, end_coord), (None, None))

        currently_known_routes_from_the_same_start_coord = \
        self.closest_coordinates.get((start_coord,distance), [])

        # three possible cases:
        
        # case 1 - if we are unaware of a shortest distance between 
        # the two coords, add the current one 
        if currently_known_min_distance is None:

            self.shortest_distances_between_coords[(start_coord, end_coord)] = \
            (distance, [current_route])

            currently_known_routes_from_the_same_start_coord.append(current_route)

            self.closest_coordinates[(start_coord, distance)] = currently_known_routes_from_the_same_start_coord

            new_route_added = True

        # case 2 - if we already have another route between the two points with the same distance
        # we append the current route to the shortest routes between the two coord
        # and we append the current route to the routes starting from the start coord
        elif currently_known_min_distance == distance:

            currently_known_min_distance_routes.append(current_route)
            currently_known_routes_from_the_same_start_coord.append(current_route)

            self.shortest_distances_between_coords[(start_coord, end_coord)] = \
            (distance, currently_known_min_distance_routes)

            self.closest_coordinates[(start_coord,distance)] = currently_known_routes_from_the_same_start_coord

            new_route_added = True

        # case 3: because we are populating this by increased distances, this can 
        # only mean that we found a route that is longer than the shortest
        # a loop
        # not doing anything for now, might need it later
        else: 
            pass

        return new_route_added

    def collect_valid_neighbors(self, coord_label):
        """
        takes a coord, returns a list of other coords that are neighboring
        list is 0-4 length
        in this function, coord_label is the tuple, coord is the CoOrdinate object
        """

        coord_input = self.my_map.floor_coordinates[coord_label]

        neighbor_coord_labels = []
        x = coord_input.x
        y = coord_input.y

        up_coord = CoOrdinate(x, y-1)
        down_coord = CoOrdinate(x, y + 1)
        if x == 0: 
            left_x = width - 1
        else:
            left_x = x -1
        left_coord = CoOrdinate(left_x, y)
        if x == width - 1:
            right_x = 0
        else:
            right_x = x + 1
        right_coord = CoOrdinate(right_x, y)

        for coord in [up_coord, down_coord, right_coord, left_coord]:
            if coord.label in self.my_map.floor_coordinates:
                neighbor_coord_labels.append(coord.label)

        return neighbor_coord_labels


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

        return urrent_minimum_distance, result_list


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

        command_strings = []

        # for now, loop through pacmans, send them to nearest pellet
        # TODO speed up if they are not sped up
        for pac in gamestate.my_pacs:

            pac_coord = pac.coord.label
            pellet_coords = Pellet.extract_coordinates_of_pellets(gamestate.pellets)
            target_label = distance_calculator.find_minimum_distance_coordinates(pac_coord, pellet_coords)[0][0]
            target = distance_calculator.my_map.floor_coordinates[target_label]

            command = Command(cmd_type = CommandType.MOVE, source = pac.pac_id, target = target)

            command_string = command.convert_to_string()
            command_strings.append(command_string)

        return command_strings

    def greedy_manhattan():
        """
        old code, not used anymore, sends each pacman to nearest manhattan pellet
        """
        for pac in gamestate.my_pacs:

            pellet_coords = Pellet.extract_coordinates_of_pellets(gamestate.pellets)
            target = distance_calculator.find_minimum_manhattan_distance_coordinates(pac.coord, pellet_coords)[0][0]

            command = Command(cmd_type = CommandType.MOVE, source = pac.pac_id, target = target)

            command_string = command.convert_to_string()
            command_strings.append(command_string)


class GameState():
    """
    collects pacs and pellets
    """

    def __init__(self, my_pacs, opponent_pacs, pellets, my_score, opponent_score):
        self.my_pacs = my_pacs
        self.opponent_pacs = opponent_pacs
        self.pellets = pellets
        self.my_score = my_score
        self.opponent_score = opponent_score

class GameStateProjector():
    """
    class that projects gamestates
    """
    def __init__(self):
        pass

    def project_one_step(self, current_gamestate, commands):
        """
        current_gamestate: GameState object
        commands: list of Command objects
        takes current_gamestate and commands
        simulates a turn
        returns the projected gamestate
        this should be an accurate projection in all cases, except for when
        opponent pac comes outside of our vision
        """
        current_mypacs = current_gamestate.my_pacs
        current_opponentpacs = current_gamestate.opponent_pacs



        projected_gamestate = GameState()
        return projected_gamestate


# *************
# ENVIRONMENT
# *************


distance_calculator = DistanceCalculator(map_of_arena)
agent = Agent(owner = Player.ME)
multiple_commands_combiner = MultipleCommandsCombiner()
gamestate_projector = GameStateProjector()

print(distance_calculator.closest_coordinates[('11,10', 2)], file = sys.stderr)

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

    gamestate = GameState(
        my_pacs = my_pacs, opponent_pacs = opponent_pacs, pellets = pellets, \
        my_score = my_score, opponent_score = opponent_score)

# *************
# STRATEGY
# *************

    commands = agent.respond(gamestate)
    commands_string = multiple_commands_combiner.combine_commands(commands)


    # MOVE <pacId> <x> <y>
    print(commands_string)
