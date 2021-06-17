from copy import deepcopy
import square
import queue

class Board:

  def __init__(self):
    self.MOVES = {
      "up": self.get_valid_neighbor_up,
      "down": self.get_valid_neighbor_down,
      "left": self.get_valid_neighbor_left,
      "right": self.get_valid_neighbor_right,
    }
    self.width = -1
    self.height = -1
    self.food = []
    self.snakes = {}
    self.squares = []

  def parse_board(self, data):
    self.width = data["width"]
    self.height = data["height"]
    self.food = data["food"]
    self.snakes = {}
    for snake in data["snakes"]: 
      self.snakes[snake["id"]] = snake
    self.squares = []
    for i in range(self.width):
      column = []
      for j in range(self.height):
        column.append(square.Square())
      self.squares.append(column)
    
    for food in self.food:
      self.squares[food["x"]][food["y"]].set_contains_food()

    for snake in self.snakes.values():
      for i in range(snake["length"]):
        body = snake["body"][i]
        self.squares[body["x"]][body["y"]].add_snake(
            snake["id"], snake["length"]-i, i==0)

  def __str__(self):
    string = ( f"Width: {self.width}\n"
               f"Height: {self.height}\n"
               f"Food: {self.food}\n" 
               f"Snakes: {self.snakes}\n" )
    x = 0
    for column in self.squares:
      y = 0
      for square in column:
        string += f"[{x},{y}] {square}\n"
        y += 1
      x += 1
    return string

  # NAVIGATION
  def is_valid_destination(self, snake_id, coordinates, distance):

    # check if coordinates are out of bounds
    x, y = coordinates
    if x < 0 or y < 0 or x >= self.width or y >= self.height:
      return False

    # check if square contains snake
    square = self.squares[x][y]
    if square.snakes:
      if square.longest_distance_to_vacant() > distance:
        return False
    return True

  def get_valid_neighbor(self, move, snake_id, x, y, distance=1):
    return self.MOVES[move](snake_id, x, y, distance)

  def get_valid_neighbor_up(self, snake_id, x, y, distance=1):
    neighbor = (x, y+1)
    return neighbor if self.is_valid_destination(snake_id, neighbor, distance) \
        else (None, None)

  def get_valid_neighbor_down(self, snake_id, x, y, distance=1):
    neighbor = (x, y-1)
    return neighbor if self.is_valid_destination(snake_id, neighbor, distance) \
        else (None, None)

  def get_valid_neighbor_left(self, snake_id, x, y, distance=1):
    neighbor = (x-1, y)
    return neighbor if self.is_valid_destination(snake_id, neighbor, distance) \
        else (None, None)

  def get_valid_neighbor_right(self, snake_id, x, y, distance=1):
    neighbor = (x+1, y)
    return neighbor if self.is_valid_destination(snake_id, neighbor, distance) \
        else (None, None)

  def get_largest_snakes(self, snake_ids):
    max_length = 0
    long_snakes = []
    for snake_id in snake_ids:
      if self.snakes[snake_id]["length"] > max_length:
        max_length = self.snakes[snake_id]["length"]
        long_snakes = [snake_id]
      else:
        long_snakes.append(snake_id)
    return long_snakes

  def simulation_copy(self):
    copy = type(self)()

    copy.width = self.width
    copy.height = self.height
    copy.food = deepcopy(self.food)
    copy.snakes = deepcopy(self.snakes)

    copy.squares = []
    for column in self.squares:
      column_copy = []
      for square in column:
        column_copy.append(square.simulation_copy())
      copy.squares.append(column_copy)

    return copy

  def get_distance_to_closest_owned_food(self, snake_id):
    closest_food_distance = None
    for food in self.food:
      x = food["x"]
      y = food["y"]
      closest_snakes = self.squares[x][y].get_closest_snake()
      if snake_id in closest_snakes:
        if len(closest_snakes) == 1 or self.get_largest_snakes(closest_snakes) == snake_id:
          distance = self.squares[x][y].get_snake_distance(snake_id)
          if closest_food_distance is None or distance < closest_food_distance:
            closest_food_distance = distance
    return closest_food_distance
  
  def calculate_snakes_distances(self, snakes_to_decrement=[]):
    for snake in self.snakes.values():
      #init queue
      bfs_queue = queue.SimpleQueue()
      #breath first search for each snake
      starting_x = snake["head"]["x"]
      starting_y = snake["head"]["y"]
      starting_distance = 1
      # Decrement the starting values of given snakes to simulate if they had moved in every possible direction the previous turn
      if snake["id"] in snakes_to_decrement:
        starting_distance = 0
      # TODO touches every square at least twice when backtracking
      x, y = self.get_valid_neighbor_up(snake["id"], starting_x, starting_y, starting_distance)
      if x is not None:
        bfs_queue.put({"x":x, "y":y, "depth":1})
      x, y = self.get_valid_neighbor_down(snake["id"], starting_x, starting_y, starting_distance)
      if x is not None:
        bfs_queue.put({"x":x, "y":y, "depth":1})
      x, y = self.get_valid_neighbor_left(snake["id"], starting_x, starting_y, starting_distance)
      if x is not None:
        bfs_queue.put({"x":x, "y":y, "depth":1})
      x, y = self.get_valid_neighbor_right(snake["id"], starting_x, starting_y, starting_distance)
      if x is not None:
        bfs_queue.put({"x":x, "y":y, "depth":1})
      # execute queue
      while not bfs_queue.empty():
        current_item = bfs_queue.get()
        current_square = self.squares[current_item["x"]][current_item["y"]]
        last_distance = current_square.get_snake_distance(snake["id"])
        if last_distance is None:
          current_square.set_snake_distance(snake["id"], current_item["depth"])
          # now add children to the queue
          x, y = self.get_valid_neighbor_up(snake["id"], current_item["x"], current_item["y"], current_item["depth"]+1)
          if x is not None:
            bfs_queue.put({"x":x, "y":y, "depth":current_item["depth"]+1})
          x, y = self.get_valid_neighbor_down(snake["id"], current_item["x"], current_item["y"], current_item["depth"]+1)
          if x is not None:
            bfs_queue.put({"x":x, "y":y, "depth":current_item["depth"]+1})
          x, y = self.get_valid_neighbor_left(snake["id"], current_item["x"], current_item["y"], current_item["depth"]+1)
          if x is not None:
            bfs_queue.put({"x":x, "y":y, "depth":current_item["depth"]+1})
          x, y = self.get_valid_neighbor_right(snake["id"], current_item["x"], current_item["y"], current_item["depth"]+1)
          if x is not None:
            bfs_queue.put({"x":x, "y":y, "depth":current_item["depth"]+1})

