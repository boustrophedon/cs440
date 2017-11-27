from math import inf,sqrt

from collections import defaultdict

from heapq import *

from graph_search import manhattan, chebyshev, chebyshev_admissible, euclidean, euclidean_admissible, dist_squared, empty_heuristic
from graph_search import remove_from_heap


class SequentialSearch:
    def __init__(self, grid, w1, w2):
        self.grid = grid
        self.w1 = w1
        self.w2 = w2
        self.heuristics = [euclidean_admissible, manhattan, chebyshev, euclidean, dist_squared]

        n = len(self.heuristics)
        # g() values
        self.g_values = list()
        # predecessors mapping used to find optimal path after search
        self.preds = list()
        self.fringes = list()
        self.visited = list()

        start = self.grid.start
        for i in range(0, n):
            self.g_values.append(defaultdict(lambda: inf))
            self.g_values[i][start] = 0

            self.preds.append(defaultdict(lambda: None))

            self.fringes.append(list())
            heappush(self.fringes[i], (self.key(start, i), start) )

            self.visited.append(set())

    def key(self, p, i):
        return self.g_values[i][p] + self.w1 * self.heuristics[i](p, self.grid.goal)

    def search(self):
        """ Returns a list of coordinates representing the best path found by
        the algorithm from `self.grid.goal` to `self.grid.start`, including both
        endpoints, or None if there is no path. Note that the path returned
        begins at goal and ends at start."""
        goal = self.grid.goal
        n = len(self.heuristics)

        fringes = self.fringes
        visited = self.visited

        # fringes[0] is the admissible heuristic's fringe
        # fringes[0][0] is the smallest element of that heap
        # the elements are (f_value, point), so we want 
        # fringes[0][0][0] to get the f value
        while fringes[0][0][0] < inf:
            for i in range(1,n):
                if fringes[i][0][0] <= self.w2 * fringes[0][0][0]:
                    f, curr = heappop(fringes[i])
                    if curr == goal:
                        return self.get_goal_path(i)
                    visited[i].add(curr)
                    self.expand_state(curr, i)

                else:
                    f, curr = heappop(fringes[0])
                    if curr == goal:
                        return self.get_goal_path(0)
                    visited[0].add(curr)
                    self.expand_state(curr, 0)

        return None

    def expand_state(self, curr, i):
        fringe = self.fringes[i]
        visited = self.visited[i]

        for neighbor, cost in self.grid.neighbors_with_costs(curr):

            if neighbor in visited:
                continue
            if self.grid.is_blocked(neighbor):
                visited.add(neighbor)
                continue

            shortest_to_neighbor = self.g_values[i][curr] + cost
            if shortest_to_neighbor >= self.g_values[i][neighbor]:
                continue
            else:
                self.preds[i][neighbor] = curr
                self.g_values[i][neighbor] = shortest_to_neighbor

                remove_from_heap(fringe, neighbor)

                heappush(fringe, (self.key(neighbor, i), neighbor)) 

    def get_goal_path(self, i):
        path = [self.grid.goal,]
        current = self.preds[i][self.grid.goal]
        while current is not None:
            path.append(current)
            current = self.preds[i][current]
        return path
