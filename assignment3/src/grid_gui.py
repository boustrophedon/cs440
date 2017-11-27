import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import *
import time

from grid_generator import *
from graph_search import *
from sequential_search import *


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
purple = '#5600ba'
# 5000ad    #7700ff
purple_light='#a544ff'
# Red for goal
red = '#ff0000'
# White for start
white='#ffffff'
# Yell for traversal over plains(?)
yellow = '#ffe247'
yellow_see_doctor = '#967f00'

adjustment_seq = 75


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.nav_grid = GridGenerator().gen_grid()
        #<create the rest of your GUI here>
        self.canvas = tk.Canvas(self.parent, width=966 + 300, height=742)
        customFont = tkFont.Font(family="Monaco", size=20)
        timeFont = tkFont.Font(family="Monaco", size=10)

        self.canvas.pack()

        # Taking in x and y coordinates for the grid
        self.canvas.create_text(1000, 150 + 200 + adjustment_seq, text="x:", font=customFont)
        self.x_e = tk.Entry(self.canvas, width=8)
        self.x_e.place(x=1000 + 20, y=150 - 10 + 200 + adjustment_seq)
        self.canvas.create_text(1000 + 145, 150 + 200 + adjustment_seq, text="y:", font=customFont)
        self.y_e = tk.Entry(self.canvas, width=8)
        self.y_e.place(x=1000 + 165, y=150 - 10 + 200 + adjustment_seq)

        # Uniform cost search button
        ufc_button = tk.Button(self.canvas, text="Uniform-Cost Search", command=lambda: self.illustrate_path(1))
        ufc_button.place(x=1000 + 40 - 10, y=20)

        # A-star button
        a_star_button = tk.Button(self.canvas, text="A* Search", command=lambda: self.illustrate_path(2))
        a_star_button.place(x=1000 + 40+20, y=50)

        # Weighted A-star button
        tvar = StringVar()
        tvar.set("1")
        self.weight_e = tk.Entry(self.canvas, width=8, textvariable=tvar)
        self.weight_e.place(x=1000 + 40 + 40, y=120)
        wtd_a_star_button = tk.Button(self.canvas, text="Weighted A* Search",
                                      command=lambda: self.illustrate_path(3, float(self.weight_e.get())))#, weight=5))
        wtd_a_star_button.place(x=1000 + 20 + 10, y=80)
        self.canvas.create_text(1000 - 20 + 40 + 40, 120+10, text="w:", font=customFont)

        # Heuristic spinbox
        self.heuristic_spinbox = Spinbox(self.canvas, values=('Manhattan',
                                                              'Distance squared',
                                                              'Euclidean',
                                                              'Euclidean (admissible)',
                                                              'Chebyshev',
                                                              'Chebyshev (admissible)'))
        self.heuristic_spinbox.place(x=1080 - 40, y=170)

        # Displaying the f, g and h values
        self.canvas.create_text(1000 + 50 + 40, 80 + 200 + adjustment_seq, text="h:\ng:\nf:", font=customFont)
        self.h_out = self.canvas.create_text(1000 + 80 + 40 + 20 + 20, 52 + 200 + adjustment_seq, text="",
                                             font=customFont)
        self.g_out = self.canvas.create_text(1000 + 80 + 40 + 20 + 20, 81 + 200 + adjustment_seq, text="",
                                             font=customFont)
        self.f_out = self.canvas.create_text(1000 + 80 + 40 + 20 + 20, 107 + 200 + adjustment_seq, text="",
                                             font=customFont)

        # Calculate button
        #calc_button = tk.Button(self.canvas, height=5, width=20, text="Calculate", command=self.calculate)
        calc_button = tk.Button(self.canvas, text="Calculate", command=self.calculate)
        calc_button.place(x=1080, y=200 + 200 + adjustment_seq)



        # Open file button
        #open_button = tk.Button(self.canvas, height=5, width=20, text="Open file", command=self.open_file)
        open_button = tk.Button(self.canvas, text="Open file", command=self.open_file)
        open_button.place(x=1080, y=200 + 60 + 200 + adjustment_seq)

        # Save file button
        save_button = tk.Button(self.canvas, text="Save file", command=self.save_file)
        save_button.place(x=1080, y=200 + 90 + 30 + 200 + adjustment_seq)

        # Holding onto the current search being displayed
        self.search = None

        # Showing how long each search took
        self.canvas.create_text(1050 + 20, 400 + 200 + 50 + 50, text="Time elapsed:", font=timeFont)
        self.time = self.canvas.create_text(1070 + 30 + 20 + 50, 400 + 250 + 50, text="", font=timeFont)

        self.refresh()

    def refresh(self):
        self.draw_map(self.canvas)
        #self.illustrate_path()

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

    def illustrate_path(self, *vargs):
        """
        Need to redo this implementation
        :param type: 1 if ucs, 2 if astar, 3 if weighted astar, 4 if sequential astar
        :return:
        """
        offset = 6
        l = []
        self.search = None
        if vargs[0] is 1:
            print("Uniform Cost Search")
            self.search = GraphSearch(self.nav_grid)
        elif vargs[0] is 2:
            print("A* Search")
            print(self.heuristic_spinbox.get())
            # TODO: More heuristics, NOT COMPLETE
            # Adding spinbox functionality
            if self.heuristic_spinbox.get() == 'Manhattan':
                self.search = GraphSearch(self.nav_grid, heuristic=manhattan)
            elif self.heuristic_spinbox.get() == 'Euclidean':
                self.search = GraphSearch(self.nav_grid, heuristic=euclidean)
            elif self.heuristic_spinbox.get() == 'Euclidean (admissible)':
                self.search = GraphSearch(self.nav_grid, heuristic=euclidean_admissible)
            elif self.heuristic_spinbox.get() == 'Distance squared':
                self.search = GraphSearch(self.nav_grid, heuristic=dist_squared)
            elif self.heuristic_spinbox.get() == 'Chebyshev':
                self.search = GraphSearch(self.nav_grid, heuristic=chebyshev)
            elif self.heuristic_spinbox.get() == 'Chebyshev (admissible)':
                self.search = GraphSearch(self.nav_grid, heuristic=chebyshev_admissible)
            else:
                self.search = GraphSearch(self.nav_grid, heuristic=empty_heuristic)

        elif vargs[0] is 3:
            print("Weighted A* Search, w:= " + str(vargs[1]))
            print(self.heuristic_spinbox.get())
            # TODO: More heuristics, NOT COMPLETE
            # Hans: Seems complete
            # Adding spinbox functionality
            if self.heuristic_spinbox.get() == 'Manhattan':
                self.search = GraphSearch(self.nav_grid, heuristic=manhattan, weight=vargs[1])
            elif self.heuristic_spinbox.get() == 'Euclidean':
                self.search = GraphSearch(self.nav_grid, heuristic=euclidean, weight=vargs[1])
            elif self.heuristic_spinbox.get() == 'Euclidean (admissible)':
                self.search = GraphSearch(self.nav_grid, heuristic=euclidean_admissible, weight=vargs[1])
            elif self.heuristic_spinbox.get() == 'Distance squared':
                self.search = GraphSearch(self.nav_grid, heuristic=dist_squared, weight=vargs[1])
            elif self.heuristic_spinbox.get() == 'Chebyshev':
                self.search = GraphSearch(self.nav_grid, heuristic=chebyshev, weight=vargs[1])
            elif self.heuristic_spinbox.get() == 'Chebyshev (admissible)':
                self.search = GraphSearch(self.nav_grid, heuristic=chebyshev_admissible, weight=vargs[1])
            else:
                self.search = GraphSearch(self.nav_grid, heuristic=empty_heuristic)
        if self.search is None:
            return
        time_elapsed = time.time()
        l = self.search.search()
        time_elapsed = time.time() - time_elapsed
        self.canvas.itemconfigure(self.time, text=str("%.8f s" % time_elapsed))
        print(time_elapsed)
        print(l)
        self.draw_map(self.canvas)
        for (x, y) in l:
            if self.nav_grid[x, y] == '1':
                self.canvas.create_rectangle(offset + square_size * x,
                                             offset + square_size * y,
                                             offset + square_size * (x + 1),
                                             offset + square_size * (y + 1),
                                             fill=yellow)
            elif self.nav_grid[x, y] == '2':
                self.canvas.create_rectangle(offset + square_size * x,
                                             offset + square_size * y,
                                             offset + square_size * (x + 1),
                                             offset + square_size * (y + 1),
                                             fill=yellow_see_doctor)
            elif self.nav_grid[x, y] == 'a':
                self.canvas.create_rectangle(offset + square_size * x,
                                             offset + square_size * y,
                                             offset + square_size * (x + 1),
                                             offset + square_size * (y + 1),
                                             fill=purple_light)
            elif self.nav_grid[x, y] == 'b':
                self.canvas.create_rectangle(offset + square_size * x,
                                             offset + square_size * y,
                                             offset + square_size * (x + 1),
                                             offset + square_size * (y + 1),
                                             fill=purple)
        # Draw the start-point
        self.canvas.create_rectangle(offset + square_size * self.nav_grid.start[0],
                                offset + square_size * self.nav_grid.start[1],
                                offset + square_size * (self.nav_grid.start[0] + 1),
                                offset + square_size * (self.nav_grid.start[1] + 1), fill=white)
        # Draw the goal
        self.canvas.create_rectangle(offset + square_size * self.nav_grid.goal[0],
                                offset + square_size * self.nav_grid.goal[1],
                                offset + square_size * (self.nav_grid.goal[0] + 1),
                                offset + square_size * (self.nav_grid.goal[1] + 1), fill=red)

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
            # This is where we need to do math
            result = (int(self.x_e.get()) , int(self.y_e.get()))
        # This is where we output the g, h and f values out
            g_x, g_y = int(self.x_e.get()), int(self.y_e.get())

            g_value = self.search.cost_from_start[(g_x,g_y)]
            h_value = self.search.heuristic((g_x,g_y), self.nav_grid.goal)
            f_value = h_value + g_value
            self.canvas.itemconfigure(self.g_out, text=str("%.2f" % g_value))
            self.canvas.itemconfigure(self.h_out, text=str("%.2f" % h_value))
            self.canvas.itemconfigure(self.f_out, text=str("%.2f" % f_value))
        # Might include a time output at some other time
        return result

    def open_file(self):
        print("opening a file....")
        name = tk.filedialog.askopenfile(title="Open file...")
        # name = tk.filedialog.askopenfile(filetypes=(("Text file", "*.txt"), ("All file types", "*.*")), title="Open file...")
        if not name:
            return
        print(name.name)
        self.nav_grid = NavigationGrid.from_file(name.name)
        self.refresh()

    def save_file(self):
        sfile = tk.filedialog.asksaveasfilename(title="Save file as...")
        if not sfile:
            return
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
