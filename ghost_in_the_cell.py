import sys
import math
from enum import Enum

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

distances = {}

factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories
for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    distances[(factory_1, factory_2)] = distance
# in the distances dictionary, factory_1 < factory_2, tested it



class Player(Enum):
    ME = 1
    OPPONENT = 2
    NEUTRAL = 3



def project_state_at_factory(factory, my_additional_troops = []):
    """
    for a certain facotry, projects 20 turns of my troops - enemy troops
    taking only current information into account
    returns a list with 21 tuples, owner, number_of_troops, my_cum_production, opponent_cum_production
    index 0 is current round
    input is assumed to be same dictionary

    my_additional_troops: the troops analysed when we calculate the impact of sending additional ones

    TODO: this excludes bomb strategies now

    """

    projections = []
    my_new_troops = [0] * 21
    opponent_new_troops = [0] * 21

    production = factory['production']
    factory_id = factory['id']
    current_cyborgs = factory['cyborgs']

    my_cum_production = 0
    opponent_cum_production = 0


    if factory in my_factories:
        current_owner = Player.ME
    elif factory in opponent_factories:
        current_owner = Player.OPPONENT
    else:
        current_owner = Player.NEUTRAL

    projections.append((current_owner, current_cyborgs, my_cum_production, opponent_cum_production))

    # get troops headed there 
    for troop in my_troops:
        if troop['target'] == factory_id:
            my_new_troops[troop['remaining_turns']] += troop['cyborgs']

    for troop in opponent_troops:
        if troop['target'] == factory_id:
            opponent_new_troops[troop['remaining_turns']] += troop['cyborgs']

    if my_additional_troops:
        for troop in my_additional_troops:
            my_new_troops[troop['remaining_turns']] += troop['cyborgs']

    for i in range(1, 20 + 1):
        # first, if owner was me or opponent, add production
        if current_owner == Player.ME or current_owner == Player.OPPONENT:
            current_cyborgs += production
            if current_owner == Player.ME:
                my_cum_production += production
            else:
                opponent_cum_production += production

        # next, check if new cyborgs arrived
        my_new_cyborgs = my_new_troops[i]
        opponent_new_cyborgs = opponent_new_troops[i]

        # 4 main cases, based on who has new cyborgs

        if my_new_cyborgs == 0 and opponent_new_cyborgs == 0:
            # nothing changes
            pass
        else:
            # first, there is a battle, so only one of us will have cyborgs left
            if my_new_cyborgs >= opponent_new_cyborgs:
                new_cyborgs = my_new_cyborgs - opponent_new_cyborgs
                attacker = Player.ME
            else:
                new_cyborgs = opponent_new_cyborgs - my_new_cyborgs
                attacker = Player.OPPONENT

            # if owner is the same as attacker, owner does not change, cyborgs add
            if current_owner == attacker:
                current_cyborgs += new_cyborgs
            else:
                # we check if siege is successful or not
                if new_cyborgs <= current_cyborgs:
                    current_cyborgs -= new_cyborgs
                else:
                    current_owner = attacker
                    current_cyborgs = new_cyborgs - current_cyborgs

        projections.append((current_owner, current_cyborgs, my_cum_production, opponent_cum_production))

    return projections

def calculate_cum_production_difference(factory_origin, factory_target, number_of_cyborgs, distance):
    """
    calculates an alternative scenario in which we send number_of_cyborgs from factory_origin to factory_target
    compares the results of the alternative scenario with the original projection, takes difference
    an additional production for us is same as -1 for opponent
    calculates it at the end of 20-turn projection
    """

    target_me_old_cum_production = factory_target['projection'][20][2]
    target_opponent_old_cum_production = factory_target['projection'][20][3]


    # we create a planned troop, in the same structure as regular toops
    planned_troop = {}

    planned_troop['cyborgs'] = number_of_cyborgs
    planned_troop['remaining_turns'] = distance + 1

    alternative_projections_target = project_state_at_factory(factory_target, [planned_troop])
    target_me_new_cum_production = alternative_projections_target[20][2]
    target_opponent_new_cum_production = alternative_projections_target[20][3]

    target_cum_production_difference = \
        target_me_new_cum_production - target_me_old_cum_production - \
        (target_opponent_new_cum_production - target_opponent_old_cum_production)

    return target_cum_production_difference

def get_number_of_cyborgs_with_same_impact_as_all(factory_origin, factory_target, distance):
    """
    calculates the minimum number of cyborgs to be sent from origin to target
    that would result in the same cumulative production difference 
    as sending the maximum available

    using a binary search
    """
    max_cyborgs = factory_origin['cyborgs']

    min_cyborgs = 0

    max_target_cum_production_difference = \
        calculate_cum_production_difference(factory_origin, factory_target, max_cyborgs, distance)

    # print(max_target_cum_production_difference, file = sys.stderr)

    while max_cyborgs - min_cyborgs > 1:
        current_cyborgs_to_check = int((max_cyborgs + min_cyborgs) / 2)

        # print(current_cyborgs_to_check, file = sys.stderr)
        # print(current_cyborgs_to_check, file = sys.stderr)
        current_target_cum_production_difference = \
            calculate_cum_production_difference(factory_origin, factory_target, current_cyborgs_to_check, distance)
        # print(current_target_cum_production_difference, file = sys.stderr)
        if current_target_cum_production_difference >= max_target_cum_production_difference:
            max_target_cum_production_difference = current_target_cum_production_difference
            max_cyborgs = current_cyborgs_to_check
        else:
            min_cyborgs = current_cyborgs_to_check

        # print(max_cyborgs, min_cyborgs, max_target_cum_production_difference, file = sys.stderr)

    return max_cyborgs, max_target_cum_production_difference


def get_factories_distance(factory_1, factory_2):
    
    return distances[(min(factory_1['id'], factory_2['id']), max(factory_1['id'], factory_2['id']))]

def score_of_possible_action(possible_action):
    """
    assigns a score to the possible action based on number of cyborgs, length, and difference in cum prod
    the higher the score, the better
    """
    cyborgs = max(possible_action['cyborgs'],1)
    # there is some 0 number cyborg here, should be avoided
    remaining_turns = possible_action['remaining_turns']
    target_cum_prod_diff = possible_action['target_cum_prod_diff']

    return target_cum_prod_diff / cyborgs / remaining_turns

def convert_command_to_string(commands):

    if commands:
        command_string = commands[0]
        if len(commands) > 1:
            for i in range(1, len(commands)):
                command_string += ';'
                command_string += commands[i]

    else:
        command_string = 'WAIT'

    return command_string

# game loop
while True:

# DATA COLLECTION
# collecting data in every single game turn

    entity_count = int(input())  # the number of entities (e.g. factories and troops)

    my_factories = []
    opponent_factories = []
    neutral_factories = []

    my_troops = []
    opponent_troops = []

    my_bombs = []
    opponent_bombs = []

    for i in range(entity_count):
        entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()
        entity_id = int(entity_id)
        arg_1 = int(arg_1)
        arg_2 = int(arg_2)
        arg_3 = int(arg_3)
        arg_4 = int(arg_4)
        arg_5 = int(arg_5)

        if entity_type == 'FACTORY':
        # save factories
            factory = {}
            factory['id'] = entity_id
            factory['cyborgs'] = arg_2
            factory['production'] = arg_3
            if arg_1 == 1:
                my_factories.append(factory)
            elif arg_1 == -1:
                opponent_factories.append(factory)
            else:
                neutral_factories.append(factory)
        elif entity_type == 'TROOP':
        # save troops
            troop = {} 
            troop['id'] = entity_id
            troop['origin'] = arg_2
            troop['target'] = arg_3
            troop['cyborgs'] = arg_4
            troop['remaining_turns'] = arg_5
            if arg_1 == 1:
                my_troops.append(troop)
            elif arg_1 == -1:
                opponent_troops.append(troop)
        elif entity_type == 'BOMB':
        # save bombs
            bomb = {}
            bomb['origin'] = arg_2
            bomb['target'] = arg_3
            bomb['remaining_turns'] = arg_4
            if arg_1 == 1:
                my_bombs.append(bomb)
            elif arg_1 == -1:
                opponent_bombs.append(bomb)

    # for all the factories, create baseline projections
    for factory in my_factories + opponent_factories + neutral_factories:
        projection = project_state_at_factory(factory)
        factory['projection'] = projection

# COMMANDS        

    commands = []

# STRATEGY PART 1 - MOVING TROOPS
# for each of our factories, loop through every other factory
# calculate the increase in cumulative production difference by round 20
# assuming we send there all of our troops there
# then calculate the minimum number of sent troops that would also result in
# and finally, come up with a score: 
# distance * troops needed / cum_prod_diff

    # we are doing a loop on the factories, check if there was any new action, and 
    # then repeat until there was at least one company that made an action
    # first, we set all the skipped turns to none

    for factory_analysed in my_factories:
        factory_analysed['new_action'] = True

    at_least_one_factory = True

    while at_least_one_factory:

        at_least_one_factory = False

        for factory_analysed in my_factories:

            if factory_analysed['new_action'] == True:

                max_score = 0
                chosen_action = None

                # loop through all possible
                for factory in my_factories + opponent_factories + neutral_factories:
                    if factory['id'] != factory_analysed['id']:
                        
                        distance = get_factories_distance(factory_analysed, factory)

                        required_cyborgs, max_target_cum_production_difference = \
                        get_number_of_cyborgs_with_same_impact_as_all(factory_analysed, factory, distance)
                        # print(factory['id'], required_cyborgs, max_target_cum_production_difference, file = sys.stderr)

                        possible_action = {}
                        possible_action['origin'] = factory_analysed['id']
                        possible_action['target'] = factory['id']

                        possible_action['remaining_turns'] = distance
                        possible_action['cyborgs'] = required_cyborgs
                        possible_action['target_cum_prod_diff'] = max_target_cum_production_difference

                        current_score = score_of_possible_action(possible_action)
                        if current_score > max_score:
                            max_score = current_score
                            chosen_action = possible_action
                            chosen_factory = factory


                # if there is a chosen action, assume that we issued the order, and 
                # adjust baseline tatistics

                if chosen_action is not None:

                    # print(chosen_action, file = sys.stderr)

                    at_least_one_factory = True

                    # add to troops so our future estimations this round are correct

                    additional_troop = {}

                    additional_troop['origin'] = chosen_action['origin']
                    additional_troop['target'] = chosen_action['target']
                    additional_troop['cyborgs'] = chosen_action['cyborgs']
                    additional_troop['remaining_turns'] = chosen_action['remaining_turns']

                    my_troops.append(additional_troop)

                    # adjust origin population

                    factory_analysed['cyborgs'] -= chosen_action['cyborgs']

                    # adjust target factory projection
                    projection = project_state_at_factory(chosen_factory)
                    chosen_factory['projection'] = projection

                    # create a new command

                    new_command = 'MOVE ' + str(chosen_action['origin']) + ' ' + \
                        str(chosen_action['target']) + ' ' + str(chosen_action['cyborgs'])

                    commands.append(new_command)

                else:
                    # if there was no action chosen, switch the 
                    factory_analysed['new_action'] = False

# STRATEGY 2

    # not tracking bombs yet, but if other player has a factory with 2 or 3, 
    # launch a bomb from our first factory
    bomb_target = None

    for factory in opponent_factories:
        if factory['production'] == 2 or factory['production'] == 3:
            # only if we are not already targeting that factory
            if my_bombs:
                if my_bombs[0]['target'] != factory['id']:
                    bomb_target = factory['id']
                    break
            else:
                bomb_target = factory['id']
                break 

    if bomb_target is not None: 
        bomb_command = \
        'BOMB' + ' ' + str(my_factories[0]['id']) + ' ' + str(bomb_target)

        commands.append(bomb_command)

# STRATEGY 3

    # increase production whenever we can, will only send out troops from factories 
    # where we have 3 production

    increase_production = []

    for factory in my_factories:
        if factory['production'] < 3 and factory['cyborgs'] >= 10:
            increase_production.append(factory['id'])

    for factory_id in increase_production:
        increase_command = 'INC '  + str(factory_id)

        commands.append(increase_command)

    # Any valid action, such as "WAIT" or "MOVE source destination cyborgs"


    command_string = convert_command_to_string(commands)


    print(command_string)
