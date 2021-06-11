class Square:

  def __init__(self):
    self.set_empty()
    self.snake_distances = {}

  def __str__(self):
    string = ( f"contains_food: {self.contains_food}\n"
               f"contains_snake: {self.contains_snake}\n"
               f"contains_snake_head: {self.contains_snake_head}\n"
               f"distance_to_vacant: {self.distance_to_vacant}\n"
               f"snake_distances: {self.snake_distances}\n" )
    return string

  # TODO: move this to custom function here and in board class instead of changing deepcopy
  # this is called when simulating a new board state
  #   should clear heads (handled in later step)
  #   should automatically move tail forward
  #   should clear snake distances (handled in later step)
  def __deepcopy__(self, memo):
    copy = type(self)()

    copy.contains_food = self.contains_food
    copy.contains_snake = self.contains_snake
    copy.distance_to_vacant = self.distance_to_vacant - 1 if self.distance_to_vacant else 0

    return copy

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
    if distance_to_vacant > self.distance_to_vacant:
      # special case to handle how the snake is stacked in the beginning
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
    self.contains_snake_head = False
    if self.distance_to_vacant == 0:
      self.contains_snake = None

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
    closest_snake = []
    closest_distance = None
    for snake_id in self.snake_distances.keys():
      distance = self.snake_distances[snake_id]
      if closest_distance is None or distance < closest_distance:
        closest_snake = [snake_id]
        closest_distance = distance
      elif distance == closest_distance:
        closest_snake.append(snake_id)
    return closest_snake
