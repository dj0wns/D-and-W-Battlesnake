import square

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
    self.snakes = data["snakes"]
    self.squares = []
    for i in range(self.width):
      column = []
      for j in range(self.height):
        column.append(square.Square())
      self.squares.append(column)
    
    for food in self.food:
      squares[food["x"]][food["y"]].set_contains_food()

    for snake in self.snakes:
      for i in range(snake["body"]):
        body = snake["body"][i]
        if i == 0:
          squares[body["x"]][body["y"]].set_contains_snake_head(snake["id"], snake["length"])
        else:
          squares[body["x"]][body["y"]].set_contains_snake(snake["id"], snake["length"])

  # NAVIGATION
  def is_valid_destination(self, snake_id, coordinates):

    # check if coordinates are out of bounds
    x, y = coordinates
    if x < 0 or y < 0 or x >= width or y >= height:
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
    for snake in self.snakes:
      #breath first search for each snake
      starting_x = snake["head"]["x"]
      starting_y = snake["head"]["y"]
      x, y = util.get_left(starting_x, starting_y)
