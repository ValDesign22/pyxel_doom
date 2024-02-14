import math
import pyxel
import time

from button import ArrowButton, Button
from config import Config
from player import Player
from renderer import Renderer

class App:
  def __init__(self):
    self.config = Config()
    self.resolution = self.config.get("config.resolution").split("x")

    pyxel.init(
      width=int(self.resolution[0]),
      height=int(self.resolution[1]),
      title="Pyxel Doom",
      fps=self.config.get("config.frame_rate"),
      quit_key=None,
    )

    # Map
    self.colors = self.config.get("colors")
    self.middle = { "x": pyxel.width // 2, "y": pyxel.height // 2 }
    self.floor_size = 2
    self.wall_height = pyxel.height // 2
    self.map = open(self.config.get("assets.map")).read().split("\n")
    
    # Player
    self.player = Player(len(self.map[0]) // 2, len(self.map) // 2, 0, self.map)

    # Parameters
    self.debug = False
    self.render_distance = self.config.get("config.render_distance")
    self.started_time = time.time()
    self.game_paused = False
    self.settings_shown = False
    self.max_walls = self.config.get("config.max_walls")
    self.fullscreen = self.config.get("config.fullscreen")

    self.renderer = Renderer(self.player, self.map, self.colors, self.middle, self.wall_height, self.render_distance, self.max_walls)

    pyxel.fullscreen(self.fullscreen)
    pyxel.run(self.update, self.draw)

  # Game loop
  def update(self):
    # Menu
    if pyxel.btnp(pyxel.KEY_F1) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_BACK):
      self.debug = not self.debug
    if pyxel.btnp(pyxel.KEY_F2) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
      self.game_paused = not self.game_paused
      pyxel.mouse(self.game_paused)
    if pyxel.btnp(pyxel.KEY_F3): # Only with keyboard
      self.renderer.change_render_mode()
    if pyxel.btnp(pyxel.KEY_F11):
      pyxel.fullscreen(not self.fullscreen)
      self.fullscreen = self.config.set("config.fullscreen", not self.fullscreen)

    # Game paused
    if self.game_paused:
      if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        if self.settings_shown == False:
          self.settings_button.is_clicked(pyxel.mouse_x, pyxel.mouse_y)
          self.quit_button.is_clicked(pyxel.mouse_x, pyxel.mouse_y)
        else:
          self.rdist_btn_down.is_clicked(pyxel.mouse_x, pyxel.mouse_y)
          self.rdist_btn_up.is_clicked(pyxel.mouse_x, pyxel.mouse_y)
          self.frate_btn_down.is_clicked(pyxel.mouse_x, pyxel.mouse_y)
          self.frate_btn_up.is_clicked(pyxel.mouse_x, pyxel.mouse_y)
          self.res_btn_down.is_clicked(pyxel.mouse_x, pyxel.mouse_y)
          self.res_btn_up.is_clicked(pyxel.mouse_x, pyxel.mouse_y)
          self.save_button.is_clicked(pyxel.mouse_x, pyxel.mouse_y)
      if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
        print("A")
      return

    # Player movement
    if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
      self.player.move(1)
    if pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
      self.player.move(-1)
    if pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
      self.player.rotate_left()
    if pyxel.btnp(pyxel.KEY_D) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
      self.player.rotate_right()

    self.player.x = max(0, min(len(self.map[0]) - 1, self.player.x))
    self.player.y = max(0, min(len(self.map) - 1, self.player.y))

  def draw(self):
    pyxel.cls(0)

    if self.game_paused:
      # Draw buttons
      if self.settings_shown == False:
        pyxel.text(self.middle["x"] - 32, self.middle["y"] - 64, "Game Paused", 7)

        self.settings_button = Button(self.middle["x"] - 42, self.middle["y"] - 40, 64, 16, 7, "Settings", 7, self.settings)
        self.settings_button.draw()
        self.quit_button = Button(self.middle["x"] - 42, self.middle["y"] - 16, 64, 16, 7, "Quit", 7, pyxel.quit)
        self.quit_button.draw()
      else:
        """
        Render distance ^ 8 v
        Frame rate ^ 60 v
        Resolution ^ 640x360 v      
        """
        # Render distance
        pyxel.text(self.middle["x"] - 32, self.middle["y"] - 64, "Settings", 7)
        pyxel.text(self.middle["x"] - 64, self.middle["y"] - 48, "Render distance", 7)
        self.rdist_btn_down = ArrowButton(self.middle["x"], self.middle["y"] - 50, 8, 8, 7, "", 7, lambda: self.change_render_distance("down"), "down")
        self.rdist_btn_down.draw()
        pyxel.text(self.middle["x"] + 14, self.middle["y"] - 48, f"{self.render_distance}", 7)
        self.rdist_btn_up = ArrowButton(self.middle["x"] + 32, self.middle["y"] - 50, 8, 8, 7, "", 7, lambda: self.change_render_distance("up"), "up")
        self.rdist_btn_up.draw()

        # Frame rate
        pyxel.text(self.middle["x"] - 64, self.middle["y"] - 32, "Frame rate", 7)
        self.frate_btn_down = ArrowButton(self.middle["x"], self.middle["y"] - 34, 8, 8, 7, "", 7, lambda: self.change_frame_rate("down"), "down")
        self.frate_btn_down.draw()
        pyxel.text(self.middle["x"] + 14, self.middle["y"] - 32, f"{self.config.get('config.frame_rate')}", 7)
        self.frate_btn_up = ArrowButton(self.middle["x"] + 32, self.middle["y"] - 34, 8, 8, 7, "", 7, lambda: self.change_frame_rate("up"), "up")
        self.frate_btn_up.draw()

        # Resolution
        pyxel.text(self.middle["x"] - 64, self.middle["y"] - 16, "Resolution", 7)
        self.res_btn_down = ArrowButton(self.middle["x"], self.middle["y"] - 18, 8, 8, 7, "", 7, lambda: self.change_resolution("down"), "down")
        self.res_btn_down.draw()
        pyxel.text(self.middle["x"] + 14, self.middle["y"] - 16, f"{self.resolution[0]}x{self.resolution[1]}", 7)
        self.res_btn_up = ArrowButton(self.middle["x"] + 48, self.middle["y"] - 18, 8, 8, 7, "", 7, lambda: self.change_resolution("up"), "up")
        self.res_btn_up.draw()

        # Save and close
        if (
          self.resolution != self.config.get("config.resolution").split("x")
        ) or (
          math.ceil(pyxel.frame_count / (time.time() - self.started_time)) != self.config.get("config.frame_rate")
        ):
          pyxel.text(self.middle["x"] - 64, self.middle["y"], "Need restart", 8)
        self.save_button = Button(self.middle["x"] - 32, self.middle["y"] + 16, 64, 16, 7, "Save and close", 7, self.save_settings)
        self.save_button.draw()

        
      return
    
    # Draw elements
    self.renderer.draw()

    # Draw debug
    if self.debug:
      # Draw minimap
      for y, row in enumerate(self.map):
        for x, tile in enumerate(row):
          pyxel.rect(x * self.floor_size, y * self.floor_size, self.floor_size, self.floor_size, self.colors[tile])
      pyxel.rect(self.player.x * self.floor_size, self.player.y * self.floor_size, self.floor_size, self.floor_size, 9)

      # Profiling
      pyxel.text(pyxel.width - 48, 4, f"{self.player.x}, {self.player.y}", 7)
      pyxel.text(pyxel.width - 48, 12, f"{"North" if self.player.orientation == 0 else "East" if self.player.orientation == 90 else "South" if self.player.orientation == 180 else "West"}", 7)
      pyxel.text(pyxel.width - 48, 20, f"{(pyxel.frame_count/(time.time() - self.started_time)):.2f} FPS", 7)

  # Button actions
  def settings(self):
    self.settings_shown = not self.settings_shown
  
  def change_render_distance(self, direction):
    if direction == "up":
      self.render_distance += 1
    else:
      self.render_distance = max(1, self.render_distance - 1)
  
  def change_frame_rate(self, direction):
    framerates = [ 30, 60, 120, 144, 165, 240 ]
    if direction == "up":
      self.config.set("config.frame_rate", framerates[(framerates.index(self.config.get("config.frame_rate")) + 1) % len(framerates)])
    else:
      self.config.set("config.frame_rate", framerates[(framerates.index(self.config.get("config.frame_rate")) - 1) % len(framerates)])

  def change_resolution(self, direction):
    resolutions = [ "640x360", "1280x720", "1920x1080" ]
    index = resolutions.index(f"{self.resolution[0]}x{self.resolution[1]}")
    self.resolution = resolutions[(index + 1) % len(resolutions) if direction == "up" else (index - 1) % len(resolutions)].split("x")
  
  def save_settings(self):
    self.config.set("config.render_distance", self.render_distance)
    self.config.set("config.frame_rate", self.config.get("config.frame_rate"))
    self.config.set("config.resolution", f"{self.resolution[0]}x{self.resolution[1]}")
    self.settings_shown = False
    self.renderer = Renderer(self.player, self.map, self.colors, self.middle, self.wall_height, self.render_distance, self.max_walls)

if __name__ == "__main__":
  App()