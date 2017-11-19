import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog

from grid_generator import *
from graph_search import *

square_size = 6

black = '#000000'
# Blue for rivers
blue_light = '#38c9ff'
blue_dark = '#1b74e8'
brown_light = '#cc9900'
brown_dark = '#663300'
# Green for plains
green_light = '#66ff66'
green_dark = '#006600'
# Pink for traversal over plains(?)
pink_neon = '#e81be4'
pink_neon_light = '#ff68fc'
# Purple for traversal over rivers(?)
purple = '#7f1ff4'
purple_light=''
# Red for goal
red = '#ff0000'
# White for start
white='#ffffff'


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.nav_grid = GridGenerator().gen_grid()
        #<create the rest of your GUI here>
        self.canvas = tk.Canvas(self.parent, width=966 + 300, height=742)
        customFont = tkFont.Font(family="Monaco", size=20)

        self.canvas.pack()

        self.canvas.create_text(1000 + 50 + 40, 80, text="h:\ng:\nf:", font=customFont)
        self.h_out = self.canvas.create_text(1000 + 80 + 40, 52, text="", font=customFont)
        self.g_out = self.canvas.create_text(1000 + 80 + 40, 81, text="", font=customFont)
        self.f_out = self.canvas.create_text(1000 + 80 + 40, 107, text="", font=customFont)

        # Taking in x and y coordinates for the grid
        self.canvas.create_text(1000, 150, text="x:", font=customFont)
        self.x_e = tk.Entry(self.canvas, width=8)
        self.x_e.place(x=1000 + 20, y=150 - 10)
        self.canvas.create_text(1000 + 145, 150, text="y:", font=customFont)
        self.y_e = tk.Entry(self.canvas, width=8)
        self.y_e.place(x=1000 + 165, y=150 - 10)

        # Uniform cost search button
        ufc_button = tk.Button(self.canvas, text="Uniform-Cost Search", command=self.calculate)

        # A-star button


        # Calculate button
        #calc_button = tk.Button(self.canvas, height=5, width=20, text="Calculate", command=self.calculate)
        calc_button = tk.Button(self.canvas, text="Calculate", command=self.calculate)

        calc_button.place(x=1000 + 30 + 40 + 10, y=200)

        # Open file button
        #open_button = tk.Button(self.canvas, height=5, width=20, text="Open file", command=self.open_file)
        open_button = tk.Button(self.canvas, text="Open file", command=self.open_file)
        open_button.place(x=1000 + 30 + 50, y=200 + 60)

        # Save file button
        save_button = tk.Button(self.canvas, text="Save file", command=self.save_file)
        save_button.place(x=1000 + 30 + 50, y=200 + 90 + 30)

        self.refresh()

    def refresh(self):
        self.draw_map(self.canvas)
        self.illustrate_path()

    def draw_map(self, canvas):
        offset = 6
        for i in range(self.nav_grid.height):
            for j in range(self.nav_grid.width):
                # Blocked, black
                if self.nav_grid[j, i] == '0':
                    canvas.create_rectangle(offset + square_size * j,
                                            offset + square_size * i,
                                            offset + square_size * (j + 1),
                                            offset + square_size * (i + 1), fill=black)
                # Regular, light green
                elif self.nav_grid[j, i] == '1':
                    canvas.create_rectangle(offset + square_size * j,
                                            offset + square_size * i,
                                            offset + square_size * (j + 1),
                                            offset + square_size * (i + 1), fill=green_light)
                # Hard to traverse, dark green
                elif self.nav_grid[j, i] == '2':
                    canvas.create_rectangle(offset + square_size * j,
                                            offset + square_size * i,
                                            offset + square_size * (j + 1),
                                            offset + square_size * (i + 1), fill=green_dark)
                # Regular with highway, light brown
                elif self.nav_grid[j, i] == 'a':
                    canvas.create_rectangle(offset + square_size * j,
                                            offset + square_size * i,
                                            offset + square_size * (j + 1),
                                            offset + square_size * (i + 1), fill=blue_light)
                # Hard to to traverse with highway
                elif self.nav_grid[j, i] == 'b':
                    canvas.create_rectangle(offset + square_size * j,
                                            offset + square_size * i,
                                            offset + square_size * (j + 1),
                                            offset + square_size * (i + 1), fill=blue_dark)
        # Draw the start-point
        canvas.create_rectangle(offset + square_size * self.nav_grid.start[0],
                                offset + square_size * self.nav_grid.start[1],
                                offset + square_size * (self.nav_grid.start[0] + 1),
                                offset + square_size * (self.nav_grid.start[1] + 1), fill=white)
        # Draw the goal
        canvas.create_rectangle(offset + square_size * self.nav_grid.goal[0],
                                offset + square_size * self.nav_grid.goal[1],
                                offset + square_size * (self.nav_grid.goal[0] + 1),
                                offset + square_size * (self.nav_grid.goal[1] + 1), fill=red)


    def illustrate_path(self):
        """
        :param start: the startpoint
        :param end: the endpoint
        :return:
        """
        offset = 6
        l = []
        #l = GraphSearch.get_goal_path()
        for i in range(120):
            l.append((i, i))
        for (x,y) in l:
            if self.nav_grid.grid[y][x] == '0':
                self.canvas.create_rectangle(offset + square_size * y,
                                             offset + square_size * x,
                                             offset + square_size * (y + 1),
                                             offset + square_size * (x + 1),
                                             fill=purple)
            elif self.nav_grid.grid[y][x] == '1':
                self.canvas.create_rectangle(offset + square_size * y,
                                             offset + square_size * x,
                                             offset + square_size * (y + 1),
                                             offset + square_size * (x + 1),
                                             fill=purple)
            elif self.nav_grid.grid[y][x] == '2':
                self.canvas.create_rectangle(offset + square_size * y,
                                             offset + square_size * x,
                                             offset + square_size * (y + 1),
                                             offset + square_size * (x + 1),
                                             fill=purple)
            elif self.nav_grid.grid[y][x] == 'a':
                self.canvas.create_rectangle(offset + square_size * y,
                                             offset + square_size * x,
                                             offset + square_size * (y + 1),
                                             offset + square_size * (x + 1),
                                             fill=purple)
            elif self.nav_grid.grid[y][x] == 'b':
                self.canvas.create_rectangle(offset + square_size * y,
                                             offset + square_size * x,
                                             offset + square_size * (y + 1),
                                             offset + square_size * (x + 1),
                                             fill=purple)

    def calculate(self):
        """
        Dummy functionality until the algorithms are implemented
        :return:
        """
        result = 0
        # Need to make sure integers are:
        # (1) parsed as integers
        # (2) within bounds
        print(self.nav_grid.start, self.nav_grid.goal)
        if self.x_e.get() != '' and self.y_e.get() != '':
            result = int(self.x_e.get()) * int(self.y_e.get())
        # This is where we output the g, h and f values out
        self.canvas.itemconfigure(self.g_out, text=str(result))
        self.canvas.itemconfigure(self.h_out, text=str(result))
        self.canvas.itemconfigure(self.f_out, text=str(result))
        # Might include a time output at some other time
        return result

    def open_file(self):
        print("opening a file....")
        name = tk.filedialog.askopenfile(title="Open file...")
        # name = tk.filedialog.askopenfile(filetypes=(("Text file", "*.txt"), ("All file types", "*.*")), title="Open file...")
        if not name:
            pass
        print(name.name)
        self.nav_grid = NavigationGrid.from_file(name.name)
        self.refresh()

    def save_file(self):
        sfile = tk.filedialog.asksaveasfilename(title="Save file as...")
        if not sfile:
            pass
        print(sfile)
        with open(sfile, 'w') as f:
            f.write(self.nav_grid.serialize())


def run_gui():
    root = tk.Tk()
    app = MainApplication(root)
    app.pack(side="top", fill="both", expand=True)
    app.master.title("Grid GUI: Assignment #3")
    root.mainloop()


if __name__ == "__main__":
    run_gui()
