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
    self.draw_obstacles("#")
    self.draw_obstacles("_")

  def draw_obstacles(self, obstacle_type):
    distance_to_obstacle = 0
    obstacle = False
    x, y = self.player.x, self.player.y
    
    i = -self.max_walls
    while i != 0:
      self.draw_next_wall(x, y, -i, obstacle_type)
      self.draw_next_wall(x, y, i, obstacle_type)
      i+=1
    
    while True:
      if x < 0 or x >= len(self.map[0]) or y < 0 or y >= len(self.map):
        break
      if self.player.orientation == Direction.NORTH:
        y -= 1
      elif self.player.orientation == Direction.EAST:
        x += 1
      elif self.player.orientation == Direction.SOUTH:
        y += 1
      elif self.player.orientation == Direction.WEST:
        x -= 1
      if distance_to_obstacle > self.render_distance:
        break
      if self.map[y][x] == "_" and obstacle_type == "#":
        break
      elif self.map[y][x] == "#" and obstacle_type == "_":
        break
      elif self.map[y][x] == obstacle_type:
        obstacle = True
        break
      distance_to_obstacle += 1
        
    if obstacle:
      obstacle_height = self.wall_height / (1 + distance_to_obstacle)
      self.draw_obstacle(self.middle["x"] - obstacle_height / 2, self.middle["x"] + obstacle_height / 2, obstacle_height, self.colors.get(obstacle_type, 0))

  def draw_next_wall(self, x, y, side, obstacle_type):
    distance_to_obstacle = 0
    obstacle = False
    x, y = x, y

    if self.player.orientation == Direction.NORTH:
      x += side
    elif self.player.orientation == Direction.EAST:
      y += side
    elif self.player.orientation == Direction.SOUTH:
      x -= side
    elif self.player.orientation == Direction.WEST:
      y -= side

    while True:
      if x < 0 or x >= len(self.map[0]) or y < 0 or y >= len(self.map):
        break
      if self.player.orientation == Direction.NORTH:
        y -= 1
        if self.map[y+1][x] != " ":
          break
      elif self.player.orientation == Direction.EAST:
        x += 1
        if self.map[y][x-1] != " ":
          break
      elif self.player.orientation == Direction.SOUTH:
        y += 1
        if self.map[y-1][x] != " ":
          break
      elif self.player.orientation == Direction.WEST:
        x -= 1
        if self.map[y][x+1] != " ":
          break
      if distance_to_obstacle > self.render_distance:
        break
      if self.map[y][x] == "_" and obstacle_type == "#":
        break
      elif self.map[y][x] == "#" and obstacle_type == "_":
        break
      elif self.map[y][x] == obstacle_type:
        obstacle = True
        break
      distance_to_obstacle += 1

    if obstacle:
      obstacle_height = self.wall_height / (1 + distance_to_obstacle)
      color = self.colors.get(obstacle_type, 0)
      left = self.middle["x"] - obstacle_height / 2 + side * obstacle_height
      right = self.middle["x"] + obstacle_height / 2 + side * obstacle_height
      if obstacle_type == "#": self.draw_side(distance_to_obstacle, x, y, side, color)
      self.draw_obstacle(left, right, obstacle_height, color)
  
  def draw_obstacle(self, left, right, obstacle_height, color):
    if self.render_mode == "3D":
      pyxel.rect(left, self.middle["y"] - obstacle_height / 2, right - left, obstacle_height, color)
    pyxel.line(left, self.middle["y"] - obstacle_height / 2, left, self.middle["y"] + obstacle_height / 2, 12)
    pyxel.line(right, self.middle["y"] - obstacle_height / 2, right, self.middle["y"] + obstacle_height / 2, 12)
    pyxel.line(left, self.middle["y"] - obstacle_height / 2, right, self.middle["y"] - obstacle_height / 2, 12)
    pyxel.line(left, self.middle["y"] + obstacle_height / 2, right, self.middle["y"] + obstacle_height / 2, 12)

  def draw_side(self, distance, x0, y0, side, color):
    x, y = x0, y0
    if self.player.orientation == Direction.NORTH:
      x -= side
    elif self.player.orientation == Direction.EAST:
      y -= side
    elif self.player.orientation == Direction.SOUTH:
      x += side
    elif self.player.orientation == Direction.WEST:
      y += side
    if self.map[y][x] != " ":
      return
    
    obstacle_height = self.wall_height / (1+distance)
    oh2 = self.wall_height / (2+distance)
    if side > 0:
      top_left = self.middle["x"] - obstacle_height / 2 + side * obstacle_height
      top_left2 = self.middle["x"] - oh2 / 2 + side * oh2
      bottom_left = self.middle["x"] - obstacle_height / 2 + side * obstacle_height
      bottom_left2 = self.middle["x"] - oh2 / 2 + side * oh2
      if self.render_mode == "3D":
        pyxel.tri(top_left, self.middle["y"] - obstacle_height / 2, top_left2, self.middle["y"] - oh2 / 2, top_left2, self.middle["y"] + oh2 / 2, color)
        pyxel.tri(top_left, self.middle["y"] - obstacle_height / 2, bottom_left, self.middle["y"] + obstacle_height / 2, bottom_left2, self.middle["y"] + oh2 / 2, color)
      pyxel.line(top_left, self.middle["y"] - obstacle_height / 2, top_left2, self.middle["y"] - oh2 / 2, 12)
      pyxel.line(bottom_left, self.middle["y"] + obstacle_height / 2, bottom_left2, self.middle["y"] + oh2 / 2, 12)
      pyxel.line(top_left2, self.middle["y"] - oh2 / 2, top_left2, self.middle["y"] + oh2 / 2, 12)
    else:
      top_right = self.middle["x"] + obstacle_height / 2 + side * obstacle_height
      top_right2 = self.middle["x"] + oh2 / 2 + side * oh2
      bottom_right = self.middle["x"] + obstacle_height / 2 + side * obstacle_height
      bottom_right2 = self.middle["x"] + oh2 / 2 + side * oh2
      if self.render_mode == "3D":
        pyxel.tri(top_right, self.middle["y"] - obstacle_height / 2, top_right2, self.middle["y"] - oh2 / 2, top_right2, self.middle["y"] + oh2 / 2, color)
        pyxel.tri(top_right, self.middle["y"] - obstacle_height / 2, bottom_right, self.middle["y"] + obstacle_height / 2, bottom_right2, self.middle["y"] + oh2 / 2, color)
      pyxel.line(top_right, self.middle["y"] - obstacle_height / 2, top_right2, self.middle["y"] - oh2 / 2, 12)
      pyxel.line(bottom_right, self.middle["y"] + obstacle_height / 2, bottom_right2, self.middle["y"] + oh2 / 2, 12)
      pyxel.line(top_right2, self.middle["y"] - oh2 / 2, top_right2, self.middle["y"] + oh2 / 2, 12)
