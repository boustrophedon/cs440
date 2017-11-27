import os
import time

import csv

from navigation_grid import *
from graph_search import *
from sequential_search import *

fields = ['map', 'w1', 'w2', 'path_cost', 'runtime']

def run_bench(m, grid):
    output = list()

    weights = [1.5, 2.0]

    for w1 in weights:
        for w2 in weights:
            data = dict()
            start = time.time()

            searcher = SequentialSearch(grid, w1, w2)
            path_cost = grid.path_cost(searcher.search()) 

            end = time.time()
            

            runtime = end-start

            data['map'] = m
            data['w1'] = w1
            data['w2'] = w2
            data['path_cost'] = path_cost
            data['runtime'] = runtime

            output.append(data)

    return output

def main():
    maps = os.listdir("maps")

    data = list()
    for m in maps:
        grid = NavigationGrid.from_file("maps/"+m)
        data += run_bench(m, grid)

    with open('data/bench_data_seq.csv', 'w', newline='') as output:
        bench_out = csv.DictWriter(output, fieldnames=fields)
        bench_out.writeheader()
        for d in data:
            bench_out.writerow(d)

if __name__ == '__main__':
    main()
