import pyxel
import time

from button import Button
from config import Config
from player import Player
from renderer import Renderer

class App:
  def __init__(self):
    self.config = Config()
    resolution = self.config.get("config.resolution").split("x")

    pyxel.init(int(resolution[0]), int(resolution[1]), title="Pyxel Doom", fps=self.config.get("config.frame_rate"))

    # Map
    self.colors = { "#": 8, "_": 7, " ": 0 }
    self.middle = { "x": pyxel.width // 2, "y": pyxel.height // 2 }
    self.floor_size = 2
    self.wall_height = pyxel.height // 2
    self.map = open(self.config.get("assets.map")).read().split("\n")
    
    # Player
    self.player = Player(len(self.map[0]) // 2, len(self.map) // 2, 0, self.map)

    # Parameters
    self.debug = False
    self.max_render_distance = self.config.get("config.render_distance")
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
      pyxel.text(self.middle["x"] - 32, self.middle["y"] - 64, "Game Paused", 7)

      # Draw buttons
      self.settings_button = Button(self.middle["x"] - 42, self.middle["y"] - 40, 64, 16, 7, "Settings", 7, self.settings)
      self.settings_button.draw()
      self.quit_button = Button(self.middle["x"] - 42, self.middle["y"] - 16, 64, 16, 7, "Quit", 7, pyxel.quit)
      self.quit_button.draw()
      return
    
    # Draw elements
    self.renderer.draw()
    # Draw minimap
    for y, row in enumerate(self.map):
      for x, tile in enumerate(row):
        pyxel.rect(x * self.floor_size, y * self.floor_size, self.floor_size, self.floor_size, self.colors[tile])
    pyxel.rect(self.player.x * self.floor_size, self.player.y * self.floor_size, self.floor_size, self.floor_size, 9)

    # Draw debug
    if self.debug:
      pyxel.text(pyxel.width - 48, 4, f"{self.player.x}, {self.player.y}", 7)
      pyxel.text(pyxel.width - 48, 12, f"{"North" if self.player.orientation == 0 else "East" if self.player.orientation == 90 else "South" if self.player.orientation == 180 else "West"}", 7)
      pyxel.text(pyxel.width - 48, 20, f"{(pyxel.frame_count/(time.time() - self.started_time)):.2f} FPS", 7)

  # Button actions
  def settings(self):
    pass

if __name__ == "__main__":
  App()