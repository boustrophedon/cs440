import scipy

from grid import Grid, random_grid, grid_from_file

DEFAULT_SIZE = 5

class PuzzleGrid:
	def __init__(self, size=DEFAULT_SIZE, input_file=None):
		if input_file is None:
			self.grid = random_grid(size)
		else:
			self.grid = grid_from_file(input_file)

		self.adj_graph = self.graphize(self.grid)


	# Returns the value of the grid puzzle at point (x,y)
	def get(self, x, y):
		return self.grid.get(x,y)

	def size(self):
		return self.grid.size()

	def value(self):
		pass
