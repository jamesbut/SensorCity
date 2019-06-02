import numpy as np

class HeatMap:

	def __init__(self, height, width):
		self.height = height
		self.width = width

		self.colour_increment = 10

		self.heat_map = np.zeros((height, width), dtype=np.uint8)

	def increment_tiles(self, binary_array):
		for i in range(len(binary_array)):
			for j in range(len(binary_array[i])):
				if binary_array[i, j] == 255:
					if self.heat_map[i, j] + self.colour_increment < 255: 
						self.heat_map[i, j] += 10
