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
		self.do_evaluate()

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
	# Returns the coordinate of the element that was changed, and the previous
	# value at that coordinate
	def change_random_entry(self):
		x = random.randint(0, self.size()-1)
		y = random.randint(0, self.size()-1)
		old = self.get(x,y)

		self.set(x,y, self.get_random_value(x, y))
		self.do_evaluate()
		return (x,y,old)

	# Returns the value of the grid puzzle at point (x,y)
	def get(self, x, y):
		return self.grid.get(x,y)

	# Sets the entry of the grid puzzle at point (x,y) to val
	# If you are going to change a lot of the grid's elements before looking at
	# the puzzle's value, consider cloning the grid and making a new PuzzleGrid
	def set(self, x, y, val):
		n = self.size()
		xdiff = max(n - x - 1, x)
		ydiff = max(n - y - 1, y)
		if val > max(xdiff, ydiff) or val <= 0:
			raise ValueError("Invalid puzzle entry at ({}, {}): {}", x, y, val)

		self.grid[x,y] = val
		
		# Fix up adjacency graph and recompute distances/values
		set_neighbors(self.grid, self.adj_graph, x, y, n)
		self.do_evaluate()

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

	# Note that this does not fix the adjacency matrix if you messed with the
	# internal structure of the grid without using set or __set__
	def do_evaluate(self):
		self._value, self._distances = self._evaluate()

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

	def __getitem__(self, idx):
		assert(len(idx) == 2)
		return self.get(idx[0], idx[1])

	def __setitem__(self, idx, val):
		assert(len(idx) == 2)
		self.set(idx[0], idx[1], val)

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
	for x in range(0, n):
		for y in range(0, n):
			set_neighbors(grid, adj, x, y, n)

	return adj

def set_neighbors(grid, graph, x, y, n):
	idx = y*n + x
	graph[idx] = 0

	offset = grid[x, y]
	
	if x-offset >= 0:
		idx2 = y*n + (x-offset)
		graph[idx, idx2] = 1
	if x+offset < n:
		idx2 = y*n + (x+offset)
		graph[idx, idx2] = 1

	if y-offset >= 0:
		idx2 = (y-offset)*n + x
		graph[idx, idx2] = 1
	if y+offset < n:
		idx2 = (y+offset)*n + x
		graph[idx, idx2] = 1
