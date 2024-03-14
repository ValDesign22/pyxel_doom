class Item():
	def __init__(self, name):
		self.name = name

class DoorKey(Item):
	def __init__(self, name, door, position):
		super().__init__(name)
		self.door = door # (x, y)
		self.x = position[0]
		self.y = position[1]
		self.collected = False

	def collect(self, player, map):
		if player.x == self.x and player.y == self.y and not self.collected:
			self.collected = True
			map[self.y] = map[self.y][:self.x] + " " + map[self.y][self.x + 1:]
			return True
		return False