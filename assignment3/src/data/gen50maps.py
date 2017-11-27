from grid_generator import *


for i in range(1, 51):
    g = GridGenerator(width=160, height=120)
    g = g.gen_grid()
    f = None
    if i < 10:
        f = open('map0' + str(i), 'w')
    else:
        f = open('map' + str(i), 'w')
    if f is not None:
        f.write(g.serialize())
        f.close()

