class Player:
  def __init__(self, x, y, orientation, map):
    self.x = x
    self.y = y
    self.orientation = orientation
    self.map = map

  def move(self, direction = 1):
    if self.orientation == 0:
      if self.map[self.y - direction][self.x] == " ":
        self.y -= direction
    elif self.orientation == 90:
      if self.map[self.y][self.x + direction] == " ":
        self.x += direction
    elif self.orientation == 180:
      if self.map[self.y + direction][self.x] == " ":
        self.y += direction
    elif self.orientation == 270:
      if self.map[self.y][self.x - direction] == " ":
        self.x -= direction

  def rotate_left(self):
    self.orientation = (self.orientation - 90) % 360

  def rotate_right(self):
    self.orientation = (self.orientation + 90) % 360