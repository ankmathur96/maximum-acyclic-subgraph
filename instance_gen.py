import graph

def line():
	g = Graph(100)
	for n in range(99):
		g.edge(n, n+1)
	return g.create_a_list()