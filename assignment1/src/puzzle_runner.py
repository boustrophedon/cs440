"""Grid puzzle for CS440 assignment 1. 

Usage:
  puzzle_runner.py display [--gui] [<file>]
  puzzle_runner.py generate [-o <file>] hill-climbing <size> <iters>
  puzzle_runner.py generate [-o <file>] random-restarts <size> <iters> <restarts>
  puzzle_runner.py generate [-o <file>] random-walk <size> <iters> <p>
  puzzle_runner.py generate [-o <file>] annealing <size> <iters> <start_temp> <decay_rate> 
  puzzle_runner.py generate [-o <file>] genetic <size> <iters> <pop_size>
  puzzle_runner.py --help
  puzzle_runner.py --version

Options:
  -h,--help     Show this screen.
  -o <file>,--output <file>    Output file for best generated puzzle
  -v,--version  Display version
"""
from docopt import docopt

from tkinter_gui import do_gui
from puzzle import PuzzleGrid

from generators import *

class PuzzleRunner:
	def __init__(self, input_file=None, gui=False):
		if input_file is not None:
			self.puzzle = PuzzleGrid.from_file(input_file)
		else:
			self.puzzle = PuzzleGrid.random_puzzle(11)

		if gui:
			self.gui = do_gui(self.puzzle)
		else:
			print(self.puzzle)
	
def main():
	arguments = docopt(__doc__, version="Assignment 1")
	if arguments["display"]:
		PuzzleRunner(arguments["<file>"], arguments["--gui"])

	elif arguments["generate"]:
		size = int(arguments["<size>"])
		iters = int(arguments["<iters>"])
		if not iters > 0:
			raise ValueError("Number of iterations should be > 0. Input: {}".format(iters))
		if not size > 0:
			raise ValueError("Size should be > 0. Input: {}".format(size))

		output = None
		if arguments["hill-climbing"]:
			gen = HillClimbingGenerator(size)

			output = gen.generate(iters)
		elif arguments["random-restarts"]:
			restarts = int(arguments["<restarts>"])
			if not restarts > 0:
				raise ValueError("Number of restarts should be > 0. Input: {}".format(restarts))

			gen = RandomRestartsGenerator(size)
			output = gen.generate(iters, restarts)
		elif arguments["random-walk"]:
			p = float(arguments["<p>"])
			if p > 1 or p < 0:
				raise ValueError("The parameter p should be a probability between 0 and 1. Input: {}".format(p))

			gen = RandomWalkGenerator(size)

			output = gen.generate(iters, p)
		elif arguments["annealing"]:
			start_temp = float(arguments["<start_temp>"])
			decay_rate = float(arguments["<decay_rate>"])

			gen = SimulatedAnnealingGenerator(size)
			output = gen.generate(iters, start_temp, decay_rate)
		elif arguments["genetic"]:
			population_size = int(arguments["<pop_size>"])
			if not population_size > 0:
				raise ValueError("Population size should be > 0. Input: {}".format(population_size))

			gen = GeneticGenerator(size)
			output = gen.generate(iters, population_size)

		if arguments["--output"]:
			with open(arguments["--output"], "w") as f:
				f.write(str(output[0].size()) + "\n" + str(output[0]))
		else:
			# print(str(output[0]) + "\n" + str(output[1]))
			do_gui(PuzzleGrid(output[0]))

if __name__ == '__main__':
	main()
