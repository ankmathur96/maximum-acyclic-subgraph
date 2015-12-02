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
	return g.create_adj_list()

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
	return g.create_adj_list()

def fully_random(num_nodes):
	"""Generates an entirely random graph"""
	g = G.DGraph(num_nodes)
	for i in range(num_nodes):
		for j in range(num_nodes):
			if random.randint(0, 1):
				g.edge(i, j)
	print("Adjacency matrix for fully random graph: ")
	print(g)
	print()
	return g.create_adj_list()

if __name__ == "__main__":
	print('Running testing suite:')
	inst_1 = line(20)
	inst_2 = random_backedges(20)
	inst_3 = fully_random(20)
