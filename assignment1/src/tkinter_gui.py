from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
import datetime
import os
from puzzle import PuzzleGrid
from numpy import *
import numpy as np
from grid import Grid
import datetime
import os

WEIRD_ORANGE= "#fb0"
RED = "#f00"
DARK_RED="#8b0000"
WHITE="#fff"

numberFont = (None, 20)


class TkinterGUI(Frame):

    def __init__(self, puzzle, root):
        super().__init__()
        self.initUI(puzzle, root)

    def initUI(self, puzzle, root):
        self.root = root
        self.puzzle = puzzle

        # DIRTY HACK SO WE CAN SUBMIT
        v = self.puzzle.value()
        size = self.puzzle.size()
        self.puzzle.distances()[size-1, size-1] = v

        self.grid = self.puzzle.grid
        self.master.title("Assignment 1")
        self.pack(fill = BOTH, expand = 1)
        self.canvas = Canvas(self)
        #canvas.create_rectangle(30, 10, 120, 80, outline="#fb0", fill="#fb0")
        #self.draw_square(30, 30)
        self.canvas.pack(fill=BOTH, expand=1)
        self.solutionButton = Button(self, text="Show solution", command=self.draw_solution)
        self.solutionButton.place(x=25, y=620)
        self.originalButton = Button(self, text="Show original", command=self.draw_puzzle)
        self.originalButton.place(x=25, y=650)

        openSolutionFileButton = Button(self, text="Open solution file...", command=self.file_open)
        openSolutionFileButton.place(x=150, y=620)
        saveSolutionFileButton = Button(self, text="Save solution to file", command=self.file_save)
        saveSolutionFileButton.place(x=320, y=620)

        openProblemFileButton = Button(self, text="Open problem file...", command=self.file_open)
        openProblemFileButton.place(x=150, y=650)
        saveProblemFileButton = Button(self, text="Save problem to file", command=self.file_save)
        saveProblemFileButton.place(x=320, y=650)

    def draw_square(self, x, y, n):
        self.canvas.create_rectangle(x - 25, y - 25, x + 25, y + 25, outline=DARK_RED, fill=DARK_RED)
        if n == -1:
            self.canvas.create_text(x, y, text='X', fill=WHITE, font=numberFont)
        elif type(n) is not int:
            self.canvas.create_text(x, y, text=str(int(n)), fill=WHITE, font=numberFont)
        else:
            self.canvas.create_text(x, y, text=str(n), fill=WHITE, font=numberFont)
        #self.canvas.after(5, self.draw_square)

    def draw_puzzle(self):
        self.canvas.create_rectangle(0, 0, 600, 600, outline=WHITE, fill=WHITE)
        oldstartx = startx = 25
        starty = 25
        size = self.puzzle.grid.size()
        if size is 9:
            oldstartx = startx = 80
            starty = 80
        elif size is 7:
            oldstartx = startx = 135
            starty = 135
        elif size is 5:
            oldstartx = startx = 190
            starty = 190
        for i in range(0, size):
            for j in range(0, size):
                # draw_square(startx, starty, puzzle.puzzle[i][j], 50, surface, font)
                self.draw_square(x=startx, y=starty, n=self.puzzle.get(i, j))
                # self.draw_square(startx, starty, puzzle.grid.array.get(i, j))
                startx += 55
            startx = oldstartx
            starty += 55

    def draw_puzzle_t(self):
        self.canvas.create_rectangle(0, 0, 600, 600, outline=WHITE, fill=WHITE)
        oldstartx = startx = 25
        starty = 25
        size = self.puzzle.grid.size()
        if size is 9:
            oldstartx = startx = 80
            starty = 80
        elif size is 7:
            oldstartx = startx = 135
            starty = 135
        elif size is 5:
            oldstartx = startx = 190
            starty = 190
        for i in range(0, size):
            for j in range(0, size):
                # draw_square(startx, starty, puzzle.puzzle[i][j], 50, surface, font)
                self.draw_square(x=startx, y=starty, n=self.puzzle.get(j, i))
                # self.draw_square(startx, starty, puzzle.grid.array.get(i, j))
                startx += 55
            startx = oldstartx
            starty += 55

    def draw_solution(self):
        oldstartx = startx = 25
        starty = 25
        size = self.puzzle.size()
        if size is 9:
            oldstartx = startx = 80
            starty = 80
        elif size is 7:
            oldstartx = startx = 135
            starty = 135
        elif size is 5:
            oldstartx = startx = 190
            starty = 190
        for i in range(0, size):
            for j in range(0, size):
                # Command goes here
                self.draw_square(x=startx, y=starty, n=self.puzzle.distances().get(i, j))
                startx += 55
            startx = oldstartx
            starty += 55


    def file_save(self):
        self.root.update()
        date = '' + str(datetime.datetime.now().year) + '_' + str(datetime.datetime.now().month) + '_' + str(datetime.datetime.now().day)
        print(date)
        filename = tk.filedialog.asksaveasfilename(defaultextension=".txt", title="Save file as...", initialdir=os.getcwd())
        if filename is '' or None:
            return
        f = open(filename, "w")
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        # Write to file here

        f.close()


    def file_open(self):
        self.root.update()
        filename = tk.filedialog.askopenfilename(defaultextension=".txt", title="Open grid/puzzle file", initialdir=os.getcwd())
        if filename is '' or None:
            return
        #f = open(filename, "r")
        # Load from file here
        self.puzzle = PuzzleGrid((Grid(PuzzleGrid.from_file(filename).grid.array)))
        self.draw_puzzle_t()
        print(self.puzzle)
        self.root.update()
        #f.close()  # `()` was missing.


def do_gui(puzzle):
    root = Tk()
    root.geometry("600x700")
    text = Text(root)

    ex = TkinterGUI(puzzle, root)

    #ex.draw_square(30, 30, 5)
    ex.draw_puzzle()
    root.mainloop()

    # root.update()
    # ex.update()


