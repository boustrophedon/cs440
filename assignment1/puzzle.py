import numpy as np
from numpy import random
from queue import Queue
from tree import Tree


class Puzzle(object):
    def __init__(self, n):
        self.n = n
        self.puzzle = []
        self.tree = Tree(self)
        r_min = 1
        r_max = n
        c_min = 1
        c_max = n
        for r in range(0, n):
            l = []
            for c in range(0, n):
                #l.append(str(random.randint(n)))
                l.append(random.randint(1,  np.amax([r_max - r, r - r_min, c_max - c, c - c_min])))
            self.puzzle.append(list(l))
        self.puzzle[n-1][n-1] = 0

    def __str__(self):
        return ''.join((str(e) + '\n') for e in self.puzzle)

    def bfs(self):
        result = []
        for r in range(0, self.n):
            l = []
            for c in range(0, self.n):
                l.append(-1)
            result.append(list(l))
        q = Queue()
        q.enqueue((0,0,0))
        while not q.isempty():
            current = q.dequeue().data
            self.tree.insert(current[0], current[1], current[2])
            #print(current)
            x = current[0]
            y = current[1]
            step = current[2]
            result[x][y] = step
            if x + self.puzzle[x][y] < self.n and result[x + self.puzzle[x][y]][y] == -1:
                q.enqueue(((x + self.puzzle[x][y]), y, step + 1))
            if x - self.puzzle[x][y] > -1 and result[x - self.puzzle[x][y]][y] == -1:
                q.enqueue(((x - self.puzzle[x][y]), y, step + 1))
            if y + self.puzzle[x][y] < self.n and result[x][y + self.puzzle[x][y]] == -1:
                q.enqueue((x, (y + self.puzzle[x][y]), step + 1))
            if y - self.puzzle[x][y] > -1 and result[x][y - self.puzzle[x][y]] == -1:
                q.enqueue((x, (y - self.puzzle[x][y]), step + 1))
        print(''.join((str(e) + '\n') for e in result))
        print(self.tree)
        return result

'''
    def bfs_no_tree(self):
        result = []
        for r in range(0, self.n):
            l = []
            for c in range(0, self.n):
                l.append(-1)
            result.append(list(l))
        q = Queue()
        q.enqueue((0,0,0))
        while not q.isempty():
            current = q.dequeue().data
            #print(current)
            x = current[0]
            y = current[1]
            step = current[2]
            result[x][y] = step
            if x + self.puzzle[x][y] < self.n and result[x + self.puzzle[x][y]][y] == -1:
                q.enqueue(((x + self.puzzle[x][y]), y, step + 1))
            if x - self.puzzle[x][y] > -1 and result[x - self.puzzle[x][y]][y] == -1:
                q.enqueue(((x - self.puzzle[x][y]), y, step + 1))
            if y + self.puzzle[x][y] < self.n and result[x][y + self.puzzle[x][y]] == -1:
                q.enqueue((x, (y + self.puzzle[x][y]), step + 1))
            if y - self.puzzle[x][y] > -1 and result[x][y - self.puzzle[x][y]] == -1:
                q.enqueue((x, (y - self.puzzle[x][y]), step + 1))
        print(''.join((str(e) + '\n') for e in result))
        return result
'''

'''
p = Puzzle(11)
print(p)

'''
#result[current[0]][current[1]] = current[2] #should be number of steps

'''

            if current[2] + self.puzzle[current[0]][current[1]] < self.n and self.puzzle[current[0] + puzzle[current[current[2]][current[1]] != 0:
                q.enqueue((current[0], current[1], self.puzzle[current[0] + self.puzzle[current[0]][current[1]]][current.y]))
            if current[0] - self.puzzle[current[0]][current[1]] > -1 and self.puzzle[current[0]][current[1]] != 0:

'''
