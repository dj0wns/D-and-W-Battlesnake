import square
import queue

class Board:
  def __init__(self):
    self.width = -1
    self.height = -1
    self.food = []
    self.snakes = []
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
        if i == 0:
          self.squares[body["x"]][body["y"]].set_contains_snake_head(snake["id"], snake["length"])
        else:
          self.squares[body["x"]][body["y"]].set_contains_snake(snake["id"], snake["length"])

  def __str__(self):
    string = ( f"Width: {self.width}\n"
               f"Height: {self.height}\n"
               f"Food: {self.food}\n" )
    x = 0
    for column in self.squares:
      y = 0
      for square in column:
        string += f"[{x},{y}] {square}\n"
        y += 1
      x += 1
    return string

  # NAVIGATION
  def is_valid_destination(self, snake_id, coordinates):

    # check if coordinates are out of bounds
    x, y = coordinates
    if x < 0 or y < 0 or x >= self.width or y >= self.height:
      return False

    # check if square contains snake
    square = self.squares[x][y]
    if square.contains_snake is not None:
      # check if square contains head of larger/equal snake
      if square.contains_snake_head:
        # TODO: store self.snakes as dictionary with snake_id as keys
        our_snake_length = 0 # TODO
        their_snake_length = 0 # TODO
        if their_snake_length >= our_snake_length:
          return False
      else:
        return False

    return True

  def get_valid_neighbor_up(self, snake_id, x, y):
    neighbor = (x, y+1)
    return neighbor if self.is_valid_destination(snake_id, neighbor) \
        else (None, None)

  def get_valid_neighbor_down(self, snake_id, x, y):
    neighbor = (x, y-1)
    return neighbor if self.is_valid_destination(snake_id, neighbor) \
        else (None, None)

  def get_valid_neighbor_left(self, snake_id, x, y):
    neighbor = (x-1, y)
    return neighbor if self.is_valid_destination(snake_id, neighbor) \
        else (None, None)

  def get_valid_neighbor_right(self, snake_id, x, y):
    neighbor = (x+1, y)
    return neighbor if self.is_valid_destination(snake_id, neighbor) \
        else (None, None)
  
  def calculate_snakes_distances(self):
    for snake in self.snakes.values():
      #init queue
      bfs_queue = queue.SimpleQueue()
      depth = 1
      #breath first search for each snake
      starting_x = snake["head"]["x"]
      starting_y = snake["head"]["y"]
      # TODO touches every square at least twice when backtracking
      x, y = self.get_valid_neighbor_up(snake["id"], starting_x, starting_y)
      if x is not None:
        bfs_queue.put({"x":x, "y":y, "depth":1})
      x, y = self.get_valid_neighbor_down(snake["id"], starting_x, starting_y)
      if x is not None:
        bfs_queue.put({"x":x, "y":y, "depth":1})
      x, y = self.get_valid_neighbor_left(snake["id"], starting_x, starting_y)
      if x is not None:
        bfs_queue.put({"x":x, "y":y, "depth":1})
      x, y = self.get_valid_neighbor_right(snake["id"], starting_x, starting_y)
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
          x, y = self.get_valid_neighbor_up(snake["id"], current_item["x"], current_item["y"])
          if x is not None:
            bfs_queue.put({"x":x, "y":y, "depth":current_item["depth"]+1})
          x, y = self.get_valid_neighbor_down(snake["id"], current_item["x"], current_item["y"])
          if x is not None:
            bfs_queue.put({"x":x, "y":y, "depth":current_item["depth"]+1})
          x, y = self.get_valid_neighbor_left(snake["id"], current_item["x"], current_item["y"])
          if x is not None:
            bfs_queue.put({"x":x, "y":y, "depth":current_item["depth"]+1})
          x, y = self.get_valid_neighbor_right(snake["id"], current_item["x"], current_item["y"])
          if x is not None:
            bfs_queue.put({"x":x, "y":y, "depth":current_item["depth"]+1})

