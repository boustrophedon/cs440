import random
import math

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

        for center in centers:
            offsets = itertools.product(range(-15, 16), range(-15, 16))
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
        while highways.is_highway(start) or \
            (start in ((0,0), (0, self.height), (self.width, 0), (self.width, self.height))):
            start = self.random_boundary_cell()

        # direction to begin moving the highway
        v = [0,0]
        if start[0] in (0, self.width):
            v[0] = (1 if start[0] == 0 else -1)
            v[1] = 0
        else:
            v[0] = 0
            v[1] = (1 if start[1] == 0 else -1)

        path = set()
        path.add(start)
        curr = start
        hit_border = False
        while not hit_border:
            for i in range(0, 20):
                curr = tadd(curr, v)
                if not highways.is_inside(curr):
                    hit_border = True
                    break
                elif highways.is_highway(curr) or curr in path:
                    return False
                else:
                    path.add(curr)

            # move "left"
            if with_p(0.2):
                # switch from moving in x dir to y dir or vice versa
                v[0], v[1] = v[1], v[0]
                # 1*1 = 1, -1*-1 = 1 so either way we end up with 1
                v[0] *= v[0]
                v[1] *= v[1]
            # move "right"
            elif with_p(0.2):
                # switch from moving in x dir to y dir or vice versa
                v[0], v[1] = v[1], v[0]
                # -1*1*1 = -1, -1*-1*-1 = -1 so either way we end up with -1
                v[0] *= -1*v[0]
                v[1] *= -1*v[1]
            # with probability 0.6 don't do anything
            else:
                pass

        if len(path) < 100:
            return False
        else:
            for p in path:
                highways[p] = HIGHWAY
            return True

    def select_blocked(self, grid):
        blocked_max = (self.width*self.height)//5
        count = 0
        while count < blocked_max:
            p = self.random_cell()
            if not grid.is_highway(p):
                count+=1
                grid[p] = BLOCKED

    def select_start(self, grid):
        is_blocked = True
        start = (0,0)
        while is_blocked:
            border = self.random_boundary_cell()
            xoffset = random.choice(range(-20, 21))
            yoffset = random.choice(range(-20, 21))

            x = (border[0] + xoffset) % self.width
            y = (border[1] + yoffset) % self.height

            start = (x,y)
            is_blocked = grid.is_blocked(start)
        grid.start = start
    
    def select_goal(self, grid):
        is_blocked = True
        is_too_close = True
        goal = (0,0)
        while is_blocked or is_too_close:
            border = self.random_boundary_cell()
            xoffset = random.choice(range(-20, 21))
            yoffset = random.choice(range(-20, 21))

            x = (border[0] + xoffset) % self.width
            y = (border[1] + yoffset) % self.height

            goal = (x,y)
            is_blocked = grid.is_blocked(goal)
            is_too_close = math.sqrt( (grid.start[0] - goal[0])**2 + (grid.start[1] - goal[1])**2) < 100
        grid.goal = goal
