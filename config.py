import os
import yaml

class Config:
  def __init__(self, dev_mode=False):
    gamefolder = "" if dev_mode else os.path.dirname(os.path.realpath(__file__)) + "/"
    self.configfile = gamefolder + "assets/config.yaml"
    if not os.path.exists(self.configfile):
      with open(self.configfile, "w") as file:
        file.write(
"""
config:
  resolution: 640x360
  frame_rate: 30
  render_distance: 10
  max_walls: 10
  fullscreen: false
  player_speed: 10
colors:
  ' ': 0
  '#': 4
  'D': 7
assets:
  map: assets/map.txt
  resources: assets/resources.pyxres
""")
    
    with open(self.configfile, "r") as file:
      self.data = yaml.safe_load(file)
  
  def get(self, key):
    keys = key.split(".")
    value = self.data
    for key in keys:
      value = value[key]
    return value
  
  def set(self, key, value):
    keys = key.split(".")
    data = self.data
    for key in keys[:-1]:
      data = data[key]
    data[keys[-1]] = value
    with open(self.configfile, "w") as file:
      yaml.dump(self.data, file)
    return value