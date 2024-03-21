import pyxel

class Direction:
  NORTH = 0
  EAST = 90
  SOUTH = 180
  WEST = 270

class Renderer():
  def __init__(self, player, map, colors, middle, wall_height, render_distance, max_walls):
    self.player = player
    self.map = map
    self.colors = colors
    self.middle = middle
    self.wall_height = wall_height
    self.render_distance = render_distance
    self.max_walls = max_walls
    self.render_mode = "3D"

  def change_render_mode(self):
    modes = ["wireframe", "3D"]
    self.render_mode = modes[(modes.index(self.render_mode) + 1) % len(modes)]

  def draw(self):
    x, y = self.player.x, self.player.y

    i = -self.max_walls
    while i != 0:
      self.draw_row(x, y, -i)
      self.draw_row(x, y, i)
      i+=1
    self.draw_row(x, y, 0)

  def draw_row(self, x, y, row):
    orientation = self.player.orientation

    if orientation == Direction.NORTH: x += row
    elif orientation == Direction.EAST: y += row
    elif orientation == Direction.SOUTH: x -= row
    elif orientation == Direction.WEST: y -= row
    if x < 0 or x >= len(self.map[0]) or y < 0 or y >= len(self.map): return

    distance = 0

    while True:
      if self.player.orientation == Direction.NORTH: y -= 1
      elif self.player.orientation == Direction.EAST: x += 1
      elif self.player.orientation == Direction.SOUTH: y += 1
      elif self.player.orientation == Direction.WEST: x -= 1
      if x < 0 or x >= len(self.map[0]) or y < 0 or y >= len(self.map): break
      if distance > self.render_distance: break
      distance += 1

    while distance != 0:
      if self.player.orientation == Direction.NORTH: y += 1
      elif self.player.orientation == Direction.EAST: x -= 1
      elif self.player.orientation == Direction.SOUTH: y -= 1
      elif self.player.orientation == Direction.WEST: x += 1
      if x < 0 or x >= len(self.map[0]) or y < 0 or y >= len(self.map): break
      if self.map[y][x] != " ":
        self.draw_obstacle(distance, x, y, row)
        if row != 0:
          self.draw_side(distance, x, y, row)
      distance -= 1

  def draw_obstacle(self, distance, x, y, row):
    step=0
    front_step = 0
    if self.player.orientation == Direction.NORTH or self.player.orientation == Direction.SOUTH:
      step = -self.player.step["x"]
      front_step = self.player.step["y"] if self.player.orientation == Direction.NORTH else -self.player.step["y"]
    elif self.player.orientation == Direction.EAST or self.player.orientation == Direction.WEST:
      step = self.player.step["y"]
      front_step = self.player.step["x"] if self.player.orientation == Direction.EAST else -self.player.step["x"]
    obstacle_height = self.wall_height / (1 + distance - front_step / self.player.step_size)
    left = self.middle["x"] - obstacle_height / 2 + row * obstacle_height
    right = self.middle["x"] + obstacle_height / 2 + row * obstacle_height
    left += step * obstacle_height / self.player.step_size
    right += step * obstacle_height / self.player.step_size
    if self.map[y][x] not in [" ", "K"]:
      color = self.colors.get(self.map[y][x], 0)
      if self.render_mode =="3D": pyxel.rect(left, self.middle["y"] - obstacle_height / 2, right - left, obstacle_height, color)
      pyxel.line(left, self.middle["y"] - obstacle_height / 2, left, self.middle["y"] + obstacle_height / 2, 12)
      pyxel.line(right, self.middle["y"] - obstacle_height / 2, right, self.middle["y"] + obstacle_height / 2, 12)
      pyxel.line(left, self.middle["y"] - obstacle_height / 2, right, self.middle["y"] - obstacle_height / 2, 12)
      pyxel.line(left, self.middle["y"] + obstacle_height / 2, right, self.middle["y"] + obstacle_height / 2, 12)
    elif self.map[y][x] == "K":
      key_x = left+obstacle_height/2
      key_y = self.middle["y"]
      pyxel.rect(key_x, key_y-5, 5, 20, 10)
  
  def draw_side(self, distance, x, y, row):
    if self.map[y][x] not in [" ", "K"]:
      step = 0
      front_step = 0
      if self.player.orientation == Direction.NORTH or self.player.orientation == Direction.SOUTH:
        step = -self.player.step["x"]
        front_step = self.player.step["y"] if self.player.orientation == Direction.NORTH else -self.player.step["y"]
      elif self.player.orientation == Direction.EAST or self.player.orientation == Direction.WEST:
        step = self.player.step["y"]
        front_step = self.player.step["x"] if self.player.orientation == Direction.EAST else -self.player.step["x"]
      obstacle_height = self.wall_height / (1 + distance - front_step / self.player.step_size)
      oh2 = self.wall_height / (2+distance - front_step / self.player.step_size)
      color = self.colors.get(self.map[y][x], 0)
      if row > 0:
        top_left = self.middle["x"] - obstacle_height / 2 + row * obstacle_height
        top_left2 = self.middle["x"] - oh2 / 2 + row * oh2
        bottom_left = self.middle["x"] - obstacle_height / 2 + row * obstacle_height
        bottom_left2 = self.middle["x"] - oh2 / 2 + row * oh2
        top_left += step * obstacle_height / self.player.step_size
        top_left2 += step * oh2 / self.player.step_size
        bottom_left += step * obstacle_height / self.player.step_size
        bottom_left2 += step * oh2 / self.player.step_size
        if self.render_mode == "3D":
          pyxel.tri(top_left, self.middle["y"] - obstacle_height / 2, top_left2, self.middle["y"] - oh2 / 2, top_left2, self.middle["y"] + oh2 / 2, color)
          pyxel.tri(top_left, self.middle["y"] - obstacle_height / 2, bottom_left, self.middle["y"] + obstacle_height / 2, bottom_left2, self.middle["y"] + oh2 / 2, color)
        pyxel.line(top_left, self.middle["y"] - obstacle_height / 2, top_left2, self.middle["y"] - oh2 / 2, 12)
        pyxel.line(bottom_left, self.middle["y"] + obstacle_height / 2, bottom_left2, self.middle["y"] + oh2 / 2, 12)
        pyxel.line(top_left2, self.middle["y"] - oh2 / 2, top_left2, self.middle["y"] + oh2 / 2, 12)
      else:
        top_right = self.middle["x"] + obstacle_height / 2 + row * obstacle_height
        top_right2 = self.middle["x"] + oh2 / 2 + row * oh2
        bottom_right = self.middle["x"] + obstacle_height / 2 + row * obstacle_height
        bottom_right2 = self.middle["x"] + oh2 / 2 + row * oh2
        top_right += step * obstacle_height / self.player.step_size
        top_right2 += step * oh2 / self.player.step_size
        bottom_right += step * obstacle_height / self.player.step_size
        bottom_right2 += step * oh2 / self.player.step_size
        if self.render_mode == "3D":
          pyxel.tri(top_right, self.middle["y"] - obstacle_height / 2, top_right2, self.middle["y"] - oh2 / 2, top_right2, self.middle["y"] + oh2 / 2, color)
          pyxel.tri(top_right, self.middle["y"] - obstacle_height / 2, bottom_right, self.middle["y"] + obstacle_height / 2, bottom_right2, self.middle["y"] + oh2 / 2, color)
        pyxel.line(top_right, self.middle["y"] - obstacle_height / 2, top_right2, self.middle["y"] - oh2 / 2, 12)
        pyxel.line(bottom_right, self.middle["y"] + obstacle_height / 2, bottom_right2, self.middle["y"] + oh2 / 2, 12)
        pyxel.line(top_right2, self.middle["y"] - oh2 / 2, top_right2, self.middle["y"] + oh2 / 2, 12)