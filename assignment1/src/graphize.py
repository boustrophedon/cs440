import numpy
import scipy
import scipy.sparse


def graphize(grid):
	n = grid.shape[0]
	size = n*n
	adj = scipy.sparse.lil_matrix((size, size))

	# make sure the grid is valid

	for row in range(0, n):
		for col in range(0, n):
			adj_ind = col*n + row

			offset = grid[row, col]
			
			horiz = list()
			if row-offset >= 0:
				adj_ind2 = col*n + (row-offset)
				adj[adj_ind, adj_ind2] = 1
			if row+offset < n:
				adj_ind2 = col*n + (row+offset)
				adj[adj_ind, adj_ind2] = 1

			if col-offset >= 0:
				adj_ind2 = (col-offset)*n + row
				adj[adj_ind, adj_ind2] = 1
			if col+offset < n:
				adj_ind2 = (col+offset)*n + row
				adj[adj_ind, adj_ind2] = 1


	return adj

def pprint(mat):
	n = mat.shape[0]
	for row in range(0,n):
		line = list()
		for col in range(0,n):
			line.append(str(int(mat[row, col])))
		print(" ".join(line))

def main():
	g = numpy.mat([[3, 2, 1, 4, 1],
				   [3, 2, 1, 3, 3],
				   [3, 3, 2, 1, 4],
				   [3, 1, 2, 3, 3],
				   [1, 4, 4, 3, 0]])

	pprint(graphize(g))


if __name__ == '__main__':
	main()
