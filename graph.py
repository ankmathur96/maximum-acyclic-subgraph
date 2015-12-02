class Graph():
	# Graph class: 0-indexed nodes and creates an adjacency list.
	# Consider switching to one of Python's native Graph classes later.
	def __init__(self, n_nodes):
		self.node_list = []
		for x in range(n_nodes):
			self.node_list.append(Node(x))

	def edge(self, n1, n2):
		if n1 >= len(self.node_list) or n2 >= len(self.node_list):
			raise IndexError('One of the nodes is out of bounds.')
		self.node_list[n1].children.add(n2)

	def create_a_list(self):
		a_list = []
		n_nodes = len(self.node_list)
		for n in self.node_list:
			if len(n.children) > 0:
				a_list.append([1 if x in n.children else 0 for x in range(n_nodes)])
			else:
				a_list.append([0 for x in range(n_nodes)])
		return a_list

	def __repr__(self):
		return str(self.create_a_list())
	def __str__(self):
		return repr(self)

class Node():
	def __init__(self, n_num, children=None):
		self.id = n_num
		if children is None:
			self.children = set()
		else:
			self.children = set()

if __name__ == "__main__":
	print('Running testing suite:')
	g = Graph(3)
	g.edge(0,1)
	g.edge(1,2)
	g.edge(2,0)
	print(g)

