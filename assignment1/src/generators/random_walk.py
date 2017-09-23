from copy import deepcopy
import random

from grid import Grid
from puzzle import PuzzleGrid

class RandomWalkGenerator:
	def __init__(self, size):
		self.puzzle = PuzzleGrid.random_puzzle(size)

	# Runs the generator for the specified number of iterations
	# iters is the number of iterations to run.
	# p is the probability of accepting a move that reduces the value of the
	# puzzle
	#
	# If report is true, print statistics on generation as it is running.
	# Typically this will be size,current_iteration,max_iterations,value,method
	#
	# Returns a tuple of the grid with the highest value and its value
	def generate(self, iters, p, report=False):
		prev = self.puzzle.value()

		for i in range(0, iters):
			x,y,old = self.puzzle.change_random_entry()
			# if we've made a bad move, then accepting with probability p is
			# the same as not accepting with probability 1-p
			if self.puzzle.value() < prev and random.random() < 1-p:
				self.puzzle[x,y] = old
			else:
				prev = self.puzzle.value()
		return (self.puzzle.clone_grid(), self.puzzle.value())
