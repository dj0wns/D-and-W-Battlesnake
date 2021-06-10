import random
import copy

import board

def pick_best_move(board, snake_id):
  # get current location
  x = board.snakes[snake_id]["head"]["x"]
  y = board.snakes[snake_id]["head"]["y"]
  best_score = -1
  best_risky_score = -1 #risky means that there is a chance we will run into the head of an equal or larger snake
  # TODO track list of best directions that tie and return random of them
  chosen_direction = ""
  chosen_risky_direction = ""
  
  # TODO clean this up, it's almost the same thing 4x
  i,j = board.get_valid_neighbor_up(snake_id, x, y)
  if i is not None:
    new_board = simulate_board_with_move(board, snake_id, i, j)
    new_board_value = evaluate_board(board, new_board, snake_id)
    risky = check_if_adjacent_longer_enemy_head(board, snake_id, i, j)
    print("up", new_board_value, risky)
    if risky:
      if new_board_value > best_risky_score:
        best_risky_score = new_board_value
        chosen_risky_direction = "up"
    else:
      if new_board_value > best_score:
        best_score = new_board_value
        chosen_direction = "up"
  
  i,j = board.get_valid_neighbor_down(snake_id, x, y)
  if i is not None:
    new_board = simulate_board_with_move(board, snake_id, i, j)
    new_board_value = evaluate_board(board, new_board, snake_id)
    risky = check_if_adjacent_longer_enemy_head(board, snake_id, i, j)
    print("down", new_board_value, risky)
    if risky:
      if new_board_value > best_risky_score:
        best_risky_score = new_board_value
        chosen_risky_direction = "down"
    else:
      if new_board_value > best_score:
        best_score = new_board_value
        chosen_direction = "down"
  
  i,j = board.get_valid_neighbor_left(snake_id, x, y)
  if i is not None:
    new_board = simulate_board_with_move(board, snake_id, i, j)
    new_board_value = evaluate_board(board, new_board, snake_id)
    risky = check_if_adjacent_longer_enemy_head(board, snake_id, i, j)
    print("left", new_board_value, risky)
    if risky:
      if new_board_value > best_risky_score:
        best_risky_score = new_board_value
        chosen_risky_direction = "left"
    else:
      if new_board_value > best_score:
        best_score = new_board_value
        chosen_direction = "left"
  
  i,j = board.get_valid_neighbor_right(snake_id, x, y)
  if i is not None:
    new_board = simulate_board_with_move(board, snake_id, i, j)
    new_board_value = evaluate_board(board, new_board, snake_id)
    risky = check_if_adjacent_longer_enemy_head(board, snake_id, i, j)
    print("right", new_board_value, risky)
    if risky:
      if new_board_value > best_risky_score:
        best_risky_score = new_board_value
        chosen_risky_direction = "right"
    else:
      if new_board_value > best_score:
        best_score = new_board_value
        chosen_direction = "right"

  if chosen_direction:
    return chosen_direction
  else:
    return chosen_risky_direction

# makes a new representation of the board if the given snake moved to the given square
# TODO move other snakes aswell, we are moving their tails but not their heads
# TODO account for picking up food for either us or other snakes
# TODO account for head on collisions
def simulate_board_with_move(board, snake_id, x, y):
  new_board = copy.deepcopy(board)
  # decrement all squares  
  # TODO potentially move this logic to the square.__deepcpy__() function so they are only touched once.
  for column in new_board.squares:
    for square in column:
      square.decrement_distance_to_vacant()
      square.clear_snake_distances()
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
      if closest_snakes.contains(snake_id):
        if len(closest_snakes) == 1 or self.get_largest_snakes(closest_snakes) == snake_id:
          closest_square_count += 1
  move_score = closest_square_count
  # Adjust for hunger
  original_food_distance = original_board.get_distance_to_closest_owned_food(snake_id)
  new_food_distance = board.get_distance_to_closest_owned_food(snake_id)
  if original_food_distance is not None and new_food_distance is not None:
    if new_food_distance < original_food_distance:
      # add factor to lightly encourage our snake to go towards the food
      # max hunger minus current hunger divided by a constant is a good simple way to account for this
      # if a new closer food is spawned out of nowhere it doesnt really affect anything
      move_score += (100 - board.snakes[snake_id]["health"])/2
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
