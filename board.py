import square

class board:
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
  
  def calculate_snakes_distances(self):
    for snake in self.snakes:
      #breath first search for each snake
      starting_x = snake["head"]["x"]
      starting_y = snake["head"]["y"]
      x, y = util.get_left(starting_x, starting_y)
      
    
