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
  
  def set(self, key, value):
    keys = key.split(".")
    data = self.data
    for key in keys[:-1]:
      data = data[key]
    data[keys[-1]] = value
    with open("assets/config.yaml", "w") as file:
      yaml.dump(self.data, file)
    return value