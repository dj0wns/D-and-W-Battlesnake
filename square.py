class Square:

  def __init__():
    self.set_empty()
    self.snake_distances = {}

  # OCCUPANT INFO
  def set_empty():
    self.contains_food = False
    self.contains_snake = None
    self.contains_snake_head = False
    self.distance_to_empty = 0

  def set_contains_food():
    self.contains_food = True
    self.contains_snake = None
    self.contains_snake_head = False
    self.distance_to_empty = 0

  def set_contains_snake(snake_id, distance_to_empty):
    self.contains_food = False
    self.contains_snake = snake_id
    self.contains_snake_head = False
    self.distance_to_empty = distance_to_empty

  def set_contains_snake_head(snake_id, distance_to_empty):
    self.contains_food = False
    self.contains_snake = snake_id
    self.contains_snake_head = True
    self.distance_to_empty = distance_to_empty

  # DISTANCE TO EMPTY
  def increment_distance_to_empty():
    self.distance_to_empty += 1

  def decrement_distance_to_empty():
    if self.distance_to_empty > 0:
      self.distance_to_empty -= 1

  # SNAKE DISTANCES
  def set_distance_to_snake(snake_id, distance_to_snake):
    self.snake_distances[snake_id] = distance_to_snake

  def clear_distance_to_snake(snake_id):
    if snake_id in self.snake_distances.keys():
      del self.snake_distances[snake_id]

  def clear_snake_distances():
    self.snake_distances.clear()

  def get_distance_to_snake(snake_id):
    if snake_id in self.snake_distances.keys():
      return self.snake_distances[snake_id]
    else
      return None

  def get_closest_snake():
    closest_snake = None
    closest_distance = None
    for snake_id in self.snake_distances.keys():
      distance = self.snake_distances[snake_id]
      if closest_distance is None or distance < closest_distance:
        closest_snake = snake_id
        distance = closest_distance
    return snake_id
