from grid_generator import GridGenerator

if __name__ == '__main__':
    gen = GridGenerator(width=100, height=80)

    grid = gen.gen_grid()

    print(grid.serialize())
