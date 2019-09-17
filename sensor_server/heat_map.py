import numpy as np

class HeatMap:

    def __init__(self, height, width, growth_rate, decay_rate):

        self.height = height
        self.width = width

        self.growth_rate = growth_rate
        self.decay_rate = decay_rate

        self.MAX_GROWTH_RATE = 30

        self.heat_map = np.zeros((height, width), dtype=np.uint8)

    def increment_tiles(self, binary_array):

        for i in range(len(binary_array)):
            for j in range(len(binary_array[i])):

                #Grow heat map
                if binary_array[i, j] == 255:

                    if self.heat_map[i, j] + self.growth_rate > 255:
                        self.heat_map[i, j] = 255
                    else:
                        self.heat_map[i, j] += self.growth_rate

                #Decay heat map
                if self.heat_map[i, j] - self.decay_rate < 0:
                    self.heat_map[i, j] = 0
                else:
                    self.heat_map[i, j] -= self.decay_rate

    def increment_growth_rate(self, amount):

        if amount < 0:

            if self.growth_rate + amount <= 0:
                self.growth_rate = 0
            else:
                self.growth_rate += amount

        else:

            if self.growth_rate + amount > self.MAX_GROWTH_RATE:
                self.growth_rate = self.MAX_GROWTH_RATE
            else:
                self.growth_rate += amount

        print("Growth rate:", self.growth_rate)
