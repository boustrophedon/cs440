from grid_generator import *


for i in range(0, 5):
    gen = GridGenerator(width=160, height=120)
    g = gen.gen_grid()
    for j in range(0,10):
        fname = 'map{:02d}'.format(10*i+j)
        with open('data/'+fname, 'w') as f:
            f.write(g.serialize())
            f.close()
        gen.select_start(g)
        gen.select_goal(g)
