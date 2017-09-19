"""Grid puzzle for CS440 assignment 1. 

Usage:
  puzzle_runner.py display <file>
  puzzle_runner.py generate [-o <file>] hill-climbing <size> <iters>
  puzzle_runner.py generate [-o <file>] random-restarts <size> <iters> <restarts>
  puzzle_runner.py generate [-o <file>] random-walk <size> <iters> <p>
  puzzle_runner.py generate [-o <file>] annealing <size> <iters> <start_t> <decay_rate> 
  puzzle_runner.py generate [-o <file>] genetic <size> <iters> <population>
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

class PuzzleRunner:
	def __init__(self, input_file=None):
		self.puzzle = PuzzleGrid(input_file=input_file)

		self.gui = GridGui(self.puzzle)

		self.gui.register_new(self.do_new_puzzle)


	def do_new_puzzle(self, size):
		# make a PuzzleGenerator, take resulting puzzle and assign it to
		# self.puzzle
		pass

	
def main():
	arguments = docopt(__doc__, version="Assignment 1")
	print(arguments)

if __name__ == '__main__':
	main()
