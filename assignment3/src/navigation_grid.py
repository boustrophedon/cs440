from math import sqrt,inf
import random
import itertools

import numpy

BLOCKED='0'
UNBLOCKED='1'
HTT='2'
HIGHWAY='a'
HTT_HIGHWAY='b'

def both_unblocked(g1, g2):
    return (g1 in (UNBLOCKED, HIGHWAY) and g2 in (UNBLOCKED, HIGHWAY))

def both_htt(g1, g2):
    return (g1 in (HTT, HTT_HIGHWAY) and g2 in (HTT, HTT_HIGHWAY))

def only_one_htt(g1, g2):
    return not (both_htt(g1, g2) or both_unblocked(g1, g2))

def both_highway(g1, g2):
    return (g1 in (HIGHWAY, HTT_HIGHWAY) and g2 in (HIGHWAY, HTT_HIGHWAY))

class NavigationGrid:
    def __init__(self, width=160, height=120):
        # add two for blocked boarder around edges. This makes neighbor computation easier.
        self.width = width+2
        self.height = height+2

        # since we only have 5 possible values U1 is overkill but it makes it
        # easier to display
        v = numpy.full((self.width, self.height), UNBLOCKED, dtype=numpy.dtype("U1"))

        # surround inner area with blocked boarder.
        v[:,0] = BLOCKED
        v[:,-1] = BLOCKED
        v[0,:] = BLOCKED
        v[-1,:] = BLOCKED
        self.grid = v

        self.generate_grid()

    @classmethod
    def from_file(cls, file_name):
        raise NotImplementedError

    def get(self, x, y):
        return self[x, y]

    def set(self, x, y, val):
        self[x, y] = val

    def size(self):
        return (self.width, self.height)

    def generate_grid(self):
        raise NotImplementedError

    def neighbors_with_costs(self, p):
        """ Returns a list of neighbors of the point with the costs to move to that point """
        ncosts = list()
        for p2 in self.neighbors(p):
            ncosts.append((p2, self.cost(p, p2)))

        return ncosts
    def neighbors(self, p):
        """ Returns the indices of the neighbors of `p` in the grid."""
        assert(0 < p[0] < self.width - 1)
        assert(0 < p[1] < self.height - 1)

        neighbors = list()

        offsets = [(1, 1),
                   (1, -1),
                   (1, 0),
                   (-1, 1),
                   (-1, -1),
                   (-1, 0),
                   (0, 1),
                   (0, -1)]

        for x in offsets:
            neighbors.append(p+x)

        return neighbors

    def cost(self, p1, p2):
        """ p1, p2 are points in the grid, which must be neighboring. Returns
        the cost to traverse from p1 to p2. Returns +inf if it is not possible
        to travel from p1 to p2."""
        assert(p2 in self.neighbors(p1))
        g1 = self[p1]
        g2 = self[p2]

        if (p1[0] == p2[0]) or (p1[1] == p2[1]):
            dist = 1.0
        else:
            dist = sqrt(2)

        if both_unblocked(g1, g2):
            dist = dist
        if only_one_htt(g1, g2):
            dist = dist * 1.5
        if both_htt(g1, g2):
            dist = dist * 2
        if both_highway(g1, g2):
            dist = dist / 4

        if g1 == BLOCKED or g2 == BLOCKED:
            dist = inf
       
        return dist

    def __getitem__(self, idx):
        # shift by 1 to compensate for border
        idx = idx+(1,1)
        # we have to reverse the index because x = width and y = height, but indexing a numpy array at [x,y] indexes x as the row and y as the column, which is backwards.

        return self.grid[idx[::-1]]

    def __setitem__(self, idx, val):
        # shift by 1 to compensate for border
        idx = idx+(1,1)

        self.grid[idx[::-1]] = val

