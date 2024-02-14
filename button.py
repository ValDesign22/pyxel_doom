import pyxel

class Button():
  def __init__(self, x, y, width, height, color, text, text_color, action):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.color = color
    self.text = text
    self.text_color = text_color
    self.action = action

  def draw(self):
    pyxel.rectb(self.x, self.y, self.width, self.height, self.color)
    pyxel.text(self.x + (self.width - len(self.text) * 4) / 2, self.y + (self.height - 6) / 2, self.text, self.text_color)

  def focus(self):
    pyxel.rectb(self.x, self.y, self.width, self.height, 8)

  def is_clicked(self, x, y):
    if x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height:
      print("Button clicked")
      self.action()
      return True
    return False
  
class ArrowButton(Button):
  def __init__(self, x, y, width, height, color, text, text_color, action, direction):
    super().__init__(x, y, width, height, color, text, text_color, action)
    self.direction = direction

  def draw(self):
    if self.direction == "up":
      pyxel.line(self.x + 2, self.y + 2, self.x + 2, self.y + self.height - 2, self.text_color)
      pyxel.line(self.x + 2, self.y + 2, self.x + self.width - 2, self.y + self.height / 2, self.text_color)
      pyxel.line(self.x + 2, self.y + self.height - 2, self.x + self.width - 2, self.y + self.height / 2, self.text_color)
    elif self.direction == "down":
      pyxel.line(self.x + self.width - 2, self.y + 2, self.x + self.width - 2, self.y + self.height - 2, self.text_color)
      pyxel.line(self.x + self.width - 2, self.y + 2, self.x + 2, self.y + self.height / 2, self.text_color)
      pyxel.line(self.x + self.width - 2, self.y + self.height - 2, self.x + 2, self.y + self.height / 2, self.text_color)

  def focus(self):
    pyxel.rectb(self.x, self.y, self.width, self.height, 8)