import random

import itertools

from navigation_grid import *

def with_p(p):
    return random.random() < p

class GridGenerator:
    def __init__(self, width=160, height=120):
        self.width = width
        self.height = height

    def gen_grid(self):
        grid = NavigationGrid(self.width, self.height)

        self.select_htt(grid)
        self.select_highways(grid)
        self.select_blocked(grid)
        self.select_start(grid)
        self.select_goal(grid)

        return grid

    def random_cell(self):
        x = random.choice(range(0, self.width))
        y = random.choice(range(0, self.height))

        return (x,y)

    def random_boundary_cell(self):
        cell = list(self.random_cell())
        # choose random cell, clip one to boundary
        x1 = random.choice([0, self.width-1])
        y1 = random.choice([0, self.height-1])
        clipped = (x1, y1)

        coord_to_clip = random.choice((0,1))
        cell[coord_to_clip] = clipped[coord_to_clip]

        return tuple(cell)

    def select_htt(self, grid):
        centers = set()
        while len(centers) < 8:
            new_cell = self.random_cell()
            if new_cell not in centers:
                centers.add(new_cell)

        offsets = itertools.product(range(-30, 31), range(-30, 31))
        for center in centers:
            points = [tadd(center, offset) for offset in offsets]
            points = filter(grid.is_inside, points)
            for p in points:
                if with_p(0.5):
                    grid[p] = HTT

        grid.htt_centers = centers

    def select_highways(self, grid):
        success = False
        # retry with a new set of highways until success
        while not success:
            highways = NavigationGrid(self.width, self.height)

            success = self.try_highways(highways)

        # merge highways into grid
        for orig, hw in zip(grid.iter_mut(), highways.iter()):
            if hw == HIGHWAY:
                if orig == HTT:
                    orig[...] = HTT_HIGHWAY
                else:
                    orig[...] = HIGHWAY

    def try_highways(self, highways):
        trymax = 10

        # for each highway, try up to 10 times
        # if any of them fail after 10 attempts, fail out of the whole thing
        # and try to generate a new set of highways
        for _ in range(0, 4):
            trycount = 0
            success = False
            while not success:
                success = self.try_highway(highways)
                
                if not success: 
                    trycount += 1
                if trycount == trymax:
                    return False
        return True

    def try_highway(self, highways):
        start = self.random_boundary_cell()
        # this will never fail with probability 1, so we can keep going until
        # we find a valid start
        while highways.is_highway(start):
            start = self.random_boundary_cell()

        # v is the direction vector telling us which way to go
        v = [0,0]
        v[random.choice((0,1))] = 1

        # move in direction away from border, which is same as move towards center.
        # if the distance from current position to center is positive, move in positive direction
        # do same thing to both coords because it doesn't affect the coord that is 0.
        v[0] *= (1 if (self.width//2 - start[0]) > 0 else -1)
        v[1] *= (1 if (self.height//2 - start[1]) > 0 else -1)

        path = list()
        path.append(start)
        curr = start
        hit_border = False
        while not hit_border:
            for i in range(0, 20):
                curr = tadd(curr, v)
                if not highways.is_inside(curr):
                    hit_border = True
                elif highways.is_highway(curr):
                    return False
                else:
                    path.append(curr)

            if with_p(0.2):
                # switch from moving in x dir to y dir or vice versa
                v[0], v[1] = v[1], v[0]
                perp_dir = random.choice((-1, 1))
                v[0] *= perp_dir
                v[1] *= perp_dir

        if len(path) < 100:
            return False
        else:
            for p in path:
                highways[p] = HIGHWAY
            return True

    def select_blocked(self, grid):
        grid[1,1] = BLOCKED

    def select_start(self, grid):
        grid.start = (0,0)
    
    def select_goal(self, grid):
        grid.goal = (100,100)
