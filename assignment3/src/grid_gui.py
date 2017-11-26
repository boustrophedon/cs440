import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import *
from decimal import *

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


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.nav_grid = GridGenerator().gen_grid()
        #<create the rest of your GUI here>
        self.canvas = tk.Canvas(self.parent, width=966 + 300, height=742)
        customFont = tkFont.Font(family="Monaco", size=20)

        self.canvas.pack()

        self.canvas.create_text(1000 + 50 + 40, 80 + 200, text="h:\ng:\nf:", font=customFont)
        self.h_out = self.canvas.create_text(1000 + 80 + 40 + 20 + 20, 52 + 200, text="", font=customFont)
        self.g_out = self.canvas.create_text(1000 + 80 + 40 + 20 + 20, 81 + 200, text="", font=customFont)
        self.f_out = self.canvas.create_text(1000 + 80 + 40 + 20 + 20, 107 + 200, text="", font=customFont)

        # Taking in x and y coordinates for the grid
        self.canvas.create_text(1000, 150 + 200, text="x:", font=customFont)
        self.x_e = tk.Entry(self.canvas, width=8)
        self.x_e.place(x=1000 + 20, y=150 - 10 + 200)
        self.canvas.create_text(1000 + 145, 150 + 200, text="y:", font=customFont)
        self.y_e = tk.Entry(self.canvas, width=8)
        self.y_e.place(x=1000 + 165, y=150 - 10 + 200)

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
                                      command=lambda: self.illustrate_path(3, int(self.weight_e.get())))#, weight=5))
        wtd_a_star_button.place(x=1000 + 20 + 10, y=80)
        self.canvas.create_text(1000 - 20 + 40 + 40, 120+10, text="w:", font=customFont)


        # Calculate button
        #calc_button = tk.Button(self.canvas, height=5, width=20, text="Calculate", command=self.calculate)
        calc_button = tk.Button(self.canvas, text="Calculate", command=self.calculate)

        calc_button.place(x=1080, y=200 + 200)

        # Open file button
        #open_button = tk.Button(self.canvas, height=5, width=20, text="Open file", command=self.open_file)
        open_button = tk.Button(self.canvas, text="Open file", command=self.open_file)
        open_button.place(x=1080, y=200 + 60 + 200)

        # Save file button
        save_button = tk.Button(self.canvas, text="Save file", command=self.save_file)
        save_button.place(x=1080, y=200 + 90 + 30 + 200)

        self.heuristic_spinbox = Spinbox(self.canvas, values=('Euclidean squared', 'Euclidean'))
        self.heuristic_spinbox.place(x=1080-40, y=170)

        self.search = None

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
        search = None
        if vargs[0] is 1:
            print("Uniform Cost Search")
            search = GraphSearch(self.nav_grid)
        elif vargs[0] is 2:
            print("A* Search")
            print(self.heuristic_spinbox.get())
            # TODO: More heuristics, NOT COMPLETE
            # Adding spinbox functionality
            if self.heuristic_spinbox.get() == 'Euclidean':
                self.search = GraphSearch(self.nav_grid, heuristic=euclidean_distance)
            else:
                self.search = GraphSearch(self.nav_grid, heuristic=euclidean_distance)

        elif vargs[0] is 3:
            print("Weighted A* Search, w:= " + str(vargs[1]))
            print(self.heuristic_spinbox.get())
            # TODO: More heuristics, NOT COMPLETE
            # Adding spinbox functionality
            if self.heuristic_spinbox.get() == 'Euclidean':
                self.search = GraphSearch(self.nav_grid, heuristic=euclidean_distance, weight=vargs[1])
            else:
                self.search = GraphSearch(self.nav_grid, heuristic=euclidean_distance, weight=vargs[1])
            '''
            if self.weight_e.get() is '' and self.heuristic_spinbox.get() is 'Euclidean':
                print("here")
                search = GraphSearch(self.nav_grid, heuristic=euclidean_distance, weight=1)
            elif self.heuristic_spinbox.get() == 'Euclidean':
                print("here2")
                search = GraphSearch(self.nav_grid, heuristic=euclidean_distance, weight=vargs[1])
            '''
            #search.weight = int(vargs[0])
        if self.search is None:
            return
        l = self.search.search()
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
        x, y = self.x_e.get(), self.y_e.get()
        x, y = int(x), int(y)
        g_value = self.search.cost_from_start.get((x,y))
        # print((int(self.x_e.get()), int(self.y_e.get())) in self.search.cost_from_start)
        self.canvas.itemconfigure(self.g_out, text=str("%.2f" % g_value))
        self.canvas.itemconfigure(self.h_out, text=str(result))
        self.canvas.itemconfigure(self.f_out, text=str(result))
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
