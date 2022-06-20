import sys
import math
from collections import namedtuple
from enum import Enum
import copy

class CardType(Enum):
	TRAINING = 0
	CODING = 1
	DAILY_ROUTINE = 2
	TASK_PRIORITIZATION = 3
	ARCHITECTURE_STUDY = 4
	CONTINUOUS_INTEGRATION = 5
	CODE_REVIEW = 6
	REFACTORING = 7
	BONUS = 8
	TECHNICAL_DEBT = 9

skill_card_types_number = 8

class GameState:

	# used to store all relevant game info in one object
	# TODO keep track of number of cards at locations somehow

	def __init__(self, game_phase, applications, player_info, card_locations, possible_moves):
		self.game_phase = game_phase
		self.applications = applications
		self.player_info = player_info
		self.card_locations = card_locations
		self.possible_moves = possible_moves

	def update_card_location(self, card_location_key, card_index, change_amount):

		# updates a piece of card count
		# e.g. for the projection, we increase certain card by one

		self.card_locations[card_location_key][card_index] += change_amount

class Agent:

	# decisionmaker

	def __init__(self):
		pass

	def get_command(self, game_state):

		# main function, every result comes ultimately from this hub

		command = ""

		# In the first league: RANDOM | MOVE <zoneId> | RELEASE <applicationId> | WAIT; In later leagues: | GIVE <cardType> | THROW <cardType> | TRAINING | CODING | DAILY_ROUTINE | TASK_PRIORITIZATION <cardTypeToThrow> <cardTypeToTake> | ARCHITECTURE_STUDY | CONTINUOUS_DELIVERY <cardTypeToAutomate> | CODE_REVIEW | REFACTORING;
		if game_state.game_phase == "MOVE":
			
			projected_states_after_moves = self.get_projected_states_after_moves(game_state)

			print(projected_states_after_moves, file = sys.stderr)

			# gonna do it weird for now, we select the move goal where it is max but not current

			location_to_move_to = None

			current_max = 0
			for i in range (skill_card_types_number):
				if i != game_state.player_info['my_player']['location']:
					if projected_states_after_moves[i] > current_max:
						location_to_move_to = i
						curent_max = projected_states_after_moves[i]

			if location_to_move_to is None: 
				command = "RANDOM"
			else:
				command = f'MOVE {location_to_move_to}'

		elif game_state.game_phase == "GIVE_CARD":
			# Starting from league 2, you must give a card to the opponent if you move close to them.
			# Write your code here to give a card
			# RANDOM | GIVE cardTypeId
			command = "RANDOM"
		elif game_state.game_phase == "THROW_CARD":
			# Starting from league 3, you must throw 2 cards away every time you go through the administrative task desk.
			# Write your code here to throw a card
			# RANDOM | THROW cardTypeId
			command = "RANDOM"
		elif game_state.game_phase == "PLAY_CARD":
			# Starting from league 2, you can play some cards from your hand.
			# Write your code here to play a card
			# WAIT | RANDOM | TRAINING | CODING | DAILY_ROUTINE | TASK_PRIORITIZATION <cardTypeIdToThrow> <cardTypeIdToTake> | ARCHITECTURE_STUDY | CONTINUOUS_INTEGRATION <cardTypeIdToAutomate> | CODE_REVIEW | REFACTORING
			command = "RANDOM"
		elif game_state.game_phase == "RELEASE":

			# simple approach for now: we release anything that we can do without shoddy skills
			
			valid_applications = self.assess_applications_availability(game_state)
			if len(valid_applications) == 0:
				command = "RANDOM"
			else:
				print(valid_applications, file  = sys.stderr)
				command = f"RELEASE {valid_applications[0]}"
		else:
			command = "RANDOM"

		return command

	def get_projected_states_after_moves(self, game_state):

		# loops through potential moves 
		# returns something
		# for now, that something is the length of valid applications assuming we go to the location and get a card there

		projected_states_after_moves = []

		for i in range(8):
			game_state.update_card_location("HAND", i, +1)
			# game_state.card_locations["HAND"][i] += 1
			valid_applications = self.assess_applications_availability(game_state)
			projected_states_after_moves.append(len(valid_applications))

			# print(f"moving to position {i} will result in these valid applications: {valid_applications}", file = sys.stderr)
			# print(f"that is because we have this projected hand: {game_state.card_locations['HAND']}", file = sys.stderr)

			game_state.update_card_location("HAND", i, -1)
			# game_state.card_locations["HAND"][i] -= 1


		return projected_states_after_moves


	def assess_applications_availability(self, game_state):

		# very simple approach, probably needs to be retuned later
		# loops through the list of application ids
		# returns a list of the application ids that we can actually do RIGHT NOW without shoddy

		valid_applications = []

		for application in game_state.applications:
			if self.assess_application_availiability(application[1][:], game_state.card_locations["HAND"]) == True: # FFS needs a [:] here to copy
				valid_applications.append(application[0])

		return valid_applications

	def assess_application_availiability(self, application_requirements, card_counts):

		# checks whether the card_counts cards cover the application requirements
		# application_requirements is a list with index 0 - 7, the required points for the 
		# card location is a list between 0 - 9 with the card counts, for example the HAND is a card_counts

		application_can_be_done = False

		# print(f"we are checking application requirements: {application_requirements} against card counts: {card_counts}", file = sys.stderr)

		# first, loop through requirements, decrease with skill cards
		for i in range(len(application_requirements)): # should be 8, but who knows
			application_requirements[i] -= card_counts[i] * 2
			application_requirements[i] = max(application_requirements[i], 0)

		# second, check if we have enough bonus skills to cover them
		if sum(application_requirements) - card_counts[CardType.BONUS.value] <= 0:
			application_can_be_done = True

		# print(f"and the result is: {application_can_be_done}", file = sys.stderr)

		return application_can_be_done



agent = Agent()

# MAIN GAME LOOP
while True:

	game_phase = input()  # can be MOVE, GIVE_CARD, THROW_CARD, PLAY_CARD or RELEASE

	# APPLICATIONS
	applications = []
	applications_count = int(input())
	for i in range(applications_count):
		object_type, _id, training_needed, coding_needed, daily_routine_needed, task_prioritization_needed, architecture_study_needed, continuous_delivery_needed, code_review_needed, refactoring_needed = input().split()
		_id = int(_id)
		training_needed = int(training_needed)
		coding_needed = int(coding_needed)
		daily_routine_needed = int(daily_routine_needed)
		task_prioritization_needed = int(task_prioritization_needed)
		architecture_study_needed = int(architecture_study_needed)
		continuous_delivery_needed = int(continuous_delivery_needed)
		code_review_needed = int(code_review_needed)
		refactoring_needed = int(refactoring_needed)
		application = (_id, [training_needed, coding_needed, daily_routine_needed, task_prioritization_needed, architecture_study_needed, continuous_delivery_needed, code_review_needed, refactoring_needed])
		applications.append(application)

	# PLAYERS
	player_info = {}
	# for i in range(2):
		# player_location: id of the zone in which the player is located
		# player_permanent_daily_routine_cards: number of DAILY_ROUTINE the player has played. It allows them to take cards from the adjacent zones
		# player_permanent_architecture_study_cards: number of ARCHITECTURE_STUDY the player has played. It allows them to draw more cards
	player_location, player_score, player_permanent_daily_routine_cards, player_permanent_architecture_study_cards = [int(j) for j in input().split()]
	other_player_location, other_player_score, other_player_permanent_daily_routine_cards, other_player_permanent_architecture_study_cards = [int(j) for j in input().split()]
	player_info['my_player'] = {'location': player_location, 'score': player_score, 'permanent_daily_routine_cards': player_permanent_architecture_study_cards, 
		'permanent_architecture_study_cards': player_permanent_architecture_study_cards}
	player_info['other_player'] = {'location': other_player_location, 'score': other_player_score, 'permanent_daily_routine_cards': other_player_permanent_daily_routine_cards, 
		'permanent_architecture_study_cards': other_player_permanent_architecture_study_cards}

	# CARD LOCATIONS
	card_locations_count = int(input())
	card_locations = {}
	for i in range(card_locations_count):
		# cards_location: the location of the card list. It can be HAND, DRAW, DISCARD or OPPONENT_CARDS (AUTOMATED and OPPONENT_AUTOMATED will appear in later leagues)
		cards_location, training_cards_count, coding_cards_count, daily_routine_cards_count, task_prioritization_cards_count, architecture_study_cards_count, continuous_delivery_cards_count, code_review_cards_count, refactoring_cards_count, bonus_cards_count, technical_debt_cards_count = input().split()
		training_cards_count = int(training_cards_count)
		coding_cards_count = int(coding_cards_count)
		daily_routine_cards_count = int(daily_routine_cards_count)
		task_prioritization_cards_count = int(task_prioritization_cards_count)
		architecture_study_cards_count = int(architecture_study_cards_count)
		continuous_delivery_cards_count = int(continuous_delivery_cards_count)
		code_review_cards_count = int(code_review_cards_count)
		refactoring_cards_count = int(refactoring_cards_count)
		bonus_cards_count = int(bonus_cards_count)
		technical_debt_cards_count = int(technical_debt_cards_count)
		card_locations[cards_location] = [training_cards_count, coding_cards_count, daily_routine_cards_count, task_prioritization_cards_count, 
			architecture_study_cards_count, continuous_delivery_cards_count, code_review_cards_count, refactoring_cards_count,
			bonus_cards_count, technical_debt_cards_count]

	# POSSIBLE MOVES
	possible_moves_count = int(input())
	possible_moves = []
	for i in range(possible_moves_count):
		possible_move = input()
		possible_moves.append(possible_move)

	game_state = GameState(game_phase, applications, player_info, card_locations, possible_moves)

	command = agent.get_command(game_state)

	print(command)
