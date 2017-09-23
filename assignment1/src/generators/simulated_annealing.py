from grid import Grid
from puzzle import PuzzleGrid
import math
import random


class SimulatedAnnealingGenerator:
	# Took out , iters, start_temp, decay_rate):
	def __init__(self, size):
		self.puzzle = PuzzleGrid.random_puzzle(size)

	def generate(self, iters, start_temp, decay_rate):
		old_value = self.puzzle.value()
		# p = self.puzzle
		temp = start_temp
		for n in range(0, iters):
			old_value = self.puzzle.value()
			# make a random change
			x, y, old = self.puzzle.change_random_entry()
			new_value = self.puzzle.value()
			print('new_value= ' + str(new_value) + '; old_value= ' + str(old_value) + '; temp= ' + str(temp))
			acceptance_prob = math.exp((new_value - old_value)/temp)
			if temp < 0.00001:
				break
			# if new_value > old_value or random.uniform(0, 1) < acceptance_prob:
			if new_value <= old_value or random.uniform(0, 1) >= acceptance_prob:

				self.puzzle[x,y] = old
				# probably not this
				# self.puzzle = p
			temp = temp * decay_rate
		return (self.puzzle.clone_grid(), self.puzzle.value())
