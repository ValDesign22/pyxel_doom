import time

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
  

  def set_pattern(self, pattern):
    self.pattern = pattern
    self.pattern_index = 0
    self.pattern_length = len(pattern)
    self.pattern_time = 0
    self.pattern_last_time = 0

  def move(self):
    if self.can_move():
      if self.pattern_time > 0:
        self.pattern_time -= 1
      else:
        self.pattern_index = (self.pattern_index + 1) % self.pattern_length
        self.pattern_time = self.pattern[self.pattern_index][1]
      self.update_step(self.pattern[self.pattern_index][0][0], self.pattern[self.pattern_index][0][1])

  def update_pos(self, direction):
    self.x += direction[0]
    self.y += direction[1]

  def get_pos(self):
    return (self.x, self.y)
  
  def get_map(self):
    return self.map
  
  def get_step(self):
    return self.step
  
  def set_step(self, axis, direction):
    self.step[axis] = direction

  def update_step(self, axis, direction):
    if self.step[axis] in [-self.step_size, self.step_size]:
      self.step[axis] = 0
      self.update_pos(direction)
    else:
      self.step[axis] += direction

class Enemy(EnemyBase):
  def __init__(self, x, y, map, speed, speed_factor = 5):
    super().__init__(x, y, map, speed, speed_factor)
    self.set_pattern([((0, 1), 10), ((1, 0), 10), ((0, -1), 10), ((-1, 0), 10)])
    self.last_time = time.time()
    self.pattern_time = self.pattern[0][1]

  def set_pattern(self, pattern):
    self.pattern = pattern
    self.pattern_index = 0
    self.pattern_length = len(pattern)
    self.pattern_time = 0
    self.pattern_last_time = 0

  def move(self):
    if self.can_move():
      if self.pattern_time > 0:
        self.pattern_time -= 1
      else:
        self.pattern_index = (self.pattern_index + 1) % self.pattern_length
        self.pattern_time = self.pattern[self.pattern_index][1]
      self.update_step(self.pattern[self.pattern_index][0][0], self.pattern[self.pattern_index][0][1])