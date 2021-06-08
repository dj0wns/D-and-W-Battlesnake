import random
import copy

import board

def pick_best_move(board, snake_id):
  # get current location
  x = board.snakes[snake_id]["head"]["x"]
  y = board.snakes[snake_id]["head"]["y"]
  best_score = -1
  chosen_direction = "up"
  i,j = board.get_valid_neighbor_up(snake_id, x, y)
  if i is not None:
    new_board = simulate_board_with_move(board, snake_id, i, j)
    new_board_value = evaluate_board(new_board, snake_id)
    print("up", new_board_value)
    if new_board_value > best_score:
      best_score = new_board_value
      chosen_direction = "up"
  i,j = board.get_valid_neighbor_down(snake_id, x, y)
  if i is not None:
    new_board = simulate_board_with_move(board, snake_id, i, j)
    new_board_value = evaluate_board(new_board, snake_id)
    print("down", new_board_value)
    if new_board_value > best_score:
      best_score = new_board_value
      chosen_direction = "down"
  i,j = board.get_valid_neighbor_left(snake_id, x, y)
  if i is not None:
    new_board = simulate_board_with_move(board, snake_id, i, j)
    new_board_value = evaluate_board(new_board, snake_id)
    print("left", new_board_value)
    if new_board_value > best_score:
      best_score = new_board_value
      chosen_direction = "left"
  i,j = board.get_valid_neighbor_right(snake_id, x, y)
  if i is not None:
    new_board = simulate_board_with_move(board, snake_id, i, j)
    new_board_value = evaluate_board(new_board, snake_id)
    print("right", new_board_value)
    if new_board_value > best_score:
      best_score = new_board_value
      chosen_direction = "right"
  return chosen_direction

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
