import random
import copy

import board

BUCKETS = ["normal", "risky"]


def check_turns_until_risky(board, snake_id, x, y):
  turns_until_risky = 0 # no foreseen riskiness
  if check_if_adjacent_longer_enemy_head(board, snake_id, x, y):
    turns_until_risky = 1
  return turns_until_risky


def bucketize_move(move, best_moves, board, snake_id):

  x, y = board.get_valid_neighbor(
      move,
      snake_id,
      board.snakes[snake_id]["head"]["x"],
      board.snakes[snake_id]["head"]["y"])
  bucket = "normal"

  # if valid move
  if x is not None:
    new_board = simulate_board_with_move(board, snake_id, x, y)
    new_board_value = evaluate_board(board, new_board, snake_id)

    # check riskiness
    turns_until_risky = check_turns_until_risky(board, snake_id, x, y)
    if turns_until_risky:
      bucket = "risky"

    # check if move is better
    if new_board_value > best_moves[bucket]["score"]:
      best_moves[bucket]["score"] = new_board_value
      best_moves[bucket]["moves"] = [move]
    elif new_board_value == best_moves[bucket]["score"]:
      best_moves[bucket]["moves"].append(move)


def pick_best_move(board, snake_id):
  best_moves = {
    "normal": {
      "score": -1,
      "moves": [],
    },
    "risky": {
      "score": -1,
      "moves": [],
    },
  }
  for move in board.MOVES.keys():
    bucketize_move(move, best_moves, board, snake_id)
  
  # return move from best bucket
  for bucket in BUCKETS:
    if best_moves[bucket]["moves"]:
      return random.choice(best_moves[bucket]["moves"])
  print("No valid moves.")
  return random.choice(board.MOVES.keys())


# makes a new representation of the board if the given snake moved to the given square
# TODO move other snakes aswell, we are moving their tails but not their heads
# TODO account for picking up food for other snakes
# TODO account for head on collisions
def simulate_board_with_move(board, snake_id, x, y):
  # Cache tail object so we can add it in after the copy to represent eating food
  ate_food = False
  new_tail_x = -1
  new_tail_y = -1
  if board.squares[x][y].contains_food:
    #we at food!
    ate_food = True
    new_tail_x = board.snakes[snake_id]["body"][-1]["x"]
    new_tail_y = board.snakes[snake_id]["body"][-1]["y"]

  new_board = copy.deepcopy(board)
  # decrement all squares  
  # TODO potentially move this logic to the square.__deepcpy__() function so they are only touched once.
  for column in new_board.squares:
    for square in column:
      square.decrement_distance_to_vacant()
      square.clear_snake_distances()
  if ate_food:
    # add to body and increase length by 1 and then increment all other body parts
    new_board.snakes[snake_id]["length"] += 1
    new_board.squares[new_tail_x][new_tail_y].set_contains_snake(snake_id, 1)
    for cell in new_board.snakes[snake_id]["body"]:
      new_board.squares[cell["x"]][cell["y"]].increment_distance_to_vacant()
    new_board.snakes[snake_id]["body"].append({"x":new_tail_x, "y":new_tail_y})

  new_board.snakes[snake_id]["head"]["x"] = x
  new_board.snakes[snake_id]["head"]["y"] = y
  new_board.squares[x][y].set_contains_snake_head(snake_id, new_board.snakes[snake_id]["length"])
  new_board.calculate_snakes_distances()
  return new_board

def evaluate_board(original_board, board, snake_id):
  #count how many squares we would be able to get to first
  # TODO account for ties and snake length to determine who really owns the square
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

def check_if_adjacent_longer_enemy_head(board, snake_id, x, y):
  if x > 0 and board.squares[x-1][y].contains_snake_head:
    new_snake_id = board.squares[x-1][y].contains_snake
    if snake_id != new_snake_id and board.snakes[snake_id]["length"] <= board.snakes[new_snake_id]["length"]:
      return True
  if y > 0 and board.squares[x][y-1].contains_snake_head:
    new_snake_id = board.squares[x][y-1].contains_snake
    if snake_id != new_snake_id and board.snakes[snake_id]["length"] <= board.snakes[new_snake_id]["length"]:
      return True
  if x < board.width - 1 and board.squares[x+1][y].contains_snake_head:
    new_snake_id = board.squares[x+1][y].contains_snake
    if snake_id != new_snake_id and board.snakes[snake_id]["length"] <= board.snakes[new_snake_id]["length"]:
      return True
  if y < board.height - 1 and board.squares[x][y+1].contains_snake_head:
    new_snake_id = board.squares[x][y+1].contains_snake
    if snake_id != new_snake_id and board.snakes[snake_id]["length"] <= board.snakes[new_snake_id]["length"]:
      return True
  return False
