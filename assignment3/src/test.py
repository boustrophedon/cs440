from grid_gui import run_gui
from grid_generator import GridGenerator
from navigation_grid import *
from graph_search import *

# no testing framework because idgaf and initially this didn't have actual real
# tests

def test_gui():
    run_gui()

def test_gen():
    gen = GridGenerator(width=100, height=80)
    print(gen.gen_grid().serialize())

def test_search_nopath():
    print("Test search no path")
    grid = NavigationGrid(10, 10)
    grid.start = (0,0)
    grid.goal =  (0,2)

    grid[0,1] = BLOCKED
    grid[1,1] = BLOCKED
    grid[1,0] = BLOCKED

    search = GraphSearch(grid)
    result = search.search()
    if result is None:
        print("Test passed.")
    else:
        print(grid.path_cost(result))
        print("Test failed, returned path:", ' '.join(map(str, result)))

def test_search_neighbors():
    print("Test search neighbors")
    grid = NavigationGrid(10, 10)
    grid.start = (0,0)
    grid.goal = (0, 1)

    search = GraphSearch(grid)
    result = search.search()
    expected = [(0,1), (0,0)]
    if result is not None:
        if result == expected:
            print("Test passed.")
        else:
            print("Test failed. Path:", ' '.join(map(str, result)))
            print("Expected:", ' '.join(map(str, expected)))
    else:
        print("Test failed, no path found.")

def test_search_obstacle():
    print("Test search obstacle")
    grid = NavigationGrid(10, 10)
    grid.start = (0,0)
    grid.goal = (0,2)
    grid[0,1] = BLOCKED
    grid[1,1] = BLOCKED
    # s o o
    # b b o
    # g o o
    search = GraphSearch(grid)
    result = search.search()
    expected = [(0,2), (1,2), (2,1), (1,0), (0,0)]
    if result is not None:
        if result == expected:
            print("Test passed.")
        else:
            print("Test failed. Path:", ' '.join(map(str, result)))
            print("Expected:", ' '.join(map(str, expected)))
    else:
        print("Test failed, no path found.")

def test_search_one_away():
    print("Test search one away")
    grid = NavigationGrid(10, 10)
    grid.start = (0,0)
    grid.goal = (0,2)

    search = GraphSearch(grid)
    result = search.search()
    expected = [(0,2), (0,1), (0,0)]
    if result is not None:
        if result == expected:
            print("Test passed.")
        else:
            print("Test failed. Path:", ' '.join(map(str, result)))
            print("Expected:", ' '.join(map(str, expected)))
    else:
        print("Test failed, no path found.")

def test_search_htt():
    print("Test HTT terrain")
    grid = NavigationGrid(10, 2)
    grid.start = (0,0)
    grid.goal = (9,0)
    for i in range(1, 9):
        grid[i,0] = HTT


    search = GraphSearch(grid)
    result = search.search()
    expected = [grid.goal,]
    for i in range(8, 0, -1):
        expected.append((i, 1))
    expected.append(grid.start)
    if result is not None:
        if result == expected:
            print("Test passed.")
        else:
            print("Test failed. Path:", ' '.join(map(str, result)))
            print("Expected:", ' '.join(map(str, expected)))
    else:
        print("Test failed, no path found.")

def test_ucs_vs_a_star():
    print("Test UCS vs A*")
    grid = GridGenerator(width=120, height=100).gen_grid()

    search_ucs = GraphSearch(grid)
    search_euclidean = GraphSearch(grid, heuristic=euclidean_distance)

    result_ucs = search_ucs.search()
    result_euclidean = search_euclidean.search()

    if result_ucs is None:
        print("ucs result is None, serializing grid to ucs_result.txt")
        with open("ucs_result.txt", "w") as f:
            f.write(grid.serialize())

    assert(result_euclidean is not None)

    ucs_cost = grid.path_cost(result_ucs)
    euclidean_cost = grid.path_cost(result_euclidean)

    if ucs_cost != euclidean_cost:
        print("UCS result:")
        print(result_ucs)
        print("Euclidean result:")
        print(result_euclidean)
        print("Costs, ucs, euclidean:")
        print(ucs_cost)
        print(euclidean_cost)
    else:
        print("Test passed")

def test_weighted_a_star():
    print("Test weighted A*")
    grid = GridGenerator(width=120, height=100).gen_grid()
    search_ucs = GraphSearch(grid)
    search_weighted = GraphSearch(grid, heuristic=euclidean_distance, weight = 5)

    result_ucs = search_ucs.search()
    result_weighted = search_weighted.search()

    assert(result_weighted is not None)
    ucs_cost = grid.path_cost(result_ucs)
    weighted_cost = grid.path_cost(result_weighted)

    assert(weighted_cost <= 5*ucs_cost)
    print("weighted cost:", weighted_cost)
    print("ucs cost:", ucs_cost)

    print("Test passed")
if __name__ == '__main__':
    test_search_nopath()
    print()
    test_search_neighbors()
    print()
    test_search_obstacle()
    print()
    test_search_one_away()
    print()
    test_search_htt()
    print()
    test_ucs_vs_a_star()
    print()
    test_weighted_a_star()
    print()
