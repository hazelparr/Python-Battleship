class Ships:
	def __init__(self, ship_type, size):
		self.ship_type = ship_type
		self.positions = []
		self.orientation = None
		self.size = size
		self.health = size