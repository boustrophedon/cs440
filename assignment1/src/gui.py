import pygame, sys
from pygame.locals import *
from puzzle import PuzzleGrid
from grid import Grid
import numpy

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (192, 192, 192)


# Grid GUI
# Takes in a grid object that exposes a get(x,y) or possibly __index__()
# and displays it

class GridGui:
    def __init__(self, puzzle):
        # max size for 11 x 11 is 600
        self.windowSurface = pygame.display.set_mode((600, 700), 0, 32)
        # windowSurface.fill(BLACK)

        self.basicFont = pygame.font.SysFont(None, 48)
        draw_puzzle(puzzle, self.windowSurface, self.basicFont)
        pygame.display.update()


def draw_square(x, y, n, width, surface, font):
    pygame.draw.polygon(surface, RED, (
        (x - width / 2, y - width / 2),
        (x + width / 2, y - width / 2),
        (x + width / 2, y + width / 2),
        (x - width / 2, y + width / 2)
    ))
    number = font.render(str(n), True, WHITE, RED)
    if int(n) >= 10:
        surface.blit(number, (x - width / 3, y - width / 3))
    else:
        surface.blit(number, (x - width / 6, y - width / 3))


def draw_puzzle(puzzle, surface, font):
    oldstartx = startx = 25
    starty = 25
    size = puzzle.grid.size
    if size is 9:
        oldstartx = startx = 80
        starty = 80
    elif size is 7:
        oldstartx = startx = 135
        starty = 135
    elif size is 5:
        oldstartx = startx = 190
        starty = 190
    for i in range(0, puzzle.grid.size()):
        for j in range(0, puzzle.grid.size()):
            # draw_square(startx, starty, puzzle.puzzle[i][j], 50, surface, font)
            draw_square(startx, starty, puzzle.get(i, j), 50, surface, font)
            startx += 55
        startx = oldstartx
        starty += 55

'''
class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Grid File Select")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W + E + N + S)

        self.button = Button(self, text="Select...", command=self.load_file, width=50, height=20)
        self.button.grid(row=1, column=0, sticky=W)

    def load_file(self):
        fname = askopenfilename(filetypes=(("TXT files", "*.txt"),
                                           ("All files", "*.*")))
        if fname:
            try:
                #print("Successfully opened " + fname)
                return fname
            except:  # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        return None
'''


if __name__ == "__main__":
    Tk().withdraw()
    fname = askopenfilename()

    if fname:
        fp = open(fname, 'r')
    else:
        fp = None

    #Tk().destroy()




    pygame.init()
    a = numpy.ndarray((11, 11), dtype=int)
    p = PuzzleGrid(a)
    gui = GridGui(p)

    #draw_square(0, 650, 100, 5000, gui.windowSurface, gui.basicFont)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()