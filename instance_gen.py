import graph as G
import random

def line(num_nodes):
	"""Generates linear chain graph"""
	g = G.DGraph(num_nodes)
	for n in range(num_nodes-1):
		g.edge(n, n+1)
	print("Adjacency matrix for linear graph: ")
	print(g)
	print()
	return g.adj_list

def random_backedges(num_nodes):
	"""Draws an edge from node 0 to every other node, plus a backedge with probability 0.5"""
	g = G.DGraph(num_nodes)
	for n in range(1, num_nodes):
		g.edge(0, n)
		if random.randint(0, 1):
			g.edge(n, 0)
	print("Adjacency matrix for random backedges: ")
	print(g)
	print()
	return g.adj_list

def fully_random(num_nodes):
	"""Generates an entirely random graph"""
	g = G.DGraph(num_nodes)
	for i in range(num_nodes):
		for j in range(num_nodes):
			if j == i:
				continue
			if random.randint(0, 1):
				g.edge(i, j)
	if num_nodes >= 5:
		for num_high_degree in range(random.randint(5, num_nodes//4)):
			i = random.randint(0, num_nodes - 1)
			for deg in range(random.randint(3, num_nodes//4)):
				j = random.randint(0, num_nodes - 1)
				while (j == i):
					j = random.randint(0, num_nodes - 1)
				g.edge(i, j)
	print("Adjacency matrix for random graph (with minimum degree 3): ")
	print(g)
	print()
	return g.adj_list

def single_cycle(num_nodes):
	"""Generates a graph with a single cycle that passes through every node, and no other edges"""
	g = G.DGraph(num_nodes)
	for n in range(num_nodes-1):
		g.edge(n, n+1)
	g.edge(num_nodes - 1, 0)
	print("Adjacency matrix for full cycle: ")
	print(g)
	print()
	return g.adj_list


def write_adj_to_file(name, adj_list, n_nodes):
	with open(name, 'w') as o1:
		print(str(n_nodes), file=o1)
		for i in range(len(adj_list) - 1):
			row = adj_list[i]
			print(' '.join(map(str, row)), file=o1)
		o1.write(' '.join(map(str, adj_list[len(adj_list) - 1])))

N_NODES = 20
if __name__ == "__main__":
	print('Generating instances:')
	print('generating instance 1 - line')
	l_adj_list = line(N_NODES)
	write_adj_to_file('eigenvectors1.in', l_adj_list, N_NODES)
	print('generating instance 2 - backedge')
	backedge_adj_list = random_backedges(N_NODES)
	write_adj_to_file('eigenvectors2.in', backedge_adj_list, N_NODES)
	print('generating instance 3 - random')
	rand_adj_list = fully_random(N_NODES)
	write_adj_to_file('eigenvectors3.in', rand_adj_list, N_NODES)
	print('done generating instances')
	full_cycle(20)
