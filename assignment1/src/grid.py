import numpy
import random

# A Grid class which holds a numpy array representing a 2D square grid with
# integer values. The values in this class have no semantic meaning.
class Grid:
	# array parameter should be a numpy ndarray
	def __init__(self, array):
		assert(array.shape[0] == array.shape[1])
		self.array = array

	# Create a grid object from a file of a grid with the following representation:
	# An integer representing the size of the grid followed by a newline
	# The rows of the grid separated by newlines, with each element of the row
	# separated by a space
	@classmethod
	def grid_from_file(cls, file_name):
		array = None
		
		with open(file_name) as f:
			# read first line and determine shape
			lines = f.readlines()
			size = int(lines[0].strip())

			shape = (size, size)
			array = numpy.empty(shape, dtype=int)

			for (row,line) in enumerate(lines[1:]):
				line = line.strip().split(' ')
				line = [int(x) for x in line]
				array[row] = line

		return cls(array)

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





