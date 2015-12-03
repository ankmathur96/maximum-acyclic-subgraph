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

	def is_edge(self, n1, n2):
		if n2 in self.node_list[n1].children:
			return True
		return False

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
		result = [' '.join(str(val).ljust(2) for val in adj_list[i]) for i in range(len(adj_list))]
		return '\n'.join(result)

	def cycle_util(self, v, visited, recursion_stack):
		if visited[v] == False:
			visited[v] = True
			recursion_stack[v] = True
			adj_vertices = self.node_list[v].children
			for m in adj_vertices:
				if not visited[m] and self.cycle_util(m, visited, recursion_stack):
					return True
				elif recursion_stack[m]:
					return True
		recursion_stack[v] = False
		return False

	def is_cycle(self):
		recursion_stack, visited = [], []
		for i in range(len(self.node_list)):
			visited.append(False)
			recursion_stack.append(False)
		for j in range(len(self.node_list)):
			if self.cycle_util(j, visited, recursion_stack):
				return True
		return False                                                                                         

	def linearize_helper(self, v, visited, linear_order):
		visited[v] = True
		for n in self.node_list[v].children:
			if visited[n] is False:
				self.linearize_helper(n, visited, linear_order)
		linear_order.append(v)

	def linearize(self):
		if self.is_cycle():
			print('IS CYCLE')
			return []
		visited = [False for i in range(len(self.node_list))]
		linear_order = []
		for i in range(len(self.node_list)):
			if visited[i] is False:
				self.linearize_helper(i, visited, linear_order)
		return linear_order[::-1]

	def __repr__(self):
		return self.print_adj_list()
	def __str__(self):
		return repr(self)

class Node():
	"""Simple node class"""
	def __init__(self, n_num, children=None):
		self.id = n_num
		self.pre = None
		self.post = None
		if children is None:
			self.children = set()
		else:
			self.children = set()
if __name__ == "__main__":
	g = DGraph(5)
	g.edge(1,0)
	g.edge(3,1)
	g.edge(0,2)
	g.edge(2,3)
	g.edge(3,4)
	print(g.linearize())
