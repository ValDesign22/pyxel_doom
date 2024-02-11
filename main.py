import pyxel
import time

from button import Button
from player import Player
from renderer import Renderer

class App:
  def __init__(self):
    pyxel.init(640, 360, title="Pyxel Doom", fps=60)

    # Map
    self.colors = {
      "#": 8,
      "_": 7,
      " ": 0
    }
    self.middle = {
      "x": pyxel.width // 2,
      "y": pyxel.height // 2
    }
    self.floor_size = 2
    self.wall_height = pyxel.height // 2
    self.map = [
      "######################",
      "#    #               #",
      "#    #               #",
      "#                    #",
      "#                    #",
      "#                    #",
      "##_#                 #",
      "#  #                 #",
      "######################"
    ]
    
    # Player
    self.player_x = len(self.map[0]) // 2
    self.player_y = len(self.map) // 2
    self.orientation = 0 # 0: North, 90: East, 180: South, 270: West
    self.player = Player(self.player_x, self.player_y, self.orientation, self.map)

    # Parameters
    self.debug = False
    self.max_render_distance = 8
    self.started_time = time.time()
    self.game_paused = False

    self.renderer = Renderer(self.player, self.map, self.colors, self.middle, self.wall_height, self.max_render_distance)

    pyxel.run(self.update, self.draw)

  # Game loop
  def update(self):
    # Menu
    if pyxel.btnp(pyxel.KEY_F1):
      self.debug = not self.debug
    if pyxel.btnp(pyxel.KEY_F2):
      self.game_paused = not self.game_paused
      pyxel.mouse(self.game_paused)
      
    # Game paused
    if self.game_paused:
      if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        self.settings_button.is_clicked(pyxel.mouse_x, pyxel.mouse_y)
        self.quit_button.is_clicked(pyxel.mouse_x, pyxel.mouse_y)
      return

    # Player movement
    if pyxel.btnp(pyxel.KEY_Z):
      self.player.move_forward()
    if pyxel.btnp(pyxel.KEY_S):
      self.player.move_backward()
    if pyxel.btnp(pyxel.KEY_Q):
      self.player.rotate_left()
    if pyxel.btnp(pyxel.KEY_D):
      self.player.rotate_right()

    self.player.x = max(0, min(len(self.map[0]) - 1, self.player.x))
    self.player.y = max(0, min(len(self.map) - 1, self.player.y))

  def draw(self):
    pyxel.cls(0)

    if self.game_paused:
      middle_x = pyxel.width // 2
      middle_y = pyxel.height // 2
      pyxel.text(middle_x - 32, middle_y - 64, "Game Paused", 7)

      # Draw buttons
      self.settings_button = Button(middle_x - 42, middle_y - 40, 64, 16, 7, "Settings", 7, self.settings)
      self.settings_button.draw()
      self.quit_button = Button(middle_x - 42, middle_y - 16, 64, 16, 7, "Quit", 7, pyxel.quit)
      self.quit_button.draw()
      return
    
    # Draw elements
    self.renderer.draw()
    
    minimap_colors = {
      "#": 3,
      "_": 7,
      " ": 0
    }

    # Draw minimap
    for y, row in enumerate(self.map):
      for x, tile in enumerate(row):
        pyxel.rect(x * self.floor_size, y * self.floor_size, self.floor_size, self.floor_size, minimap_colors[tile])
    pyxel.rect(self.player.x * self.floor_size, self.player.y * self.floor_size, self.floor_size, self.floor_size, 9)

    # Draw debug
    if self.debug:
      pyxel.text(pyxel.width - 48, 4, f"{self.player.x}, {self.player.y}", 7)
      pyxel.text(pyxel.width - 48, 12, f"{"North" if self.player.orientation == 0 else "East" if self.player.orientation == 90 else "South" if self.player.orientation == 180 else "West"}", 7)
      pyxel.text(pyxel.width - 48, 20, f"{(pyxel.frame_count/(time.time() - self.started_time)):.2f} FPS", 7)

  # Button actions
  def settings(self):
    pass

  # Map rendering
  # def draw_obstacles(self, obstacle_type):
  #   distance_to_obstacle = 0
  #   obstacle = False
  #   x, y = self.player.x, self.player.y

  #   self.draw_next_wall(x, y, 1, obstacle_type)
  #   self.draw_next_wall(x, y, -1, obstacle_type)
    
  #   while True:
  #     if self.player.orientation == Direction.NORTH:
  #       y -= 1
  #     elif self.player.orientation == Direction.EAST:
  #       x += 1
  #     elif self.player.orientation == Direction.SOUTH:
  #       y += 1
  #     elif self.player.orientation == Direction.WEST:
  #       x -= 1
  #     if distance_to_obstacle > self.max_render_distance:
  #       break
  #     if x < 0 or x >= len(self.map[0]) or y < 0 or y >= len(self.map):
  #       break
  #     if self.map[y][x] == "_" and obstacle_type == "#":
  #       break
  #     elif self.map[y][x] == "#" and obstacle_type == "_":
  #       break
  #     elif self.map[y][x] == obstacle_type:
  #       obstacle = True
  #       break
  #     distance_to_obstacle += 1
        
  #   if obstacle:
  #     obstacle_height = self.wall_height / (1 + distance_to_obstacle)
  #     color = self.colors.get(obstacle_type, 0)
  #     left = self.middle["x"] - obstacle_height / 2
  #     right = self.middle["x"] + obstacle_height / 2
  #     self.draw_obstacle(left, right, obstacle_height, color)

  # def draw_next_wall(self, x, y, side, obstacle_type):
  #   distance_to_obstacle = 0
  #   obstacle = False
  #   x, y = x, y

  #   if self.player.orientation == Direction.NORTH:
  #     x += side
  #   elif self.player.orientation == Direction.EAST:
  #     y += side
  #   elif self.player.orientation == Direction.SOUTH:
  #     x -= side
  #   elif self.player.orientation == Direction.WEST:
  #     y -= side

  #   while True:
  #     if self.player.orientation == Direction.NORTH:
  #       y -= 1
  #       if self.map[y+1][x] != " ":
  #         break
  #     elif self.player.orientation == Direction.EAST:
  #       x += 1
  #       if self.map[y][x-1] != " ":
  #         break
  #     elif self.player.orientation == Direction.SOUTH:
  #       y += 1
  #       if self.map[y-1][x] != " ":
  #         break
  #     elif self.player.orientation == Direction.WEST:
  #       x -= 1
  #       if self.map[y][x+1] != " ":
  #         break
  #     if distance_to_obstacle > self.max_render_distance:
  #       break
  #     if x < 0 or x >= len(self.map[0]) or y < 0 or y >= len(self.map):
  #       break
  #     if self.map[y][x] == "_" and obstacle_type == "#":
  #       break
  #     elif self.map[y][x] == "#" and obstacle_type == "_":
  #       break
  #     elif self.map[y][x] == obstacle_type:
  #       obstacle = True
  #       break
  #     distance_to_obstacle += 1

  #   if obstacle:
  #     obstacle_height = self.wall_height / (1 + distance_to_obstacle)
  #     color = self.colors.get(obstacle_type, 0)
  #     left = self.middle["x"] - obstacle_height / 2 + side * obstacle_height
  #     right = self.middle["x"] + obstacle_height / 2 + side * obstacle_height
  #     self.draw_obstacle(left, right, obstacle_height, color)
  
  # def draw_obstacle(self, left, right, obstacle_height, color):
  #   pyxel.rect(left, self.middle["y"] - obstacle_height / 2, right - left, obstacle_height, color)
  #   pyxel.line(left, self.middle["y"] - obstacle_height / 2, left, self.middle["y"] + obstacle_height / 2, 12)
  #   pyxel.line(right, self.middle["y"] - obstacle_height / 2, right, self.middle["y"] + obstacle_height / 2, 12)
  #   pyxel.line(left, self.middle["y"] - obstacle_height / 2, right, self.middle["y"] - obstacle_height / 2, 12)
  #   pyxel.line(left, self.middle["y"] + obstacle_height / 2, right, self.middle["y"] + obstacle_height / 2, 12)

App()