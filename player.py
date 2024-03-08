from renderer import Direction

class Player:
  def __init__(self, x, y, orientation, map):
    self.x = x
    self.y = y
    self.orientation = orientation
    self.map = map
    self.step = {
      "y": 0,
      "x": 0,
    }

  def move(self, direction = 1):
    if self.orientation == Direction.NORTH:
      if self.map[self.y - direction][self.x] == " ":
        if self.step["y"] in [-9, 9]:
          self.y -= direction
          self.step["y"] = 0
        else:
          self.step["y"] += 1 * direction
    elif self.orientation == Direction.EAST:
      if self.map[self.y][self.x + direction] == " ":
        if self.step["x"] in [-9, 9]:
          self.x += direction
          self.step["x"] = 0
        else:
          self.step["x"] += 1 * direction
    elif self.orientation == Direction.SOUTH:
      if self.map[self.y + direction][self.x] == " ":
        if self.step["y"] in [-9, 9]:
          self.y += direction
          self.step["y"] = 0
        else:
          self.step["y"] -= 1 * direction
    elif self.orientation == Direction.WEST:
      if self.map[self.y][self.x - direction] == " ":
        if self.step["x"] in [-9, 9]:
          self.x -= direction
          self.step["x"] = 0
        else:
          self.step["x"] -= 1 * direction
    
    print(f"Player position: {self.x}, {self.y}")
    print(f"Player orientation: {self.orientation}")
    print(f"Player step: {self.step}")

  def rotate_left(self):
    self.orientation = (self.orientation - 90) % 360

  def rotate_right(self):
    self.orientation = (self.orientation + 90) % 360