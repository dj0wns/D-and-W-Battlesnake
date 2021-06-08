import random

import board

def pick_best_move(board, snake_id):
  # get current location
  x = board.snakes[snake_id]["head"]["x"]
  y = board.snakes[snake_id]["head"]["y"]
  valid_directions = []
  i,j = board.get_valid_neighbor_up(snake_id, x, y)
  if i is not None:
    valid_directions.append("up")
  i,j = board.get_valid_neighbor_down(snake_id, x, y)
  if i is not None:
    valid_directions.append("down")
  i,j = board.get_valid_neighbor_left(snake_id, x, y)
  if i is not None:
    valid_directions.append("left")
  i,j = board.get_valid_neighbor_right(snake_id, x, y)
  if i is not None:
    valid_directions.append("right")
  move = random.choice(valid_directions)
  return move

def evaluate_board(board, snake_id):
  
  return 0
