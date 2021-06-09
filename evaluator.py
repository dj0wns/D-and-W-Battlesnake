import random
import copy

import board

def pick_best_move(board, snake_id):
  # get current location
  x = board.snakes[snake_id]["head"]["x"]
  y = board.snakes[snake_id]["head"]["y"]
  best_score = -1
  best_risky_score = -1 #risky means that there is a chance we will run into the head of an equal or larger snake
  chosen_direction = ""
  chosen_risky_direction = ""
  
  i,j = board.get_valid_neighbor_up(snake_id, x, y)
  if i is not None:
    new_board = simulate_board_with_move(board, snake_id, i, j)
    new_board_value = evaluate_board(new_board, snake_id)
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
    new_board_value = evaluate_board(new_board, snake_id)
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
    new_board_value = evaluate_board(new_board, snake_id)
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
    new_board_value = evaluate_board(new_board, snake_id)
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
# TODO move other snakes aswell
def simulate_board_with_move(board, snake_id, x, y):
  new_board = copy.deepcopy(board)
  # decrement all squares  
  for column in new_board.squares:
    for square in column:
      square.decrement_distance_to_vacant()
      square.clear_snake_distances()
  new_board.snakes[snake_id]["head"]["x"] = x
  new_board.snakes[snake_id]["head"]["y"] = y
  new_board.squares[x][y].set_contains_snake_head(snake_id, new_board.snakes[snake_id]["length"])
  new_board.calculate_snakes_distances()
  return new_board

def evaluate_board(board, snake_id):
  #count how many squares we would be able to get to first
  closest_square_count = 0
  for column in board.squares:
    for square in column:
      if square.get_closest_snake() == snake_id:
        closest_square_count += 1
  return closest_square_count

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
