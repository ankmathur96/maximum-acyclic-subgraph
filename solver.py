import graph as g
import random

PROCESS_MODE = False
N_INSTANCES = 400
N_RANDOM_TRIES = 1000
TEST_INSTANCES = ['test.in']

def process_instance(f):
    """Parses the instance and returns the corresponding graph.

    Args:
        f (TextIOWrapper): The file being read.

    Returns:
        DGraph: The directed graph described by the file.

    """
    num_nodes = int(f.readline())
    adj_matrix = []
    instance = g.DGraph(num_nodes)
    for x in range(num_nodes):
        line = f.readline().split()
        for i, edge in enumerate(line):
            if (int(edge) == 1):
                instance.edge(int(x), int(i))
    return instance

def compute_result(instance):
    """Comutes an approximate ordering of the nodes in the graph such that
       the number of valid edges is maximized. See the Maximum Acyclic Subgraph
       problem for more details.

    Args:
        instance (DGraph): The graph which we are ordering.

    Returns:
        list: An ordered list of integers that represent nodes in graph.

    """
    # first check whether the graph is linear, if so, you're done.
    lin_order = instance.linearize()
    if (lin_order != []):
        return lin_order
    # try the same thing, except with circular graphs (edge cases)
    circular = False # FIX THIS
    if (circular):
        return [] # FIX THIS
    # if fully connected, return any any arbitrary ordering of the nodes.
    adj_list = instance.create_adj_list()
    # this is a one liner to check if all edges are present
    if ((sum([sum([el != 1 for el in row]) for row in adj_list]) == 0)):
        return [x for x in range(len(adj_list))]
    # ACTUAL ALGORITHM:
    # label the vertices such that you can say one set of the graph
    # has edges where the edge (n1, n2) has n1 < n2 and the other set has n1 > n2.
    # Neither of these will have cycles. Pick the one with larger cardinality.
    # Repeat several times and take the best ordering.
    # Linearize and produce a valid ranking at the end.
    best_set = []
    for i in range(N_RANDOM_TRIES):
        labels = [x for x in range(len(adj_list))]
        random.shuffle(labels)
        set1 = [] # make these actually sets # FIX THIS
        set2 = [] # make these actually sets # FIX THIS
        for x in range(len(adj_list)):# Iterate through every edge by checking for 1s in adj_list
        	for y in range(len(adj_list[x])):
        		if adj_list[x][y] == 1:
		            if labels[x] < labels[y]:
		                set1.append((x,y))
		            else:
		                set2.append((x,y))
        larger_set = set1 if len(set1) > len(set2) else set2
        if (len(larger_set) > len(best_set)):
            best_set = larger_set
    new_graph = DGraph(len(adj_list))
    for edge in best_set:
        new_graph.edge(edge[0], edge[1])
    return new_graph.linearize()

if PROCESS_MODE:
    with open('eigenvectors.out', 'w') as o:        
        for x in range(N_INSTANCES):
            with open(str(x) + '.in', 'r') as i:
                instance = process_instance(i)
                result = compute_result(instance)
                print(' '.join(map(str, result)) + '\n', file=o)
else:
    print('running on test instances.')
    for instance in TEST_INSTANCES:
        with open(instance + '-out.out', 'w') as o:
            with open(instance, 'r') as i:
                instance = process_instance(i)
                result = compute_result(instance)
                print(' '.join(map(str, result)) + '\n', file=o)

