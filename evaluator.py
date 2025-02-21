import copy
import itertools
import random
import time
from collections import Counter

import board

BUCKETS = ["normal", "risky_in_3", "risky_in_2", "risky_in_1", "death_in_1", "invalid"]
STEP = 1 # Might want deeper steps in future


def pick_best_move(board, snake_id, time_allotted):
  start = time.time_ns()
  # initialize buckets
  bucketed_moves = {}
  for bucket in BUCKETS:
    bucketed_moves[bucket] = {}

  # bucketize each move
  for move in board.MOVES.keys():
    bucket, x, y = bucketize_move(move, board, snake_id)
    bucketed_moves[bucket][move] = {"x": x, "y": y}

  # find top bucket with moves
  best_bucket = BUCKETS[-1]
  for bucket in BUCKETS:
    if bucketed_moves[bucket]:
      best_bucket = bucket
      break

  #print(best_bucket, bucketed_moves[bucket])
  # only invalid moves
  if best_bucket == BUCKETS[-1]:
    #print("No valid moves.")
    return random.choice(list(board.MOVES.keys()))

  # only one best move
  elif len(bucketed_moves[best_bucket]) == 1:
    #TODO replace with better code (functionally this is equivalent though)
    for key in bucketed_moves[best_bucket].keys():
      return key

  # find best scoring move
  else:
    other_snake_destinations = list_valid_other_snake_destinations(board, snake_id)

    # initialize worst scores per move
    worst_scores = {}
    for move in bucketed_moves[best_bucket].keys():
      worst_scores[move] = None

    # simulate each move, keeping track of current worst score before time out
    time_out = False
    for i in range(0, len(other_snake_destinations), STEP):
      for move, destination in bucketed_moves[best_bucket].items():
        score = evaluate_destination(destination, board, snake_id, other_snake_destinations, i, i+STEP)
        if worst_scores[move] is None or score < worst_scores[move]:
          worst_scores[move] = score
        elapsed_time = time.time_ns() - start
        if elapsed_time >= time_allotted:
          time_out = True
          break
      if time_out:
        break
    #print(f"Executed {i} simulations in {elapsed_time/1000000} ms")

    # find best of the worst scores per move
    best_score = -1
    best_moves = []
    for move, score in worst_scores.items():
      if score is not None and score > best_score:
        best_score = score
        best_moves = [move]
      elif score is not None and score == best_score:
        best_moves.append(move)

    return random.choice(best_moves)


def list_valid_other_snake_destinations(board, snake_id_to_ignore):
  destinations = []
  for snake_id in board.snakes:
    snake_destinations = []
    if snake_id == snake_id_to_ignore:
      continue
    for move in board.MOVES.keys():
      x, y = board.get_valid_neighbor(
          move,
          snake_id,
          board.snakes[snake_id]["head"]["x"],
          board.snakes[snake_id]["head"]["y"])
      if x is None:
        continue
      snake_destinations.append({snake_id: {"x":x, "y":y}})
    destinations.append(snake_destinations)
    #TODO if snake_destinations is valid, add a random in-bounds move
  return list(itertools.product(*destinations))

def bucketize_move(move, board, snake_id):

  # get destination
  x, y = board.get_valid_neighbor(
      move,
      snake_id,
      board.snakes[snake_id]["head"]["x"],
      board.snakes[snake_id]["head"]["y"])

  bucket = "normal"

  # check if destination valid
  if x is None:
    bucket = "invalid"

  # check riskiness
  else:
    #simulate board with only us moving for riskiness calculation
    new_board = \
        simulate_possible_next_board(board, {snake_id: { "x":x, "y":y }})
    turns_until_risky = check_turns_until_risky(new_board, snake_id)
    if turns_until_risky == 0:
      bucket = "death_in_1"
    if turns_until_risky == 1:
      bucket = "risky_in_1"
    elif turns_until_risky == 2:
      bucket = "risky_in_2"
    elif turns_until_risky  == 3:
      bucket = "risky_in_3"

  return bucket, x, y


def evaluate_destination(destination, board, snake_id, other_snake_destinations, osd_start_index, osd_stop_index):
  worst_score = None
  for i in range(osd_start_index, osd_stop_index):
    destinations = {}
    #TODO replace with better code. other_snake_destinations is a list of tuples of dicts, kind of a weird data format
    for other_snake_destination in other_snake_destinations[i]:
      for snake_dest_id in other_snake_destination.keys():
        destinations[snake_dest_id] = other_snake_destination[snake_dest_id]
    destinations[snake_id] = destination
    new_board = simulate_possible_next_board(board, destinations)
    new_board_value = evaluate_board(board, new_board, snake_id)

    # see if we are the worst board state discovered
    if worst_score is None or worst_score > new_board_value:
      worst_score = new_board_value

  # if there are no other snakes (e.g. challenge mission)
  if worst_score is None:
    destinations = {}
    destinations[snake_id] = destination
    new_board = simulate_possible_next_board(board, destinations)
    worst_score = evaluate_board(board, new_board, snake_id)

  return worst_score


# makes a new representation of the board if the given snake moved to the given square
# TODO move other snakes aswell, we are moving their tails but not their heads
# TODO account for picking up food for other snakes
# TODO tree: this should take all snakes new destinations (dict of snake_id: (coordinate))
# TODO: when branching other snakes' possible moves, if only invalid moves available, force move to be in bounds
def simulate_possible_next_board(board, snake_destinations):

  new_board = board.simulation_copy()

  dead_snakes = set()

  # apply each snake's move
  for snake_id, head in snake_destinations.items():
    x = head["x"]
    y = head["y"]

    # update head
    new_board.snakes[snake_id]["head"] = head
    # update new body list to new head + all but old tail
    new_board.snakes[snake_id]["body"] = \
        [head] + new_board.snakes[snake_id]["body"][:-1]

    # update square for new head
    self_collision = new_board.squares[x][y].add_snake(
        snake_id, new_board.snakes[snake_id]["length"], True)

    if self_collision:
      dead_snakes.add(snake_id)

    # reduce health
    new_board.snakes[snake_id]["health"] -= 1

    # if snake ate food
    if board.squares[x][y].contains_food:

      # increment each snake segment's distance to vacant
      for segment in new_board.snakes[snake_id]["body"]:
        new_board.squares[segment["x"]][segment["y"]]\
            .increment_distance_to_vacant(snake_id)
      # add newly grown tail on top of current tail in body list
      new_board.snakes[snake_id]["body"].append(
          new_board.snakes[snake_id]["body"][-1])
      # increment snake length
      new_board.snakes[snake_id]["length"] += 1

      # reset health
      new_board.snakes[snake_id]["health"] = 100

      # remove from food list
      try:
        new_board.food.remove(head)
      except ValueError:
        pass

  for snake_id, head in snake_destinations.items():
    if snake_id in dead_snakes:
      continue

    # if snake is out of health
    if new_board.snakes[snake_id]["health"] <= 0:
      dead_snakes.add(snake_id)
      continue

    snake_heads = new_board.squares[head["x"]][head["y"]].get_snake_heads()
    # if head on head collision
    if len(snake_heads) > 1:
      current_snake_len = new_board.snakes[snake_id]["length"]
      for snake_head_id in snake_heads:
        # ignore our own snake, so we don't eat ourselves <3
        if snake_head_id != snake_id:
          # If we are shorter or equal to the other snake we ded
          if new_board.snakes[snake_head_id]["length"] >= current_snake_len:
            dead_snakes.add(snake_id)
          # If we are longer or equal to the other snake they ded
          if new_board.snakes[snake_head_id]["length"] <= current_snake_len:
            dead_snakes.add(snake_head_id)

    # if head on body collision
    elif len(new_board.squares[head["x"]][head["y"]].get_snakes()) > 1:
      dead_snakes.add(snake_id)

  # remove all dead snakes from board and squares
  for snake_id in dead_snakes:
    for body in new_board.snakes[snake_id]["body"]:
      new_board.squares[body["x"]][body["y"]].remove_snake("snake_id")
    del new_board.snakes[snake_id]

  snakes_with_destinations = list(snake_destinations.keys())
  snake_ids = list(new_board.snakes.keys())
  snakes_to_decrement = list((Counter(snakes_with_destinations) - Counter(snake_ids)).elements())
  new_board.calculate_snakes_distances(snakes_to_decrement)

  return new_board


def evaluate_board(original_board, board, snake_id):
  #count how many squares we would be able to get to first
  # TODO check for why we sometimews seem to ignore food at low hp
  # TODO account for ties and snake length to determine who really owns the square
  if snake_id not in board.snakes.keys():
    return -1
  move_score = 0
  closest_square_count = 0
  for column in board.squares:
    for square in column:
      closest_snakes = square.get_closest_snake()
      if snake_id in closest_snakes:
        if len(closest_snakes) == 1 or board.get_largest_snakes(closest_snakes) == snake_id:
          closest_square_count += 1
  move_score = closest_square_count
  # Adjust for hunger
  # see if our snake would have eaten this turn
  ate_food = False
  for food in original_board.food:
    if food["x"] == board.snakes[snake_id]["head"]["x"] and food["y"] == board.snakes[snake_id]["head"]["y"]:
      ate_food = True
  original_food_distance = original_board.get_distance_to_closest_owned_food(snake_id)
  new_food_distance = board.get_distance_to_closest_owned_food(snake_id)
  if ate_food or (original_food_distance is not None and new_food_distance is not None):
    if ate_food or new_food_distance < original_food_distance:
      # add factor to lightly encourage our snake to go towards the food
      # max hunger minus current hunger divided by a constant is a good simple way to account for this
      # if a new closer food is spawned out of nowhere it doesnt really affect anything
      if board.snakes[snake_id]["health"] > 30:
        move_score += 0.5
      else:
        move_score += (30 - board.snakes[snake_id]["health"])
  return move_score


def check_turns_until_risky(board, snake_id):
  turns_until_risky = 0 # extremely risky!
  for column in board.squares:
    for square in column:
      closest_snakes = square.get_closest_snake()
      if snake_id in closest_snakes:
        if len(closest_snakes) == 1 or \
            board.get_largest_snakes(closest_snakes) == snake_id:
          if turns_until_risky < square.get_snake_distance(snake_id):
            turns_until_risky = square.get_snake_distance(snake_id)
  return turns_until_risky

