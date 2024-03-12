import time
from renderer import Direction

class EnemyBase:
  def __init__(self, x, y, map, speed, speed_factor = 5):
    self.x = x
    self.y = y
    self.map = map
    self.step = {
      "y": 0,
      "x": 0,
    }
    self.step_size = speed
    self.time_step = 1 / (self.step_size * speed_factor)
    self.last_time = 0


  def can_move(self):
    if time.time() - self.last_time > self.time_step:
      self.last_time = time.time()
      return True
    return False


  def set_pattern(self, pattern): # pattern = [((x, y), time), ...]
    self.pattern = pattern
    self.pattern_index = 0
    self.pattern_length = len(pattern)
    self.pattern_time = 0
    self.pattern_last_time = 0

  def move(self):
    if self.can_move():
      if self.pattern_time >= self.pattern[self.pattern_index][1]:
        self.pattern_time = 0
        self.pattern_index = (self.pattern_index + 1) % self.pattern_length
      else:
        self.pattern_time += 1
        self.step = {
          "y": self.pattern[self.pattern_index][0][0],
          "x": self.pattern[self.pattern_index][0][1],
        }
        self.x += self.step["x"]
        self.y += self.step["y"]

  def get_pos(self):
    return (self.x, self.y)