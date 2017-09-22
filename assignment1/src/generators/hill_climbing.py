from grid import Grid
from puzzle import random_puzzle

class HillClimbingGenerator:
	def __init__(self, size, iters):
		self.grid = random_puzzle(size)
