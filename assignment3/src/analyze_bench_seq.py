import csv

from collections import defaultdict

def get_rows():
    rows = list()
    with open("data/bench_data_seq.csv") as f:
        rows = [row for row in csv.DictReader(f)]
    return rows

def avg_run_time(data):
    accum = defaultdict(lambda: [0,0])
    for row in data:
        p = (row['w1'], row['w2'])
        accum[p][0] += float(row['runtime'])
        accum[p][1] += 1

    for k in accum:
        accum[k][0] = accum[k][0] / accum[k][1]

    return accum

def avg_cost(data):
    accum = defaultdict(lambda: [0,0])
    for row in data:
        p = (row['w1'], row['w2'])
        accum[p][0] += float(row['path_cost'])
        accum[p][1] += 1

    for k in accum:
        accum[k][0] = accum[k][0] / accum[k][1]

    return accum


def main():
    print("Runtimes: ")

    rows = get_rows()

    runtimes = avg_run_time(rows)
    descending = sorted(runtimes, key=lambda p: runtimes[p][0])
    for p in descending:
        print(' '.join(p) + ":", runtimes[p][0])

    print("Costs: ")

    costs = avg_cost(rows)
    descending = sorted(costs, key=lambda p: costs[p][0])
    for p in descending:
        print(' '.join(p) + ":", costs[p][0], '\\\\')


if __name__ == '__main__':
    main()
