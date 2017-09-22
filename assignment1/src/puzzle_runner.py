"""Grid puzzle for CS440 assignment 1. 

Usage:
  puzzle_runner.py display <file>
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

from gui import GridGui
from puzzle import PuzzleGrid

from generators import *

class PuzzleRunner:
	def __init__(self, input_file=None):
		self.puzzle = PuzzleGrid.from_file(input_file)

		self.gui = GridGui(self.puzzle)

	def do_new_puzzle(self, size):
		# make a PuzzleGenerator, take resulting puzzle and assign it to
		# self.puzzle
		pass

	
def main():
	arguments = docopt(__doc__, version="Assignment 1")
	if arguments["display"]:
		puzzle = PuzzleRunner(arguments["<file>"])
		print(puzzle.puzzle)
	elif arguments["generate"]:
		size = int(arguments["<size>"])
		iters = int(arguments["<iters>"])

		if arguments["hill-climbing"]:
			gen = HillClimbingGenerator(size, iters)
		elif arguments["random-restarts"]:
			restarts = int(arguments["<restarts>"])

			gen = RandomRestartsGenerator(size, iters, restarts)
		elif arguments["random-walk"]:
			p = float(arguments["<p>"])

			gen = RandomWalkGenerator(size, iters, p)
		elif arguments["annealing"]:
			start_temp = float(arguments["<start_temp>"])
			decay_rate = float(arguments["<decay_rate>"])

			gen = SimulatedAnnealingGenerator(size, iters, start_temp, decay_rate)
		elif arguments["genetic"]:
			population_size = int(arguments["<pop_size>"])

			gen = GeneticGenerator(size, iters, population_size)

if __name__ == '__main__':
	main()
