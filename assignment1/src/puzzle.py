import copy
import random

import numpy
import scipy
import scipy.sparse

from grid import Grid

class PuzzleGrid:
	# Input: grid, an instance of Grid that represents a puzzle
	#
	# self.grid is a Grid with values representing how many squares in the
	# cardinal directions we can move
	# 
	# self.adj_graph is a sparse scipy matrix representing the graph formed by
	# the possible moves of the grid
	def __init__(self, grid):
		# Todo: validate grid
		self.grid = grid

		self.adj_graph = graphize(self.grid)
		self._value, self._distances = self._evaluate()

	@classmethod
	def from_file(cls, input_file):
		grid = Grid.grid_from_file(input_file)
		return cls(grid)

	@classmethod
	def random_puzzle(cls, size):
		result = numpy.empty((size, size), dtype=int)

		n = size
		for x in range(0, n):
			for y in range(0, n):
				result[x,y] = cls._get_random_value(n, x, y)
		result[n - 1, n - 1] = 0
		return cls(Grid(result))

	# Given an x and y coordinate on the grid, return a random value for the
	# puzzle that is valid at that coordinate
	def get_random_value(self, x, y):
		return PuzzleGrid._get_random_value(self.size(), x, y)

	@staticmethod
	def _get_random_value(n, x, y):
		assert(0 <= x < n)
		assert(0 <= y < n)
		# n - x - 1 is the distance to the right edge
		# x's range is [0,(n-1)], so if x == n-1 then n - x = 1 and we
		# technically want to be able to reach 0 (though in actuality we do not ever accept 0)
		#
		# x is the distance to the left edge
		xdiff = max(n - x - 1, x)
		# same reasoning for y coordinate
		ydiff = max(n - y - 1, y)
		return random.randint(1, max(xdiff, ydiff))

	# Changes one element of the grid to a valid value at random
	#
	# Returns the coordinate of the element that was changed
	def change_random_entry(self):
		x = random.randint(0, self.size()-1)
		y = random.randint(0, self.size()-1)

		self.grid[x,y] = self.get_random_value(x, y)
		self._value, self._distances = self._evaluate()
		return (x,y)

	# Returns the value of the grid puzzle at point (x,y)
	def get(self, x, y):
		return self.grid.get(x,y)

	# Returns a copy of the underlying Grid object
	def clone_grid(self):
		return copy.deepcopy(self.grid)

	def size(self):
		return self.grid.size()

	def value(self):
		return self._value

	# Returns a grid with each element's value representing the distance from
	# the start
	def distances(self):
		return self._distances

	# Returns a tuple of the value and a grid with elements representing the
	# number of moves it takes to reach that position in the original puzzle
	def _evaluate(self):
		# use dijkstra's to find the distances from 0 to each of the
		# other places in the grid
		distances = scipy.sparse.csgraph.dijkstra(self.adj_graph, True, 0, False, True)

		distances[distances == numpy.inf] = -1
		dist_grid = Grid(distances.reshape((self.size(), self.size())))
		# the goal will always be the last element of the distances array
		# if its value is -1, it cannot be reached
		if (distances[-1] != -1):
			return (int(distances[-1]), dist_grid)
		else:
			unreachable = -(distances == -1).sum()
			return (unreachable, dist_grid)

	def __str__(self):
		out = list()

		out.append(str(self.grid))
		
		out.append(str(self.distances()))
		out.append(str(self.value()))

		return "\n\n".join(out)

# Given a grid, turn it into a graph represented by a (sparse) adjacency
# matrix
def graphize(grid):
	n = grid.size()
	size = n*n
	
	adj = scipy.sparse.lil_matrix((size, size))

	# adjacency matrix for graph we create has indices in row major order
	for row in range(0, n):
		for col in range(0, n):
			adj_ind = col*n + row

			# col, row is correct here: x value is the column y
			# value is the row. I probably should change the whole
			# thing tbh
			offset = grid[col, row]
			
			if row-offset >= 0:
				adj_ind2 = col*n + (row-offset)
				adj[adj_ind, adj_ind2] = 1
			if row+offset < n:
				adj_ind2 = col*n + (row+offset)
				adj[adj_ind, adj_ind2] = 1

			if col-offset >= 0:
				adj_ind2 = (col-offset)*n + row
				adj[adj_ind, adj_ind2] = 1
			if col+offset < n:
				adj_ind2 = (col+offset)*n + row
				adj[adj_ind, adj_ind2] = 1

	return adj
