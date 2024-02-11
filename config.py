import yaml

class Config:
  def __init__(self):
    with open("assets/config.yaml", "r") as file:
      self.data = yaml.safe_load(file)
  
  def get(self, key):
    keys = key.split(".")
    value = self.data
    for key in keys:
      value = value[key]
    return value