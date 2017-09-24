from grid import Grid

from .hill_climbing import HillClimbingGenerator

class RandomRestartsGenerator:
	def __init__(self, size):
		self.size = size

	# Runs the generator for the specified number of iterations
	# iters is the number of iterations to do for each hillclimbing run.
	# restarts is the number of times we do a hillclimbing run. 
	#
	# If report is true, print statistics on generation as it is running.
	# Typically this will be size,current_iteration,max_iterations,value,method
	#
	# Returns a tuple of the grid with the highest value and its value
	def generate(self, iters, restarts, report=False):
		best_grid,best_value = HillClimbingGenerator(self.size).generate(iters,report=report)
		for i in range(1, restarts):
			grid, value = HillClimbingGenerator(self.size).generate(iters,report=report)
			if value >= best_value:
				best_grid = grid
				best_value = value

		return (best_grid, best_value)
