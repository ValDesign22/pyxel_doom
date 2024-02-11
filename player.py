class Player:
  def __init__(self, x, y, orientation, map):
    self.x = x
    self.y = y
    self.orientation = orientation
    self.map = map

  def move_forward(self):
    if self.orientation == 0:
      if self.map[self.y - 1][self.x] == " ":
        self.y -= 1
    elif self.orientation == 90:
      if self.map[self.y][self.x + 1] == " ":
        self.x += 1
    elif self.orientation == 180:
      if self.map[self.y + 1][self.x] == " ":
        self.y += 1
    elif self.orientation == 270:
      if self.map[self.y][self.x - 1] == " ":
        self.x -= 1

  def move_backward(self):
    if self.orientation == 0: 
      if self.map[self.y + 1][self.x] == " ":
        self.y += 1
    elif self.orientation == 90:
      if self.map[self.y][self.x - 1] == " ":
        self.x -= 1
    elif self.orientation == 180:
      if self.map[self.y - 1][self.x] == " ":
        self.y -= 1
    elif self.orientation == 270:
      if self.map[self.y][self.x + 1] == " ":
        self.x += 1

  def rotate_left(self):
    self.orientation = (self.orientation - 90) % 360

  def rotate_right(self):
    self.orientation = (self.orientation + 90) % 360