from renderer import Direction
import time

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
    self.step_size = 10
    self.time_step = 1 / (self.step_size * 5)
    self.last_time = 0

  def can_move(self):
    # Check if the player can move from the last_time and the step_size
    if time.time() - self.last_time > self.time_step:
      self.last_time = time.time()
      return True
    return False

  def move(self, direction = 1):
    if self.orientation == Direction.NORTH:
      if self.map[self.y - direction][self.x] == " " and self.can_move():
        if self.step["y"] in [-self.step_size, self.step_size]:
          self.y -= direction
          self.step["y"] = 0
        else:
          self.step["y"] += 1 * direction
        self.last_time = time.time()
    elif self.orientation == Direction.EAST:
      if self.map[self.y][self.x + direction] == " " and self.can_move():
        if self.step["x"] in [-self.step_size, self.step_size]:
          self.x += direction
          self.step["x"] = 0
        else:
          self.step["x"] += 1 * direction
        self.last_time = time.time()
    elif self.orientation == Direction.SOUTH:
      if self.map[self.y + direction][self.x] == " " and self.can_move():
        if self.step["y"] in [-self.step_size, self.step_size]:
          self.y += direction
          self.step["y"] = 0
        else:
          self.step["y"] -= 1 * direction
        self.last_time = time.time()
    elif self.orientation == Direction.WEST:
      if self.map[self.y][self.x - direction] == " " and self.can_move():
        if self.step["x"] in [-self.step_size, self.step_size]:
          self.x -= direction
          self.step["x"] = 0
        else:
          self.step["x"] -= 1 * direction
        self.last_time = time.time()

  def rotate_left(self):
    self.orientation = (self.orientation - 90) % 360

  def rotate_right(self):
    self.orientation = (self.orientation + 90) % 360