import pyxel


class Direction:
  NORTH = 0
  EAST = 90
  SOUTH = 180
  WEST = 270

class Renderer():
  def __init__(self, player, map, colors, middle, wall_height, max_render_distance):
    self.player = player
    self.map = map
    self.colors = colors
    self.middle = middle
    self.wall_height = wall_height
    self.max_render_distance = max_render_distance

  def draw(self):
    self.draw_obstacles("#")
    self.draw_obstacles("_")

  def draw_obstacles(self, obstacle_type):
    distance_to_obstacle = 0
    obstacle = False
    x, y = self.player.x, self.player.y

    self.draw_next_wall(x, y, 1, obstacle_type)
    self.draw_next_wall(x, y, -1, obstacle_type)
    
    while True:
      if self.player.orientation == Direction.NORTH:
        y -= 1
      elif self.player.orientation == Direction.EAST:
        x += 1
      elif self.player.orientation == Direction.SOUTH:
        y += 1
      elif self.player.orientation == Direction.WEST:
        x -= 1
      if distance_to_obstacle > self.max_render_distance:
        break
      if x < 0 or x >= len(self.map[0]) or y < 0 or y >= len(self.map):
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
      left = self.middle["x"] - obstacle_height / 2
      right = self.middle["x"] + obstacle_height / 2
      self.draw_obstacle(left, right, obstacle_height, color)

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
      if distance_to_obstacle > self.max_render_distance:
        break
      if x < 0 or x >= len(self.map[0]) or y < 0 or y >= len(self.map):
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
      self.draw_obstacle(left, right, obstacle_height, color)
  
  def draw_obstacle(self, left, right, obstacle_height, color):
    pyxel.rect(left, self.middle["y"] - obstacle_height / 2, right - left, obstacle_height, color)
    pyxel.line(left, self.middle["y"] - obstacle_height / 2, left, self.middle["y"] + obstacle_height / 2, 12)
    pyxel.line(right, self.middle["y"] - obstacle_height / 2, right, self.middle["y"] + obstacle_height / 2, 12)
    pyxel.line(left, self.middle["y"] - obstacle_height / 2, right, self.middle["y"] - obstacle_height / 2, 12)
    pyxel.line(left, self.middle["y"] + obstacle_height / 2, right, self.middle["y"] + obstacle_height / 2, 12)