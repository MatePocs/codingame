import sys
import math


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

class Unit:
    """
    contains information about the unit
    """

    def __init__(self):
        pass

    def update(self, x, y, health, unit_type):
        self.x = x
        self.y = y
        self.health = health
        self.unit_type = unit_type


class Agent:
    """
    our agent that determines our steps for the round
    """
    def __init__(self):
        pass

    def determine_move(self, sites, my_queen):
        """
        returns a list of two strings, first: queen command, second: train command
        """
        commands = []
        queen_move = self.determine_queen_move(sites, my_queen)
        commands.append(queen_move)
        train_move = self.determine_train_move(sites)
        commands.append(train_move)
        return commands

    def determine_queen_move(self, sites, my_queen):
        """
        returns one string, command for the queen
        """

        # for now: if touches something, build there a type of barrack
        # if doesn't touch anything: move towards nearest site

        if touched_site == -1:
            nearest_site = self.get_nearest_empty_site_to_queen(sites,my_queen)
            command = "MOVE " + str(nearest_site.x) + " " + str(nearest_site.y)
        else:
            command = "BUILD " + str(touched_site) + " BARRACKS-KNIGHT"


        return command

    def determine_train_move(self, sites):
        """
        returns one string, command for training
        """
        command = "TRAIN"
        return command

    def get_nearest_empty_site_to_queen(self, sites, my_queen):
        """
        from the list of sites, returns the one that is empty and
        nearest to the queen
        """

        min_distance = (1920**2 + 1000**2) ** 0.5
        closest_site = None

        for site in sites.values():
            if site.owner == 0:
                current_distance = ((site.x - my_queen.x) ** 2 + (site.y - my_queen.y) ** 2) ** 0.5
                if current_distance < min_distance:
                    min_distance = current_distance
                    closest_site = site

        return closest_site


# **************
# 02 - STARTING INFRASTRUCTURE
# **************

sites = {}
my_queen = Unit()
agent = Agent()

my_units = []
#here as a reminder, in every game round, we will update my units

num_sites = int(input())
for i in range(num_sites):
    site_id, x, y, radius = [int(j) for j in input().split()]
    sites[site_id] = Site(site_id, x, y, radius)


while True:

# **************
# 03 - GAME ROUND DATA
# **************

    gold, touched_site = [int(i) for i in input().split()]
    for i in range(num_sites):
        site_id, ignore_1, ignore_2, structure_type, owner, param_1, param_2 = [int(j) for j in input().split()]
        # updating site with new information
        sites[site_id].update(structure_type, owner, param_1, param_2)


    num_units = int(input())
    for i in range(num_units):
        x, y, owner, unit_type, health = [int(j) for j in input().split()]
        # for now: only keeping track of queen and my own units
        if owner == 0:
            if unit_type == -1:
                my_queen.update(x, y, unit_type, health)
            else:
                pass



# **************
# 04 - RESPONSE
# **************

    commands = agent.determine_move(sites,my_queen)


    print(commands[0])
    print(commands[1])
