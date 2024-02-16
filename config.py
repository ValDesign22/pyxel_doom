import os
import yaml

class Config:
  def __init__(self, dev_mode=False):
    gamefolder = "" if dev_mode else os.path.dirname(os.path.realpath(__file__)) + "/"
    self.configfile = gamefolder + "assets/config.yaml"
    if not os.path.exists(self.configfile):
      with open(self.configfile, "w") as file:
        file.write("config:\n  resolution: 640x360\n  frame_rate: 30\n  render_distance: 10\n  max_walls: 10\n  fullscreen: false\ncolors:\n  _: 7\n  #: 8\nassets:\n  map: assets/map.txt\n")
    
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