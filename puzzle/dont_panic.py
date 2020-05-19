import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# nb_floors: number of floors
# width: width of the area
# nb_rounds: maximum number of rounds
# exit_floor: floor on which the exit is found
# exit_pos: position of the exit on its floor
# nb_total_clones: number of generated clones
# nb_additional_elevators: ignore (always zero)
# nb_elevators: number of elevators
nb_floors, width, nb_rounds, exit_floor, exit_pos, nb_total_clones, nb_additional_elevators, nb_elevators = [int(i) for i in input().split()]
elevators = []
for i in range(nb_elevators):
    # elevator_floor: floor on which this elevator is found
    # elevator_pos: position of the elevator on its floor
    elevator_floor, elevator_pos = [int(j) for j in input().split()]
    elevators.append((elevator_floor, elevator_pos))

arrived_at_new_floor = True
old_floor = 0
stopping_points = [0] * 2

# game loop
while True:
    # clone_floor: floor of the leading clone
    # clone_pos: position of the leading clone on its floor
    # direction: direction of the leading clone: LEFT or RIGHT
    clone_floor, clone_pos, direction = input().split()
    clone_floor = int(clone_floor)
    clone_pos = int(clone_pos)

    # check if we arrived at a new floor

    if clone_floor != old_floor:
        arrived_at_new_floor = True
        old_floor = clone_floor

    # calculate the target that we want to reach 
    # this should be calculated once per floor, when we arrive

    if arrived_at_new_floor:

        if clone_floor == exit_floor:
            target_pos = exit_pos
        else:
            for elevator_tup in elevators:
                if elevator_tup[0] == clone_floor:
                    target_pos = elevator_tup[1]
                    break
        arrived_at_new_floor = False

        #if we arrived at a new floor, we also establish stopping points for the leader
        # possible two stoppoing points: 
        # if we are moving in the wrong direction, the first one
        # and then just after the target pos

        if target_pos > clone_pos:
            if direction == 'lEFT':
                # we are heading in the wrong dir
                stopping_points[0] = clone_pos - 1
                stopping_points[1] = target_pos + 1
            elif direction == 'RIGHT':
                stopping_points[0] = 0
                stopping_points[1] = target_pos + 1
        elif target_pos < clone_pos:
            if direction == 'RIGHT':
                stopping_points[0] = clone_pos + 1
                stopping_points[1] = target_pos - 1
            elif direction == 'LEFT':
                stopping_points[0] = 0
                stopping_points[1] = target_pos - 1

    # and in any case, we are stopping with the leader if we are at a stopping point

    if clone_pos in stopping_points:
        command = 'BLOCK'
    else:
        command = 'WAIT'

    # action: WAIT or BLOCK
    print(command)
