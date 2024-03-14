from renderer import Direction
import time

class Player:
  def __init__(self, x, y, orientation, map, speed):
    self.x = x
    self.y = y
    self.orientation = orientation
    self.map = map
    self.step = {
      "y": 0,
      "x": 0,
    }
    self.step_size = speed
    self.time_step = 1 / (self.step_size * 5)
    self.last_time = 0

  def sprint(self, pressed):
    self.time_step = 1 / (self.step_size * (10 if pressed else 5))

  def can_move(self):
    if time.time() - self.last_time > self.time_step:
      self.last_time = time.time()
      return True
    return False
  
  def update_step(self, axis, direction):
    if self.step[axis] in [-self.step_size, self.step_size]:
      self.step[axis] = 0
      self.update_pos(axis, direction)
    else:
      if self.orientation == Direction.NORTH or self.orientation == Direction.SOUTH:
        self.step[axis] -= 1 * direction
      elif self.orientation == Direction.EAST or self.orientation == Direction.WEST:
        self.step[axis] += 1 * direction

  def update_pos(self, axis, delta):
    if axis == "x":
      self.x += delta
    elif axis == "y":
      self.y += delta

  def move(self, direction = 1):
    if self.can_move():
      if self.orientation == Direction.NORTH and self.map[self.y - direction][self.x] == " ":
        self.update_step("y", -direction)
      elif self.orientation == Direction.EAST and self.map[self.y][self.x + direction] == " ":
        self.update_step("x", direction)
      elif self.orientation == Direction.SOUTH and self.map[self.y + direction][self.x] == " ":
        self.update_step("y", direction)
      elif self.orientation == Direction.WEST and self.map[self.y][self.x - direction] == " ":
        self.update_step("x", -direction)
      self.last_time = time.time()

  def rotate(self, direction):
    self.orientation = (self.orientation + 90 * direction) % 360