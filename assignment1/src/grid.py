import numpy

# A Grid class which holds a numpy array representing a 2D square grid with
# integer values. The values in this class have no semantic meaning.
class Grid:
	# array parameter should be a numpy ndarray
	def __init__(self, array):
		assert(array.shape[0] == array.shape[1])
		self.array = array

	def get(self, x, y):
		return self.array[x,y]

	def set(self, x, y, value):
		self.array[x,y] = value

	def size(self):
		return self.array.shape[0]

	# Returns the underlying numpy array
	def get_raw(self):
		return self.array

	def __getitem__(self, idx):
		assert(len(idx) == 2)
		return self.get(idx[0], idx[1])

	def __setitem__(self, idx, val):
		assert(len(idx) == 2)
		self.set(idx[0], idx[1], val)

	def __str__(self):
		out = list()

		n = self.size()
		for x in range(0,n):
			line = list()
			for y in range(0,n):
				v = self.array[x,y]
				if v != -1: v = str(int(v));
				else: v = "X";
				line.append(v)
			out.append(" ".join(line))
		return "\n".join(out)

# this is not actually useful for our project currently with the semantics of
# Grid. the random puzzles we want have semantics regarding which values are
# valid.
def random_grid(size):
	pass

# Create a grid object from a file of a grid represented with the elements
# separated by spaces and each row separated by a newline
def grid_from_file(file_name):
	array = None

	with open(file_name) as f:
		# read first line and determine shape
		lines = f.readlines()
		first = lines[0].strip().split(' ')
		size = len(first)

		shape = (size, size)
		array = numpy.empty(shape, dtype=int)

		for (row,line) in enumerate(lines):
			line = line.strip().split(' ')
			line = [int(x) for x in line]
			array[row] = line

	return Grid(array)


