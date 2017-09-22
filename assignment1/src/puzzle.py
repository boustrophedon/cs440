import numpy
import scipy
import scipy.sparse

from grid import Grid, grid_from_file

DEFAULT_SIZE = 5

class PuzzleGrid:
	# If size is passed, generate a random puzzle of size `size`
	# If input_file is passed, read in a puzzle from the given file
	#
	# self.grid is a Grid with values representing how many squares in the
	# cardinal directions we can move
	# 
	# self.adj_graph is a sparse scipy matrix representing the graph formed by
	# the possible moves of the grid
	def __init__(self, size=DEFAULT_SIZE, input_file=None):
		if input_file is None:
			self.grid = self.random_grid(size)
		else:
			self.grid = grid_from_file(input_file)
			# Todo: validate grid

		self.adj_graph = graphize(self.grid)
		self.value, self.distances = self._evaluate()

	# Returns the value of the grid puzzle at point (x,y)
	def get(self, x, y):
		return self.grid.get(x,y)

	def size(self):
		return self.grid.size()

	def value(self):
		return self.value

	def random_grid(self, size):
		result = numpy.empty((size, size), dtype=int)

		n = size
		for x in range(0, n):
			for y in range(0, n):
				result[x,y] = random.randint(1, numpy.amax([n - x, x - n]))
		result[n - 1, n - 1] = 0
		return Grid(result)

	# Returns a grid with each element's value representing the distance from
	# the start
	def distances(self):
		return self.distances

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
		
		out.append(str(self.distances))
		out.append(str(self.value))

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
