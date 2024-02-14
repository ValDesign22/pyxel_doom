import os
import yaml

class Config:
  def __init__(self):
    if not os.path.exists("assets/config.yaml"):
      with open("assets/config.yaml", "w") as file:
        file.write("config:\n  resolution: 256x256\n  frame_rate: 30\n  render_distance: 10\n  max_walls: 10\n  fullscreen: false\ncolors:\n  _: 7\n  #: 8\nassets:\n  map: assets/map.txt\n")
    
    with open("assets/config.yaml", "r") as file:
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
    with open("assets/config.yaml", "w") as file:
      yaml.dump(self.data, file)
    return value