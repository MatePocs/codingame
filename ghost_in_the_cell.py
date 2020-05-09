import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

distances = {}

factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories
for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    distances[(factory_1, factory_2)] = distance

# in the distances dictionary, factory_1 < factory_2, tested it

# game loop
while True:
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
                opponent_troops.append(factory)
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

# STRATEGY 1

    # OK, simple strategy: in every turn, take our factory with the most
    # current robots, and send out half to the nearest factory that is not ours

    max_cyborg = 0
    max_id = None
    for factory in my_factories:
        current_cyborg = factory['cyborgs']
        #paradigm change, only send out from factories where prod is below 3
        if current_cyborg > max_cyborg and factory['production'] == 3:
            max_cyborg = current_cyborg
            max_id = factory['id']

    # i think we can send 0 troops, 
    # so won't add a WAIT for cases when we dont have available

    # find factory closest to ours
    # haha, modify, we need to target the one that prodocue first

    min_distance_3 = 21
    min_id_3 = None

    min_distance_2 = 21
    min_id_2 = None

    min_distance_1 = 21
    min_id_1 = None

    min_distance_0 = 21
    min_id_0 = None

    for factory in opponent_factories + neutral_factories:

        if max_id is None:
            current_distance = 21
        else:
            current_key = \
            (min(max_id, factory['id']), max(max_id, factory['id']))

            current_distance = distances[current_key]

        if factory['production'] == 3:
            if current_distance < min_distance_3:
                min_distance_3 = current_distance
                min_id_3 = factory['id']
        elif factory['production'] == 2:
            if current_distance < min_distance_2:
                min_distance_2 = current_distance
                min_id_2 = factory['id']
        elif factory['production'] == 1:
            if current_distance < min_distance_1:
                min_distance_1 = current_distance
                min_id_1 = factory['id']
        elif factory['production'] == 0:
            if current_distance < min_distance_0:
                min_distance_0 = current_distance
                min_id_0 = factory['id']

    min_id = None

    if min_id_3 is not None:
        min_id = min_id_3
    elif min_id_2 is not None:
        min_id = min_id_2
    elif min_id_1 is not None:
        min_id = min_id_1
    else:
        min_id = min_id_0

    if min_id == None:
        command = 'WAIT'
    else:
        command = \
        'MOVE' + ' ' + str(max_id) + ' ' + str(min_id) + ' ' + str(int(max_cyborg/2))

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
        command = command + ';' + bomb_command

# STRATEGY 3

    # increase production whenever we can, will only send out troops from factories 
    # where we have 3 production

    increase_production = []

    for factory in my_factories:
        if factory['production'] < 3 and factory['cyborgs'] >= 10:
            increase_production.append(factory['id'])

    increase_command = ''
    for factory_id in increase_production:
        increase_command += 'INC' + ' ' + str(factory_id) + ';'

    command = increase_command + command

    # Any valid action, such as "WAIT" or "MOVE source destination cyborgs"
    print(command)
