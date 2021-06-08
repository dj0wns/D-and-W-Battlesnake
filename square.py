class Square:

  def __init__(self):
    self.set_empty()
    self.snake_distances = {}

  # OCCUPANT INFO
  def set_empty(self):
    self.contains_food = False
    self.contains_snake = None
    self.contains_snake_head = False
    self.distance_to_vacant = 0

  def set_contains_food(self):
    self.contains_food = True
    self.contains_snake = None
    self.contains_snake_head = False
    self.distance_to_vacant = 0

  def set_contains_snake(self, snake_id, distance_to_vacant):
    self.contains_food = False
    self.contains_snake = snake_id
    self.contains_snake_head = False
    self.distance_to_vacant = distance_to_vacant

  def set_contains_snake_head(self, snake_id, distance_to_vacant):
    self.contains_food = False
    self.contains_snake = snake_id
    self.contains_snake_head = True
    self.distance_to_vacant = distance_to_vacant

  # DISTANCE TO VACANT
  def increment_distance_to_vacant(self):
    self.distance_to_vacant += 1

  def decrement_distance_to_vacant(self):
    if self.distance_to_vacant > 0:
      self.distance_to_vacant -= 1

  def is_empty(self):
    return not (self.contains_food or self.contains_snake)

  # SNAKE DISTANCES
  def set_snake_distance(self, snake_id, distance_to_snake):
    self.snake_distances[snake_id] = distance_to_snake

  def clear_snake_distance(self, snake_id):
    if snake_id in self.snake_distances.keys():
      del self.snake_distances[snake_id]

  def clear_snake_distances(self):
    self.snake_distances.clear()

  def get_snake_distance(self, snake_id):
    return self.snake_distances[snake_id] \
        if snake_id in self.snake_distances.keys() else None

  def get_closest_snake(self):
    closest_snake = None
    closest_distance = None
    for snake_id in self.snake_distances.keys():
      distance = self.snake_distances[snake_id]
      if closest_distance is None or distance < closest_distance:
        closest_snake = snake_id
        closest_distance = distance
    return closest_snake
