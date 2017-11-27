import os
import time

import csv

from navigation_grid import *
from graph_search import *
from sequential_search import *

fields = ['map', 'algo', 'path_cost', 'runtime', 'heuristic', 'weight']
heuristics = {empty_heuristic:"ucs", euclidean_admissible:"euclid_adm", \
        manhattan:"manhattan", chebyshev:"chebyshev", euclidean:"euclidean", \
        dist_squared:"dist_squared"}

def run_bench(m, grid):
    output = list()

    weights = [1.0, 1.5, 2.0]

    for heuristic,hname in heuristics.items():
        for weight in weights:
            data = dict()
            if heuristic == empty_heuristic and weight != 1.0:
                continue

            start = time.time()

            searcher = GraphSearch(grid, heuristic=heuristic, weight=weight)
            path_cost = grid.path_cost(searcher.search()) 

            end = time.time()
            

            runtime = end-start

            data['map'] = m
            if heuristic == empty_heuristic:
                data['algo'] = 'ucs'
            elif weight == 1.0:
                data['algo'] = 'astar'
            else:
                data['algo'] = 'weighted_astar'
            data['path_cost'] = path_cost
            data['runtime'] = runtime
            data['heuristic'] = hname
            data['weight'] = weight

            output.append(data)

    return output

def main():
    maps = os.listdir("maps")

    data = list()
    for m in maps:
        grid = NavigationGrid.from_file("maps/"+m)
        data += run_bench(m, grid)

    with open('data/bench_data.csv', 'w', newline='') as output:
        bench_out = csv.DictWriter(output, fieldnames=fields)
        bench_out.writeheader()
        for d in data:
            bench_out.writerow(d)

if __name__ == '__main__':
    main()
