class Square:

  def __init__(self):
    self.set_empty()
    self.snake_distances = {}

  def __str__(self):
    string = f"contains_food: {self.contains_food}\n"
    for snake_id, snake in self.snakes.items():
      string += ( f"\tsnake_id: {snake_id}\n"
                  f"\t\tdistance_to_vacant: {snake['distance_to_vacant']}\n"
                  f"\t\thead: {snake['head']}\n" )
    return string

  # This is called when simulating a new board state
  #   Keep track of whether or not there was food
  #   Keep track of snakes
  #   Clear snake distances (handled by never being set)
  #   Move tail forward and clear heads (handled by decrement distance to vacant)
  def simulation_copy(self):
    copy = type(self)()

    copy.contains_food = self.contains_food
    copy.snakes = self.snakes
    copy.decrement_distance_to_vacant()

    return copy

  # OCCUPANT INFO
  def set_empty(self):
    self.contains_food = False
    self.snakes = {}

  def set_contains_food(self):
    self.contains_food = True
    self.snakes = {}

  def add_snake(self, snake_id, distance_to_vacant, head=False):
    # only set if new snake or new distance_to_vacant is greater
    self_collision = snake_id in self.snakes.keys()
    if not self_collision \
        or distance_to_vacant > self.snakes[snake_id]["distance_to_vacant"]:
      self.contains_food = False
      self.snakes[snake_id] = {
          "distance_to_vacant": distance_to_vacant,
          "head": head,
        }
    return self_collision

  def remove_snake(self, snake_id):
    try:
      del self.snakes[snake_id]
    except KeyError:
      print(f"Tried to remove snake ({snake_id}) from square it is not in")

  def get_snakes(self):
    return self.snakes.keys()

  def get_snake_heads(self):
    heads = []
    for snake_id, snake in self.snakes.items():
      if snake["head"]:
        heads.append(snake_id)
    return heads

  # DISTANCE TO VACANT
  def longest_distance_to_vacant(self):
    longest_distance = 0
    for snake in self.snakes.values():
      if snake["distance_to_vacant"] > longest_distance:
        longest_distance = snake["distance_to_vacant"]
    return longest_distance

  def increment_distance_to_vacant(self, snake_id):
    self.snakes[snake_id]["distance_to_vacant"] += 1

  def decrement_distance_to_vacant(self):
    for snake in self.snakes.values():
      snake["distance_to_vacant"] -= 1
      snake["head"] = False
      if snake["distance_to_vacant"] <= 0:
        del snake

  def is_empty(self):
    return not (self.contains_food or self.snakes)

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
