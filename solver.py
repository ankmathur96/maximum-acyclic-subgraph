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
    """Computes an approximate ordering of the nodes in the graph such that
       the number of valid edges is maximized. See the Maximum Acyclic Subgraph
       problem for more details. 

       This function is run when the input graph is a DAG.

    Args:
        instance (DGraph): The graph which we are ordering.

    Returns:
        list: An ordered list of integers that represent nodes in graph.

    """
    # UNTESTED 
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
    new_graph = g.DGraph(len(adj_list))
    for edge in best_set:
        new_graph.edge(edge[0], edge[1])
    return new_graph.linearize()

def compute_result_2(instance):
    """Computes an 8/9-approximation of the nodes in the graph such that
       the number of valid edges is maximized. See the Maximum Acyclic Subgraph
       problem for more details.

       This function is run when the input graph has degree at most 3.

    Args:
        instance (DGraph): The graph which we are ordering.

    Returns:
        list: An ordered list of integers that represent nodes in graph.

    """
    # UNTESTED
    if has_blue_edge(instance):
        S, inst_cpy = {}, g.DGraph(len(instance.adj_list), copy(instance.adj_list))
        while inst_cpy.is_cycle():
            cycle = inst_cpy.find_cycle()
            for i in range(len(cycle) - 1):
                inst_cpy.adj_list[cycle[i]][cycle[i+1]] = 0
                if cycle[i] not in S:
                    S[cycle[i]] = [cycle[i + 1]]
                else:
                    S[cycle[i]].append(cycle[i + 1])
            inst_cpy.adj_list[cycle[-1][0]] = 0
        for i in range(len(inst_cpy.adj_list)):
            for j in range(len(inst_cpy.adj_list[0])):
                if i != j:
                    if inst_cpy.adj_list[i][j] = 1:
                        if i not in S:
                            S[i] = [j]
                        else:
                            S[i].append(j)
        sub_adj_list = [[0 for _ in range(len(S.keys()))] for _ in range(len(S.keys()))]
        for i in S.keys():
            for j in S[i]:
                sub_adj_list[i][j] = 1
        return g.DGraph(len(sub_adj_list), sub_adj_list)
    else:
        # Algorithm 2


def compute_result_3(instance):
    """Computes a 1/2-approximation of the nodes in the graph such that
       the number of valid edges is maximized. See the Maximum Acyclic Subgraph
       problem for more details.

       This function is run when the conditions specified for compute_result and
       compute_result_2 are not satisfied.

    Args:
        instance (DGraph): The graph which we are ordering.

    Returns:
        list: An ordered list of integers that represent nodes in graph.

    """


####################
# HELPER FUNCTIONS #
####################

def has_blue_edge(instance):
    """Returns true if the input DGraph has a blue edge, and false otherwise"""
    blue_edge = False
    for i in range(len(instance.adj_list)):
        for j in range(len(instance.adj_list[0])):
            if i != j:
                if instance.is_edge(i, j) and instance.in_degree(i) == 2 and instance.out_degree(j) == 2:
                    blue_edge = True
                    break
    return blue_edge

def copy(mat):
    """Returns a shallow copy of an input matrix"""
    return [[mat[i][j] for j in range(len(mat[0]))] for i in range(len(mat))]

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

