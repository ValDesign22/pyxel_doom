import math
import pyxel
import time

from button import ArrowButton, Button
from config import Config
from item import DoorKey
from player import Player
from renderer import Direction, Renderer

class App:
  def __init__(self):
    self.dev_mode = True
    self.config = Config(self.dev_mode)
    self.resolution = self.config.get("config.resolution").split("x")

    pyxel.init(
      width=int(self.resolution[0]),
      height=int(self.resolution[1]),
      title="Pyxel",
      fps=self.config.get("config.frame_rate")
    )

    # Map
    self.colors = self.config.get("colors")
    self.middle = { "x": pyxel.width // 2, "y": pyxel.height // 2 }
    self.floor_size = pyxel.width // pyxel.height * 4
    self.wall_height = pyxel.height // 2
    self.map = open(self.config.get("assets.map")).read().split("\n")
    
    # Player
    self.player = Player(len(self.map[0]) // 2, len(self.map) // 2, 0, self.map, self.config.get("config.player_speed"))
    if self.map[self.player.y][self.player.x] == "#":
      for y, row in enumerate(self.map):
        for x, tile in enumerate(row):
          if tile == " ":
            self.player.x = x
            self.player.y = y
            break
        else:
          continue
        break
    self.block = (x:= self.player.x, y:= self.player.y)

    # Parameters
    self.debug = False
    self.render_distance = self.config.get("config.render_distance")
    self.started_time = time.time()
    self.counter = 0
    self.fps = self.config.get("config.frame_rate")
    self.game_paused = False
    self.settings_shown = False
    self.current_button = 0
    self.gamepad_pressed = False
    self.max_walls = self.config.get("config.max_walls")
    self.fullscreen = self.config.get("config.fullscreen")

    self.renderer = Renderer(self.player, self.map, self.colors, self.middle, self.wall_height, self.render_distance, self.max_walls)

    # Buttons
    self.settings_button = Button(self.middle["x"] - 42, self.middle["y"] - 40, 64, 16, 7, "Settings", 7, self.settings)
    self.quit_button = Button(self.middle["x"] - 42, self.middle["y"] - 16, 64, 16, 7, "Quit", 7, pyxel.quit)
    self.save_button = Button(self.middle["x"] - 32, self.middle["y"] + 16, 64, 16, 7, "Save and close", 7, self.save_settings)

    # Settings Buttons
    self.rdist_btn_down = ArrowButton(self.middle["x"], self.middle["y"] - 50, 8, 8, 7, 7, lambda: self.change_render_distance("down"), "down")
    self.rdist_btn_up = ArrowButton(self.middle["x"] + 32, self.middle["y"] - 50, 8, 8, 7, 7, lambda: self.change_render_distance("up"), "up")
    self.frate_btn_down = ArrowButton(self.middle["x"], self.middle["y"] - 34, 8, 8, 7, 7, lambda: self.change_frame_rate("down"), "down")
    self.frate_btn_up = ArrowButton(self.middle["x"] + 32, self.middle["y"] - 34, 8, 8, 7, 7, lambda: self.change_frame_rate("up"), "up")
    self.res_btn_down = ArrowButton(self.middle["x"], self.middle["y"] - 18, 8, 8, 7, 7, lambda: self.change_resolution("down"), "down")
    self.res_btn_up = ArrowButton(self.middle["x"] + 48, self.middle["y"] - 18, 8, 8, 7, 7, lambda: self.change_resolution("up"), "up")

    self.doorkey = DoorKey("Key 1", (4, 20), (5, 5))

    pyxel.fullscreen(self.fullscreen)
    pyxel.run(self.update, self.draw)

  # Game loop
  def update(self):
    self.counter += 1
    if (time.time() - self.started_time) > 1:
      self.fps = self.counter / (time.time() - self.started_time)
      self.counter = 0
      self.started_time = time.time()

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
      # Mouse click
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

      # Keyboard and gamepad
      if self.settings_shown == False:
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
          self.game_paused = False
          pyxel.mouse(False)
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) or pyxel.btnp(pyxel.KEY_Z):
          self.gamepad_pressed = True
          self.current_button = (self.current_button + 1) % 2
        elif pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btnp(pyxel.KEY_S):
          self.gamepad_pressed = True
          self.current_button = (self.current_button - 1) % 2
        elif pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.KEY_SPACE):
          if self.current_button == 0:
            self.settings_button.is_clicked(self.settings_button.x + 1, self.settings_button.y + 1)
          else:
            self.quit_button.is_clicked(self.quit_button.x + 1, self.quit_button.y + 1)
          self.current_button = 0
      else:
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) or pyxel.btnp(pyxel.KEY_Z):
          self.gamepad_pressed = True
          self.current_button = (self.current_button + 1) % 4
        elif pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btnp(pyxel.KEY_S):
          self.gamepad_pressed = True
          self.current_button = (self.current_button - 1) % 4
        elif pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or pyxel.btnp(pyxel.KEY_Q):
          if self.current_button == 0:
            self.rdist_btn_down.is_clicked(self.rdist_btn_down.x + 1, self.rdist_btn_down.y + 1)
          elif self.current_button == 1:
            self.frate_btn_down.is_clicked(self.frate_btn_down.x + 1, self.frate_btn_down.y + 1)
          elif self.current_button == 2:
            self.res_btn_down.is_clicked(self.res_btn_down.x + 1, self.res_btn_down.y + 1)
        elif pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or pyxel.btnp(pyxel.KEY_D):
          if self.current_button == 0:
            self.rdist_btn_up.is_clicked(self.rdist_btn_up.x + 1, self.rdist_btn_up.y + 1)
          elif self.current_button == 1:
            self.frate_btn_up.is_clicked(self.frate_btn_up.x + 1, self.frate_btn_up.y + 1)
          elif self.current_button == 2:
            self.res_btn_up.is_clicked(self.res_btn_up.x + 1, self.res_btn_up.y + 1)
        elif pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.KEY_SPACE):
          if self.current_button == 3:
            self.save_button.is_clicked(self.save_button.x + 1, self.save_button.y + 1)
          self.current_button = 0
      return

    # Player movement
    if pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
      self.player.move(1)
    if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
      self.player.move(-1)
    if pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
      self.player.rotate(-1)
    if pyxel.btnp(pyxel.KEY_D) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
      self.player.rotate(1)
    self.player.sprint(pyxel.btn(pyxel.KEY_LSHIFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_X))

    self.player.x = max(0, min(len(self.map[0]) - 1, self.player.x))
    self.player.y = max(0, min(len(self.map) - 1, self.player.y))

    block_x, block_y = self.player.x, self.player.y
    if self.player.orientation == Direction.NORTH: block_y -= 1
    elif self.player.orientation == Direction.EAST: block_x += 1
    elif self.player.orientation == Direction.SOUTH: block_y += 1
    elif self.player.orientation == Direction.WEST: block_x -= 1
    if block_x < 0 or block_x >= len(self.map[0]) or block_y < 0 or block_y >= len(self.map): return
    if self.map[block_y][block_x] == "D":
      if pyxel.btnp(pyxel.KEY_E) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y):
        self.map[block_y] = self.map[block_y][:block_x] + " " + self.map[block_y][block_x + 1:] 

  def draw(self):
    pyxel.cls(0)

    # Pause and settings menu
    if self.game_paused:
      # Draw buttons
      if self.settings_shown == False:
        pyxel.text(self.middle["x"] - 32, self.middle["y"] - 64, "Game Paused", 7)

        self.settings_button.draw()
        self.quit_button.draw()
        if self.gamepad_pressed:
          self.settings_button.focus() if self.current_button == 0 else self.quit_button.focus()

        if pyxel.mouse_x > self.middle["x"] - 42 and pyxel.mouse_x < self.middle["x"] + 22 and pyxel.mouse_y > self.middle["y"] - 40 and pyxel.mouse_y < self.middle["y"] - 24:
          self.current_button = 0
          self.gamepad_pressed = False
          self.settings_button.focus()
        elif pyxel.mouse_x > self.middle["x"] - 42 and pyxel.mouse_x < self.middle["x"] + 22 and pyxel.mouse_y > self.middle["y"] - 16 and pyxel.mouse_y < self.middle["y"]:
          self.current_button = 1
          self.gamepad_pressed = False
          self.quit_button.focus()

      else:
        # Render distance
        pyxel.text(self.middle["x"] - 32, self.middle["y"] - 64, "Settings", 7)
        pyxel.text(self.middle["x"] - 64, self.middle["y"] - 48, "Render distance", 7)
        self.rdist_btn_down.draw()
        pyxel.text(self.middle["x"] + 14, self.middle["y"] - 48, f"{self.render_distance}", 7)
        self.rdist_btn_up.draw()

        # Frame rate
        pyxel.text(self.middle["x"] - 64, self.middle["y"] - 32, "Frame rate", 7)
        self.frate_btn_down.draw()
        pyxel.text(self.middle["x"] + 14, self.middle["y"] - 32, f"{self.config.get('config.frame_rate')}", 7)
        self.frate_btn_up.draw()

        # Resolution
        pyxel.text(self.middle["x"] - 64, self.middle["y"] - 16, "Resolution", 7)
        self.res_btn_down.draw()
        pyxel.text(self.middle["x"] + 14, self.middle["y"] - 16, f"{self.resolution[0]}x{self.resolution[1]}", 7)
        self.res_btn_up.draw()

        # Save and close
        if (
          self.resolution != self.config.get("config.resolution").split("x")
        ) or (
          math.ceil(self.fps) != self.config.get("config.frame_rate")
        ):
          pyxel.text(self.middle["x"] - 64, self.middle["y"], "Need restart", 8)
        self.save_button.draw()

        # Focus
        if self.gamepad_pressed:
          if self.current_button == 0:
            self.rdist_btn_down.focus()
            self.rdist_btn_up.focus()
          elif self.current_button == 1:
            self.frate_btn_down.focus()
            self.frate_btn_up.focus()
          elif self.current_button == 2:
            self.res_btn_down.focus()
            self.res_btn_up.focus()
          elif self.current_button == 3:
            self.save_button.focus()

        if pyxel.mouse_x > self.middle["x"] and pyxel.mouse_x < self.middle["x"] + 8 and pyxel.mouse_y > self.middle["y"] - 50 and pyxel.mouse_y < self.middle["y"] - 42:
          self.current_button = 0
          self.gamepad_pressed = False
          self.rdist_btn_down.focus()
        elif pyxel.mouse_x > self.middle["x"] + 32 and pyxel.mouse_x < self.middle["x"] + 40 and pyxel.mouse_y > self.middle["y"] - 50 and pyxel.mouse_y < self.middle["y"] - 42:
          self.current_button = 0
          self.gamepad_pressed = False
          self.rdist_btn_up.focus()
        elif pyxel.mouse_x > self.middle["x"] and pyxel.mouse_x < self.middle["x"] + 8 and pyxel.mouse_y > self.middle["y"] - 34 and pyxel.mouse_y < self.middle["y"] - 26:
          self.current_button = 1
          self.gamepad_pressed = False
          self.frate_btn_down.focus()
        elif pyxel.mouse_x > self.middle["x"] + 32 and pyxel.mouse_x < self.middle["x"] + 40 and pyxel.mouse_y > self.middle["y"] - 34 and pyxel.mouse_y < self.middle["y"] - 26:
          self.current_button = 1
          self.gamepad_pressed = False
          self.frate_btn_up.focus()
        elif pyxel.mouse_x > self.middle["x"] and pyxel.mouse_x < self.middle["x"] + 8 and pyxel.mouse_y > self.middle["y"] - 18 and pyxel.mouse_y < self.middle["y"] - 10:
          self.current_button = 2
          self.gamepad_pressed = False
          self.res_btn_down.focus()
        elif pyxel.mouse_x > self.middle["x"] + 48 and pyxel.mouse_x < self.middle["x"] + 56 and pyxel.mouse_y > self.middle["y"] - 18 and pyxel.mouse_y < self.middle["y"] - 10:
          self.current_button = 2
          self.gamepad_pressed = False
          self.res_btn_up.focus()
        elif pyxel.mouse_x > self.middle["x"] - 32 and pyxel.mouse_x < self.middle["x"] + 32 and pyxel.mouse_y > self.middle["y"] + 16 and pyxel.mouse_y < self.middle["y"] + 32:
          self.current_button = 3
          self.save_button.focus()
          self.gamepad_pressed = False

      return
    
    # Draw elements
    self.renderer.draw()
    
    block_x, block_y = self.player.x, self.player.y
    if self.player.orientation == Direction.NORTH: block_y -= 1
    elif self.player.orientation == Direction.EAST: block_x += 1
    elif self.player.orientation == Direction.SOUTH: block_y += 1
    elif self.player.orientation == Direction.WEST: block_x -= 1
    if block_x < 0 or block_x >= len(self.map[0]) or block_y < 0 or block_y >= len(self.map): return
    if self.map[block_y][block_x] == "D":
     pyxel.text(self.middle["x"] - 20, self.middle["y"] + 64, "[E] Open door", 7)

    # Draw debug
    if self.debug:
      # Profiling
      pyxel.text(pyxel.width - 48, 4, f"{self.player.x}, {self.player.y}", 7)
      pyxel.text(pyxel.width - 48, 12, f"{"North" if self.player.orientation == 0 else "East" if self.player.orientation == 90 else "South" if self.player.orientation == 180 else "West"}", 7)
      pyxel.text(pyxel.width - 48, 20, f"{math.ceil(self.fps)} FPS", 7)

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