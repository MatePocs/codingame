import sys
import math

# GLOBAL VARIABLES

debugging_mode = True

archer_price = 100
knight_price = 80
max_distance = (1920 ** 2 + 1000 ** 2) ** 0.5
# to be used for minimum distance calculations


# **************
# 01 - CLASSES
# **************

class Site:
    """
    one site on the map
    """

    def __init__(self, site_id, x, y, radius):
        # the rest of the parameters will come in in the first update phase
        self.site_id = site_id
        self.x = x
        self.y = y
        self.radius = radius

    def update(self, structure_type = None, owner = None, param_1 = None, param_2 = None):
        if structure_type is not None:
            self.structure_type = structure_type
        if owner is not None:
            self.owner = owner
        if param_1 is not None:
            self.param_1 = param_1
        if param_2 is not None:
            self.param_2 = param_2

    @staticmethod
    def split_sites_by_owner(sites):
        """
        takes in sites dictionary containing all the sites
        returns three dictionaries, my_sites, neutral_sites, and opponent_sites
        we are also splitting my_sites to types
        """
        my_sites = {}
        my_knight_barracks = {}
        my_archer_barracks = {}
        neutral_sites = {}
        opponent_sites = {}
        opponent_knight_barracks = {}
        opponent_archer_barracks = {}

        for site_id in sites:
            site = sites[site_id]
            if site.owner == 0:
                my_sites[site_id] = site
                if site.structure_type == 2:
                    if site.param_2 == 0:
                        my_knight_barracks[site_id] = site
                    elif site.param_2 == 1:
                        my_archer_barracks[site_id] = site
            elif site.owner == 1:
                opponent_sites[site_id] = site
                if site.structure_type == 2:
                    if site.param_2 == 0:
                        opponent_knight_barracks[site_id] = site
                    elif site.param_2 == 1:
                        opponent_archer_barracks[site_id] = site
            elif site.owner == -1:
                neutral_sites[site_id] = site

        return my_sites, my_knight_barracks, my_archer_barracks, neutral_sites, \
        opponent_sites, opponent_knight_barracks, opponent_archer_barracks

    @staticmethod
    def calculate_distance(object1, object2):
        """
        calculates the distance between two objects (straight line) that both need to have x and y attributes
        """

        return  ((object1.x - object2.x) ** 2 + (object1.y - object2.y) ** 2) ** 0.5


class Unit:
    """
    contains information about the unit
    """

    def __init__(self):
        self.touched_site = -1

    def update(self, x, y, owner, unit_type, health):
        self.x = x
        self.y = y
        self.health = health
        self.owner = owner
        self.unit_type = unit_type

    @staticmethod
    def split_units_by_owner_and_type(units):
        """
        takes a list of units, and sorts them into four lists
        """
        my_knights = []
        my_archers = [] 
        opponent_knights = []
        opponent_archers = []

        for unit in units:
            if unit.owner == 0:
                if unit.unit_type == 0:
                    my_knights.append(unit)
                elif unit.unit_type == 1:
                    my_archers.append(unit)
            elif unit.owner == 1:
                if unit.unit_type == 0:
                    opponent_knights.append(unit)
                elif unit.unit_type == 1:
                    opponent_archers.append(unit)

        return my_knights, my_archers, opponent_knights, opponent_archers

        

class GameState:
    """
    only purpose is to group the data
    """

    def __init__(
        self, my_sites, my_knight_barracks, my_archer_barracks, neutral_sites, \
        opponent_sites, opponent_knight_barracks, opponent_archer_barracks, \
        my_queen, opponent_queen, \
        my_knights, my_archers, opponent_knights, opponent_archers, gold):
        self.my_sites = my_sites
        self.my_knight_barracks = my_knight_barracks
        self.my_archer_barracks = my_archer_barracks
        self.neutral_sites = neutral_sites
        self.opponent_sites = opponent_sites
        self.opponent_knight_barracks = opponent_knight_barracks
        self.opponent_archer_barracks = opponent_archer_barracks
        self.my_queen = my_queen
        self.opponent_queen = opponent_queen
        self.my_knights = my_knights 
        self.my_archers = my_archers 
        self.opponent_knights = opponent_knights 
        self.opponent_archers = opponent_archers

        self.gold = gold

    # TODO also calculate things like my_knight_barracks, my_archer_barracks in the future


class Agent:
    """
    our agent that determines our steps for the round
    """
    def __init__(self):
        self.game_turn = 0

    def increase_game_turn(self):
        self.game_turn += 1

    def determine_move(self,game_state):
        """
        returns a list of two strings, first: queen command, second: train command
        """
        commands = []
        queen_move = self.determine_queen_move(game_state)
        commands.append(queen_move)
        train_move = self.determine_train_move(game_state)
        commands.append(train_move)
        return commands

    def determine_queen_move(self, game_state):
        """
        returns one string, command for the queen
        """


        # first of all: if situation is bad, run with queen
        if self.should_queen_escape(game_state):
            command = self.determine_escape_move(game_state)
        else:
            command = self.determine_expansion_move(game_state)

        return command

    def should_queen_escape(self, game_state):
        """
        determines if we should push for expansion or escape with queen
        """

        # for now: escape if queen's health is below 40

        should_escape = False

        if game_state.my_queen.health < 40:
            should_escape = True

        return should_escape

    def determine_escape_move(self, game_state):
        """
        determines where the queen should escape
        """

        # for now, we check opponent queen, and move in opposite corner
        if game_state.opponent_queen.x > 1920 / 2: 
            destination_x = 0
        else:
            destination_x = 1920
        if game_state.opponent_queen.y > 1000 / 2: 
            destination_y = 0
        else:
            destination_y = 1000

        command = "MOVE " + str(destination_x) + " " + str(destination_y)

        return command

    def determine_expansion_move(self, game_state):
        """
        determines where the queen should move to build new buildings
        """
        # check if queen is touching a neutral site
        if game_state.my_queen.touched_site != -1 and game_state.my_queen.touched_site in game_state.neutral_sites:
        # if yes: build there
            command = self.build_at_queen_location(game_state)
        else:
        # if not: select the neutral site that is nearest to queen
            closest_site = self.get_closest_site_to_queen(game_state.neutral_sites, game_state.my_queen)
            command = "MOVE " + str(closest_site.x) + " " + str(closest_site.y)

        return command


    def build_at_queen_location(self, game_state):
        """
        builds something at the queen's current location
        """

        # first: determine if we have more archer barracks or knight barracks
        if len(game_state.my_archer_barracks) < len(game_state.my_knight_barracks):
            building_type = "BARRACKS-ARCHER"
        else:
            building_type = "BARRACKS-KNIGHT"

        command = "BUILD " + str(game_state.my_queen.touched_site) + " " + building_type

        return command

    def determine_train_move(self, game_state):
        """
        returns one string, command for training
        """
        command = "TRAIN"

        # for now, we are training one unit per round (should be OK, considering we only get 10 gold per round)

        # only strting thinking about it in round 10, and archers mostly

        # first, determine what type of unit we need to train
        # same approach as with building, first knights, then archers

        if self.game_turn > 10: 

            if len(game_state.my_archers) < len(game_state.my_knights):
                training_sites = game_state.my_archer_barracks
                training_cost = archer_price
            else:
                training_sites = game_state.my_knight_barracks
                training_cost = knight_price

            if game_state.gold > training_cost:
                site = self.choose_site_to_train(game_state, training_sites)
                if site is not None: 
                    command = command + " " + str(site.site_id)


        return command


    def choose_site_to_train(self, game_state, training_sites):
        """
        return one site from the training_sites where we should train
        """

        chosen_site = None

        # for now: going to pick that site that is available and closest to 

        min_distance = max_distance

        for site_id in training_sites:
            site = training_sites[site_id]
            # first, only process if the site is available, no production at the time
            if site.param_1 == 0:
                current_distance = Site.calculate_distance(site, game_state.opponent_queen)
                if current_distance < min_distance:
                    min_distance = current_distance
                    chosen_site = site

        return chosen_site

    def get_closest_site_to_queen(self, sites, queen):
        """
        from the list of sites, returns the one that is
        nearest to the queen
        can be used to determine where we should build (closest neutral to my_queen)
        or where to train (closest my site to opponent_queen)
        """

        min_distance = max_distance
        closest_site = None

        for site in sites.values():
            current_distance = Site.calculate_distance(site, queen)
            if current_distance < min_distance:
                min_distance = current_distance
                closest_site = site

        return closest_site


# **************
# 02 - STARTING INFRASTRUCTURE
# **************

sites = {}
my_queen = Unit()
opponent_queen = Unit()
agent = Agent()

units = []
#TODO here as a reminder, in every game round, we will update my units

num_sites = int(input())
for i in range(num_sites):
    site_id, x, y, radius = [int(j) for j in input().split()]
    sites[site_id] = Site(site_id, x, y, radius)


while True:

# **************
# 03 - GAME ROUND DATA
# **************

    gold, touched_site = [int(i) for i in input().split()]
    my_queen.touched_site = touched_site

# SITES

    for i in range(num_sites):
        site_id, ignore_1, ignore_2, structure_type, owner, param_1, param_2 = [int(j) for j in input().split()]
        # updating site with new information
        sites[site_id].update(structure_type, owner, param_1, param_2)

    # once we gathered sites, create three dictionaries 
    my_sites, my_knight_barracks, my_archer_barracks, neutral_sites, \
    opponent_sites, opponent_knight_barracks, opponent_archer_barracks  = \
    Site.split_sites_by_owner(sites)

# UNITS

    units = []
    num_units = int(input())
    for i in range(num_units):
        x, y, owner, unit_type, health = [int(j) for j in input().split()]
        # we are handling queens differently, keeping them in a global variable
        if unit_type == -1:
                if owner == 0:
                    my_queen.update(x, y, unit_type, owner, health)
                elif owner == 1: 
                    opponent_queen.update(x, y, unit_type, owner, health)
        else:
            # if they are not queen, keep units in the units list to be split later
            current_unit = Unit()
            current_unit.update(x, y, unit_type, owner, health)
            units.append(current_unit)

    # and same way as with the sites, we are splitting units 
    my_knights, my_archers, opponent_knights, opponent_archers = Unit.split_units_by_owner_and_type(units)

    # also, increase the game turn
    agent.increase_game_turn()


# **************
# 04 - RESPONSE
# **************

    game_state = GameState(
        my_sites, my_knight_barracks, my_archer_barracks, neutral_sites, \
        opponent_sites, opponent_knight_barracks, opponent_archer_barracks, \
        my_queen, opponent_queen, my_knights, my_archers, opponent_knights, opponent_archers, gold)

    commands = agent.determine_move(game_state)


    print(commands[0])
    print(commands[1])
