from math import inf

from heapq import *

def empty_heuristic(start, goal):
    return 0

class GraphSearch:
    """ Implements Weighted A* with parameters for heuristic and weight so that
    it collapses to regular A* with weight = 1 and Dijkstra's with heuristic
    constant 0. The heuristic function is only passed in the current
    coordinates and the goal coordinates."""
    def __init__(self, grid, weight=1, heuristic=empty_heuristic):
        self.grid = grid
        self.weight = weight
        self.heuristic = heuristic

        self.cost_from_start = dict() # 'g()'

    def search(self):
        """ Returns a list of coordinates representing the best path found by
        the algorithm from `self.grid.goal` to `self.grid.start`, including both
        endpoints, or None if there is no path. Note that the path returned
        begins at goal and ends at start."""
        start = self.grid.start
        goal = self.grid.goal
        self.cost_from_start[start] = 0
        preds = dict()
        preds[start] = None

        # actually a heap
        fringe = list()
        heappush(fringe, (0+self.heuristic(start, goal), start) )

        visited = set()

        count = 0
        while not len(fringe) == 0:
            f, curr = heappop(fringe)

            if curr == goal:
                return self.get_goal_path(preds)
            visited.add(curr)
            for neighbor, cost in self.grid.neighbors_with_costs(curr):
                if neighbor in visited:
                    continue

                if not in_heap(fringe, neighbor):
                    self.cost_from_start[neighbor] = inf
                    preds[neighbor] = None

                shortest_to_neighbor = self.cost_from_start[curr] + cost
                if shortest_to_neighbor >= self.cost_from_start[neighbor]:
                    continue
                else:
                    preds[neighbor] = curr
                    self.cost_from_start[neighbor] = shortest_to_neighbor

                    remove_from_heap(fringe, neighbor)

                    heappush(fringe, (shortest_to_neighbor + self.heuristic(neighbor, goal), neighbor)) 

        return None

    def get_goal_path(self, preds):
        path = [self.grid.goal,]
        current = preds[self.grid.goal]
        while current is not None:
            path.append(current)
            current = preds[current]
        return path

# TODO use/implement treap instead of heapq to get logn removes?
def remove_from_heap(heap, point):
    x = None
    for cost, p in heap:
        if p == point:
            x = (cost, p)
            heap.remove(x)
            heapify(heap)
            break

def in_heap(heap, point):
    for _, p in heap:
        if p == point:
            return True

    return False

