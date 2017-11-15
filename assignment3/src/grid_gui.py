import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog

from grid_generator import *

square_size = 6

light_green = '#66ff66'
dark_green = '#006600'
black = '#000000'
light_brown = '#cc9900'
dark_brown = '#663300'


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.nav_grid = GridGenerator().gen_grid()
        #<create the rest of your GUI here>
        self.canvas = tk.Canvas(root, width=966 + 300, height=742)
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

        # Calculate button
        calc_button = tk.Button(self.canvas, height=5, width=20, text="Calculate", command=self.calculate)
        calc_button.place(x=1000 + 30, y=200 - 30)

        # Open file button
        open_button = tk.Button(self.canvas, height=5, width=20, text="Open file", command=self.open_file)
        open_button.place(x=1000 + 30, y=200 + 30)

        # Save file button
        save_button = tk.Button(self.canvas, height=5, width=20, text="Save file", command=self.save_file)
        save_button.place(x=1000 + 30, y=200 + 90)

        self.draw_map(self.canvas)


    #nav_grid = GridGenerator().gen_grid()

    def draw_map(self, canvas):
        offset = 6
        for i in range(self.nav_grid.height):
            for j in range(self.nav_grid.width):
                # Blocked, black
                if self.nav_grid.grid[i][j] == '0':
                    canvas.create_rectangle(offset + square_size * j, offset + square_size * i,
                                            offset + square_size * (j + 1),
                                            offset + square_size * (i + 1), fill=black)
                # Regular, light green
                elif self.nav_grid.grid[i][j] == '1':
                    canvas.create_rectangle(offset + square_size * j, offset + square_size * i,
                                            offset + square_size * (j + 1),
                                            offset + square_size * (i + 1), fill=light_green)
                # Hard to traverse, dark green
                elif self.nav_grid.grid[i][j] == '2':
                    canvas.create_rectangle(offset + square_size * j, offset + square_size * i,
                                            offset + square_size * (j + 1),
                                            offset + square_size * (i + 1), fill=dark_green)
                # Regular with highway, light brown
                elif self.nav_grid.grid[i][j] == 'a':
                    canvas.create_rectangle(offset + square_size * j, offset + square_size * i,
                                            offset + square_size * (j + 1),
                                            offset + square_size * (i + 1), fill=light_brown)
                # Hard to to traverse with highway
                elif self.nav_grid.grid[i][j] == 'b':
                    canvas.create_rectangle(offset + square_size * j, offset + square_size * i,
                                            offset + square_size * (j + 1),
                                            offset + square_size * (i + 1), fill=dark_brown)

    def calculate(self):
        """
        Dummy functionality until the algorithms are implemented
        :return:
        """
        result = 0
        if self.x_e.get() != '' and y_e.get() != '':
            result = int(self.x_e.get()) * int(y_e.get())
        self.canvas.itemconfigure(self.g_out, text=str(result))
        self.canvas.itemconfigure(self.h_out, text=str(result))
        self.canvas.itemconfigure(self.f_out, text=str(result))
        return result

    def open_file(self):
        print("opening a file....")
        name = tk.filedialog.askopenfile(title="Open file...")
        # name = tk.filedialog.askopenfile(filetypes=(("Text file", "*.txt"), ("All file types", "*.*")), title="Open file...")
        if not name:
            pass
        print(name.name)
        f = open(name.name, 'r')
        f.close()
        # Set this object's grid to the file
        # Display in tkinter
        '''
        try:
            f = open(name, "r")
            f.close()
        except IOError:
            pass
        except TypeError:
            pass
        '''

    def save_file(self):
        sfile = tk.filedialog.asksaveasfilename(title="Save file as...")
        if not sfile:
            pass
        print(sfile)
        f = open(sfile, 'w')
        f.write(str(nav_grid))
        f.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    app.pack(side="top", fill="both", expand=True)
    app.master.title("Grid GUI: Assignment #3")
    root.mainloop()


