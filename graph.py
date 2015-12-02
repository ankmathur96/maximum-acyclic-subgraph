class DGraph():
	"""Directed Graph class"""
	# Graph class: 0-indexed nodes and creates an adjacency list.
	# Consider switching to one of Python's native Graph classes later.
	def __init__(self, n_nodes):
		self.node_list = []
		for x in range(n_nodes):
			self.node_list.append(Node(x))

	def edge(self, n1, n2):
		"""Generates an edge between nodes n1 and n2"""
		if n1 >= len(self.node_list) or n2 >= len(self.node_list):
			raise IndexError('One of the nodes is out of bounds.')
		self.node_list[n1].children.add(n2)

	def create_adj_list(self):
		"""Returns an adjacency matrix representation of self"""
		adj_list = []
		n_nodes = len(self.node_list)
		for n in self.node_list:
			if len(n.children) > 0:
				adj_list.append([1 if x in n.children else 0 for x in range(n_nodes)])
			else:
				adj_list.append([0 for x in range(n_nodes)])
		return adj_list

	def print_adj_list(self):
		"""Outputs easy-view formatted representation of the adjacency matrix for this graph"""
		adj_list = self.create_adj_list()
		result = [' '.join(str(val).ljust(3) for val in adj_list[i]) for i in range(len(adj_list))]
		return '\n'.join(result)

	def __repr__(self):
		return str(self.print_adj_list())
	def __str__(self):
		return repr(self)

class Node():
	"""Simple node class"""
	def __init__(self, n_num, children=None):
		self.id = n_num
		if children is None:
			self.children = set()
		else:
			self.children = set()

