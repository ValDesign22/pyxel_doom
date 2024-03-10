from renderer import Direction

class Player:
  def __init__(self, x, y, orientation, map, fps):
    self.x = x
    self.y = y
    self.orientation = orientation
    self.map = map
    self.step = {
      "y": 0,
      "x": 0,
    }
    self.step_size = (fps / (fps / 25)) if fps > 30 else fps
    print(self.step_size)

  def move(self, direction = 1):
    if self.orientation == Direction.NORTH:
      if self.map[self.y - direction][self.x] == " ":
        if self.step["y"] in [-self.step_size, self.step_size]:
          self.y -= direction
          self.step["y"] = 0
        else:
          self.step["y"] += 1 * direction
    elif self.orientation == Direction.EAST:
      if self.map[self.y][self.x + direction] == " ":
        if self.step["x"] in [-self.step_size, self.step_size]:
          self.x += direction
          self.step["x"] = 0
        else:
          self.step["x"] += 1 * direction
    elif self.orientation == Direction.SOUTH:
      if self.map[self.y + direction][self.x] == " ":
        if self.step["y"] in [-self.step_size, self.step_size]:
          self.y += direction
          self.step["y"] = 0
        else:
          self.step["y"] -= 1 * direction
    elif self.orientation == Direction.WEST:
      if self.map[self.y][self.x - direction] == " ":
        if self.step["x"] in [-self.step_size, self.step_size]:
          self.x -= direction
          self.step["x"] = 0
        else:
          self.step["x"] -= 1 * direction

  def rotate_left(self):
    self.orientation = (self.orientation - 90) % 360

  def rotate_right(self):
    self.orientation = (self.orientation + 90) % 360