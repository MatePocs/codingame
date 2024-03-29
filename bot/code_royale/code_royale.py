import sys
import math

# GLOBAL VARIABLES

debugging_mode = True

archer_price = 100
knight_price = 80
giant_price = 140
max_distance = (1920 ** 2 + 1000 ** 2) ** 0.5


# **************
# 01 - CLASSES
# **************

class Site:
    """
    one site on the map
    """

    def __init__(self, site_id, x, y, radius):
        # the rest of the parameters will come in the first update phase
        self.site_id = site_id
        self.x = x
        self.y = y
        self.radius = radius

    def update(self, structure_type=None, gold_remaining = None, max_mine_size = None, owner=None, param_1=None, param_2=None):
        if structure_type is not None:
            self.structure_type = structure_type
        if gold_remaining is not None:
            self.gold_remaining = gold_remaining
        if owner is not None:
            self.max_mine_size = max_mine_size
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
        my_giant_barracks = {}
        my_towers = {}
        my_mines = {}
        neutral_sites = {}
        opponent_sites = {}
        opponent_knight_barracks = {}
        opponent_archer_barracks = {}
        opponent_giant_barracks = {}
        opponent_towers = {}
        opponent_mines = {}

        for site_id in sites:
            site = sites[site_id]
            if site.owner == 0:
                my_sites[site_id] = site
                if site.structure_type == 0:
                    my_mines[site_id] = site
                elif site.structure_type == 1:
                    my_towers[site_id] = site
                elif site.structure_type == 2:
                    if site.param_2 == 0:
                        my_knight_barracks[site_id] = site
                    elif site.param_2 == 1:
                        my_archer_barracks[site_id] = site
                    elif site.param_2 == 2:
                        my_giant_barracks[site_id] = site
            elif site.owner == 1:
                opponent_sites[site_id] = site
                if site.structure_type == 0:
                    opponent_mines[site_id] = site
                elif site.structure_type == 1:
                    opponent_towers[site_id] = site
                elif site.structure_type == 2:
                    if site.param_2 == 0:
                        opponent_knight_barracks[site_id] = site
                    elif site.param_2 == 1:
                        opponent_archer_barracks[site_id] = site
                    elif site.param_2 == 2:
                        opponent_giant_barracks[site_id] = site
            elif site.owner == -1:
                neutral_sites[site_id] = site

        return my_sites, my_knight_barracks, my_archer_barracks, my_giant_barracks, my_towers, my_mines, \
               neutral_sites, \
               opponent_sites, opponent_knight_barracks, opponent_archer_barracks, opponent_giant_barracks, opponent_towers, opponent_mines

    @staticmethod
    def calculate_distance(object1, object2):
        """
        calculates the distance between two objects (straight line) that both need to have x and y attributes
        """

        return ((object1.x - object2.x) ** 2 + (object1.y - object2.y) ** 2) ** 0.5


class Unit:
    """
    contains information about the unit
    """

    def __init__(self, x, y, owner, unit_type, health):
        self.x = x
        self.y = y
        self.owner = owner
        self.unit_type = unit_type
        self.health = health

    def update(self, touched_site):
        self.touched_site = touched_site

    def calc_distance_from_my_queen(self, my_queen):
        self.distance_from_my_queen = Site.calculate_distance(self, my_queen)

    @staticmethod
    def split_units_by_owner_and_type(units):
        """
        takes a list of units, and sorts them into four lists
        """
        my_knights = []
        my_archers = []
        my_giants = []
        opponent_knights = []
        opponent_archers = []
        opponent_giants = []

        for unit in units:
            if unit.owner == 0:
                if unit.unit_type == -1:
                    my_queen = unit
                elif unit.unit_type == 0:
                    my_knights.append (unit)
                elif unit.unit_type == 1:
                    my_archers.append (unit)
                elif unit.unit_type == 2:
                    my_giants.append (unit)

            elif unit.owner == 1:
                if unit.unit_type == -1:
                    opponent_queen = unit
                if unit.unit_type == 0:
                    opponent_knights.append (unit)
                elif unit.unit_type == 1:
                    opponent_archers.append (unit)
                elif unit.unit_type == 2:
                    opponent_giants.append (unit)

        return my_queen, opponent_queen, my_knights, my_archers, my_giants, \
               opponent_knights, opponent_archers, opponent_giants


class GameState:
    """
    only purpose is to group the data
    """

    def __init__(
            self, my_sites, my_knight_barracks, my_archer_barracks, my_giant_barracks, my_towers, my_mines,
            neutral_sites,
            opponent_sites, opponent_knight_barracks, opponent_archer_barracks, opponent_giant_barracks,
            opponent_towers, opponent_mines,
            my_queen, opponent_queen,
            my_knights, my_archers, my_giants,
            opponent_knights, opponent_archers, opponent_giants,
            gold):
        self.my_sites = my_sites
        self.my_knight_barracks = my_knight_barracks
        self.my_archer_barracks = my_archer_barracks
        self.my_giant_barracks = my_giant_barracks
        self.my_towers = my_towers
        self.my_mines = my_mines
        self.neutral_sites = neutral_sites
        self.opponent_sites = opponent_sites
        self.opponent_knight_barracks = opponent_knight_barracks
        self.opponent_archer_barracks = opponent_archer_barracks
        self.opponent_giant_barracks = opponent_giant_barracks
        self.opponent_towers = opponent_towers
        self.opponent_mines = opponent_mines
        self.my_queen = my_queen
        self.opponent_queen = opponent_queen
        self.my_knights = my_knights
        self.my_archers = my_archers
        self.my_giants = my_giants
        self.opponent_knights = opponent_knights
        self.opponent_archers = opponent_archers
        self.opponent_giants = opponent_giants

        self.gold = gold


class Agent:
    """
    our agent that determines our steps for the round
    """

    def __init__(self):
        self.game_turn = 0
        self.queen_distance_danger = 100
        self.mine_limit = 3

    def increase_game_turn(self):
        self.game_turn += 1

    def determine_move(self, game_state):
        """
        returns a list of two strings, first: queen command, second: train command
        """
        commands = []
        queen_move = self.determine_queen_move (game_state)
        commands.append (queen_move)
        train_move = self.determine_train_move (game_state)
        commands.append (train_move)
        return commands

    def determine_queen_move(self, game_state):
        """
        returns one string, command for the queen
        """

        # first of all: check if there are any enemy knights

        closest_knight = self.get_closest_opponent_knight_to_queen(game_state)

        command = None

        if not(closest_knight is None):
            if closest_knight.distance_from_my_queen < self.queen_distance_danger:
                command = self.determine_escape_move(game_state, closest_knight)
        
        if command is None:
            command = self.determine_expansion_move(game_state)

        return command

    def should_queen_escape(self, game_state):
        """
        determines if we should push for expansion or escape with queen
        """
        # if closest enemy knight is 

        should_escape = False

        if game_state.my_queen.health < 40:
            should_escape = True

        return should_escape

    def get_closest_opponent_knight_to_queen(self, game_state):
        """
        calculates the closest knight to the queen
        """
        closest_knight = None
        closest_distance = max_distance
        for opponent_knight in game_state.opponent_knights:
            if opponent_knight.distance_from_my_queen < closest_distance:
                closest_distance = opponent_knight.distance_from_my_queen
                closest_knight = opponent_knight

        return closest_knight



    def determine_escape_move(self, game_state, closest_knight):
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

        command = "MOVE " + str (destination_x) + " " + str (destination_y)

        return command

    def determine_expansion_move(self, game_state):
        """
        determines where the queen should move to build new buildings
        """
        
        command = None

        # check if queen is touching a site
        if game_state.my_queen.touched_site != -1:
            # if it's a neutral site, build there accordingly
            if game_state.my_queen.touched_site in game_state.neutral_sites:
                command = self.build_at_queen_location(game_state, "automatic")
            # otherwise, if queen is touching my mine, and its level is under required, upgrade
            elif game_state.my_queen.touched_site in game_state.my_mines:
                # only build if we can, i.e. we have not reached the limit yet
                if game_state.my_mines[game_state.my_queen.touched_site].param_1 < game_state.my_mines[game_state.my_queen.touched_site].max_mine_size:
                    command = self.build_at_queen_location(game_state, "mine")
        
        if command is None:
            # if not: select the neutral site that is nearest to queen
            closest_site = self.get_closest_site_to_queen (
                sites_list=[game_state.neutral_sites, game_state.opponent_knight_barracks, game_state.opponent_archer_barracks], \
                queen=game_state.my_queen)
            if closest_site is None:
                # if we are still empty, move to current position
                closest_site = game_state.my_queen

            command = "MOVE " + str (closest_site.x) + " " + str (closest_site.y)

        return(command)
        
    def build_at_queen_location(self, game_state, building_type_decision):
        """
        builds something at the queen's current location
        """
        if building_type_decision == "automatic":
            building_type = self.next_in_predetermined_building_list (game_state)
        elif building_type_decision == "mine":
            building_type = "MINE"
            
        command = "BUILD " + str (game_state.my_queen.touched_site) + " " + building_type

        return command


    def next_in_predetermined_building_list(self, game_state):
        """
        builds by a pre-determined list
        we have a list of building types
        one by one checks if we have the required buildings up until that point
        the first time when we don't, that is the building type to build
        at the end of the list, keeps building last building
        """

        building_list = self.determine_building_list (game_state)

        current_buildings = {}
        current_buildings["BARRACKS-ARCHER"] = len (game_state.my_archer_barracks)
        current_buildings["BARRACKS-KNIGHT"] = len (game_state.my_knight_barracks)
        current_buildings["BARRACKS-GIANT"] = len (game_state.my_giant_barracks)
        current_buildings["TOWER"] = len (game_state.my_towers)
        current_buildings["MINE"] = len (game_state.my_mines)

        for building_type in building_list:
            if current_buildings[building_type] > 0:
                current_buildings[building_type] -= 1
            else:
                break

        return building_type

    def determine_building_list(self, game_state):
        """
        determines what kind of buildings we should have
        """
        # for now: fix

        building_list = \
            ["MINE", "MINE", "BARRACKS-ARCHER", "BARRACKS-KNIGHT", "MINE","TOWER", "MINE", "TOWER", \
             "BARRACKS-ARCHER", "BARRACKS-KNIGHT", "TOWER", "TOWER", "MINE"]

        return building_list

    def determine_train_move(self, game_state):
        """
        returns one string, command for training
        """

        command = "TRAIN"

        # for now, we are training one unit per round 

        if self.game_turn > 3:

            if (len (game_state.my_archers) < len (game_state.my_knights) or \
                len(game_state.my_knight_barracks) == 0) and len(opponent_knights) > 0:
                training_sites = game_state.my_archer_barracks
                training_cost = archer_price
            else:
                training_sites = game_state.my_knight_barracks
                training_cost = knight_price

            if game_state.gold > training_cost:
                site = self.choose_site_to_train (game_state, training_sites)
                if site is not None:
                    command = command + " " + str (site.site_id)

        return command

    def choose_site_to_train(self, game_state, training_sites):
        """
        return one site from the training_sites where we should train
        """

        chosen_site = None

        # for now: going to pick that site that is available and closest to opponent queen

        min_distance = max_distance

        for site_id in training_sites:
            site = training_sites[site_id]
            # first, only process if the site is available, no production at the time
            if site.param_1 == 0:
                current_distance = Site.calculate_distance (site, game_state.opponent_queen)
                if current_distance < min_distance:
                    min_distance = current_distance
                    chosen_site = site

        return chosen_site

    def get_closest_site_to_queen(self, sites_list, queen):
        """
        from the list of sites, returns the one that is
        nearest to the queen
        can be used to determine where we should build (closest neutral to my_queen)
        or where to train (closest my site to opponent_queen)
        """

        min_distance = max_distance
        closest_site = None

        for sites in sites_list:

            for site in sites.values ():
                current_distance = Site.calculate_distance (site, queen)
                if current_distance < min_distance:
                    min_distance = current_distance
                    closest_site = site

        return closest_site


# **************
# 02 - STARTING INFRASTRUCTURE
# **************

sites = {}
agent = Agent ()

num_sites = int (input ())
for i in range (num_sites):
    site_id, x, y, radius = [int (j) for j in input ().split ()]
    sites[site_id] = Site (site_id, x, y, radius)

while True:

    # **************
    # 03 - GAME ROUND DATA
    # **************

    gold, touched_site = [int (i) for i in input ().split ()]

    # SITES

    for i in range (num_sites):
        site_id, gold_remaining, max_mine_size, structure_type, owner, param_1, param_2 = [int (j) for j in input ().split ()]
        # updating site with new information
        sites[site_id].update (structure_type, gold_remaining, max_mine_size, owner, param_1, param_2)

    # once we gathered sites, create three dictionaries 
    my_sites, my_knight_barracks, my_archer_barracks, my_giant_barracks, my_towers, my_mines, \
    neutral_sites, \
    opponent_sites, opponent_knight_barracks, opponent_archer_barracks, opponent_giant_barracks, opponent_towers, opponent_mines = \
        Site.split_sites_by_owner (sites)

    # UNITS

    units = []
    num_units = int (input ())
    for i in range (num_units):
        x, y, owner, unit_type, health = [int (j) for j in input ().split ()]
        current_unit = Unit (x, y, owner, unit_type, health)
        units.append (current_unit)

    # and same way as with the sites, we are splitting units 
    my_queen, opponent_queen, my_knights, my_archers, my_giants, opponent_knights, opponent_archers, opponent_giants = Unit.split_units_by_owner_and_type (
        units)

    my_queen.update (touched_site)

    # for opponent knights, calculate how far they are from my queen
    for opponent_knight in opponent_knights:
        opponent_knight.calc_distance_from_my_queen(my_queen)

    # also, increase the game turn
    agent.increase_game_turn ()

    # **************
    # 04 - RESPONSE
    # **************

    game_state = GameState (
        my_sites, my_knight_barracks, my_archer_barracks, my_giant_barracks, my_towers, my_mines,
        neutral_sites,
        opponent_sites, opponent_knight_barracks, opponent_archer_barracks, opponent_giant_barracks, opponent_towers,
        opponent_mines,
        my_queen, opponent_queen,
        my_knights, my_archers, my_giants,
        opponent_knights, opponent_archers, opponent_giants,
        gold)

    commands = agent.determine_move (game_state)

    print (commands[0])
    print (commands[1])
