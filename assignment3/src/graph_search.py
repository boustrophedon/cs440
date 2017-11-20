from math import inf,sqrt

from heapq import *

def empty_heuristic(start, goal):
    return 0

def euclidean_distance(start, goal):
    return 0.25*sqrt( (start[0] - goal[0])**2 + (start[1] - goal[1])**2 )


class GraphSearch:
    """ Implements Weighted A* with parameters for heuristic and weight so that
    it collapses to regular A* with weight = 1 and Dijkstra's with heuristic
    constant 0. The heuristic function is only passed in the current
    coordinates and the goal coordinates."""
    def __init__(self, grid, heuristic=empty_heuristic, weight=1):
        self.grid = grid
        self.weight = weight
        self.heuristic = heuristic


    def search(self):
        """ Returns a list of coordinates representing the best path found by
        the algorithm from `self.grid.goal` to `self.grid.start`, including both
        endpoints, or None if there is no path. Note that the path returned
        begins at goal and ends at start."""
        start = self.grid.start
        goal = self.grid.goal
        cost_from_start = dict() # 'g()'
        cost_from_start[start] = 0
        preds = dict()
        preds[start] = None

        # actually a heap
        fringe = list()
        heappush(fringe, (0+self.heuristic(start, goal)*self.weight, start) )

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
                if self.grid.is_blocked(neighbor):
                    visited.add(neighbor)
                    continue

                if not in_heap(fringe, neighbor):
                    cost_from_start[neighbor] = inf
                    preds[neighbor] = None

                shortest_to_neighbor = cost_from_start[curr] + cost
                if shortest_to_neighbor >= cost_from_start[neighbor]:
                    continue
                else:
                    preds[neighbor] = curr
                    cost_from_start[neighbor] = shortest_to_neighbor

                    remove_from_heap(fringe, neighbor)

                    heappush(fringe, (shortest_to_neighbor + \
                        self.weight*self.heuristic(neighbor, goal), neighbor)) 

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

