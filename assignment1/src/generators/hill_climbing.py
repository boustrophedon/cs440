from grid import Grid
from puzzle import PuzzleGrid

class HillClimbingGenerator:
	def __init__(self, size, iters):
		self.grid = PuzzleGrid.random_puzzle(size)
