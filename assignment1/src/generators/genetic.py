import numpy.random

from grid import Grid
from puzzle import PuzzleGrid

class GeneticGenerator:
	def __init__(self, size):
		self.population = list()
		self.size = size

	def generate(self, iters, population_size):
		for i in range(0, population_size):
			self.population.append(PuzzleGrid.random_puzzle(self.size))

		for i in range(0, iters):
			# if the puzzle has a negative value, make it very unlikely to be chosen
			vals = [max(-0.001*p.value(), p.value()) for p in self.population]
			total = sum(vals)

			# probability a given puzzle is chosen during selection is higher
			# if value is higher. this is different than the example with
			# n-queens given in class, where we wanted to minimize the
			# evaluation function so we inverted the values.
			p_vals = [v/total for v in vals]

			# To reduce computation, crossover and mutation are done on the
			# raw numpy arrays and then turned back into puzzlegrids.
			# Probably should use the PuzzleGrid.clone_grid() method but we
			# don't actually need the old puzzles so we can just use their
			# grids.
			grids = [p.grid.get_raw() for p in self.population]
			# do selection with given probability distribution
			selected = numpy.random.choice(len(grids), len(grids), replace=True, p=p_vals)

			for i in range(0, len(self.population)):
				idx1, idx2 = numpy.random.choice(selected, 2)
				g1, g2 = grids[idx1], grids[idx2]
				self.population[i] = mutate(crossover(g1, g2))

		best = max(self.population, key=lambda p:p.value())
		return (best.clone_grid(), best.value())

# Given two 2d numpy arrays, produce "offspring" of them by selecting a row at
# random and combining them from the given row
def crossover(g1, g2):
	cutoff = numpy.random.choice(g1.shape[0])
	g1[cutoff:] = g2[cutoff:]

	return PuzzleGrid(Grid(g1))

def mutate(p):
	p.change_random_entry()

	return p
