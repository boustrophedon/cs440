from copy import deepcopy

from grid import Grid
from puzzle import PuzzleGrid

class HillClimbingGenerator:
	def __init__(self, size):
		self.puzzle = PuzzleGrid.random_puzzle(size)

	# Runs the generator for the specified number of iterations
	# iters is the number of iterations to run.
	#
	# If report is true, print statistics on generation as it is running.
	# Typically this will be size,current_iteration,max_iterations,value,method
	#
	# Returns a tuple of the grid with the highest value and its value
	def generate(self, iters, report=False):
		prev = self.puzzle.value()

		for i in range(0, iters):
			x,y,old = self.puzzle.change_random_entry()
			if self.puzzle.value() < prev:
				self.puzzle[x,y] = old
			else:
				prev = self.puzzle.value()
		return (self.puzzle.clone_grid(), self.puzzle.value())
