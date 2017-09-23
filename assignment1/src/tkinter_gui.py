from tkinter import *
#from tkinter.filedialog import askopenfilename
from puzzle import PuzzleGrid


WEIRD_ORANGE= "#fb0"
RED = "#f00"
DARK_RED="#8b0000"
WHITE="#fff"


class TkinterGUI(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Assignment 1")
        self.pack(fill = BOTH, expand = 1)
        self.canvas = Canvas(self)
        #canvas.create_rectangle(30, 10, 120, 80, outline="#fb0", fill="#fb0")
        #self.draw_square(30, 30)
        self.canvas.pack(fill=BOTH, expand=1)

    def draw_square(self, x, y, n):
        self.canvas.create_rectangle(x - 25, y - 25, x + 25, y + 25, outline=DARK_RED, fill=DARK_RED)
        self.canvas.create_text(x, y, text=str(5), fill=WHITE)
        self.canvas.after(5, self.draw_square)

    def draw_puzzle(self, puzzle):
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
                self.draw_square(startx, starty, puzzle.get(i, j))
                startx += 55
            startx = oldstartx
            starty += 55





if __name__ == "__main__":
    root = Tk()
    ex = TkinterGUI()
    root.geometry("600x700")
    # root.mainloop()
    p = PuzzleGrid(7)
    ex.draw_square(30, 30, 5)
    root.mainloop()

    # root.update()
    # ex.update()