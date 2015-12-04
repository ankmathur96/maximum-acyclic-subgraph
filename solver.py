import graph as g
import random

PROCESS_MODE = False
N_INSTANCES = 400
N_RANDOM_TRIES = 1000
TEST_INSTANCES = ['test.in']

def find_MAS(instance):
    """Overaching function that approximates the maximum acyclic subgraph for an input directed graph"""
    lin_order = instance.linearize()
    if lin_order:
        return compute_result_general(instance, lin_order)
    for i in range(len(instance.adj_list)):
        if instance.out_degree(i) + instance.in_degree(i) > 3:
            return compute_result_general(instance)
    return compute_result_small_degree(instance)

def compute_result_general(instance, linearization=None):
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
    # Special cases
    if linearization != None:
        return longest_increasing_subsequence(instance, linearization)
    if circular(instance):
        return compute_result_small_degree(instance)
    if complete(instance):
        return [x for x in range(len(adj_list))]

    # ACTUAL ALGORITHM:
    # label the vertices such that you can say one set of the graph
    # has edges where the edge (n1, n2) has n1 < n2 and the other set has n1 > n2.
    # Neither of these will have cycles. Pick the one with larger cardinality.
    # Repeat several times and take the best ordering.
    # Linearize and produce a valid ranking at the end.
    best_set = []
    for i in range(N_RANDOM_TRIES):
        labels = [x for x in range(len(instance.adj_list))]
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

def compute_result_small_degree(instance):
    """Computes an 8/9-approximation of the nodes in the graph such that
       the number of valid edges is maximized. See the Maximum Acyclic Subgraph
       problem for more details.

       This function is run when the input graph has degree at most 3.

    Args:
        instance (DGraph): The graph which we are ordering.

    Returns:
        list: An ordered list of integers that represent nodes in graph.

    """
    S, inst_cpy = {}, g.DGraph(len(instance.adj_list), copy(instance.adj_list))
    if not has_blue_edge(instance):
        while inst_cpy.is_cycle():
            cycle = inst_cpy.find_cycle()
            for i in range(len(cycle) - 1):
                inst_cpy.adj_list[cycle[i]][cycle[i+1]] = 0
                if cycle[i] not in S:
                    S[cycle[i]] = [cycle[i + 1]]
                else:
                    S[cycle[i]].append(cycle[i + 1])
            inst_cpy.adj_list[cycle[-1]][cycle[0]] = 0
        for i in range(len(inst_cpy.adj_list)):
            for j in range(len(inst_cpy.adj_list[0])):
                if i != j:
                    if inst_cpy.adj_list[i][j] == 1:
                        if i not in S:
                            S[i] = [j]
                        else:
                            S[i].append(j)
        sub_adj_list = [[0 for _ in range(len(inst_cpy.adj_list))] for _ in range(len(inst_cpy.adj_list))]
        for i in S.keys():
            for j in S[i]:
                sub_adj_list[i][j] = 1
        return g.DGraph(len(sub_adj_list), sub_adj_list)
    else:
        while has_blue_edge(inst_cpy):
            # Optimally treat any 2- and 3- cycles

            # Find a blue edge

            # ... continue
            break
        return None

####################
# HELPER FUNCTIONS #
####################
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
    """Returns a shallow copy of the input matrix"""
    return [[mat[i][j] for j in range(len(mat[0]))] for i in range(len(mat))]

def circular(instance):
    """Edge case tester. Returns true if instance is a perfectly circular graph"""
    if sum([sum(row) for row in instance.adj_list]) != len(instance.adj_list):
        return False
    curr_node, nodes = 0, {i : True for i in range(len(instance.adj_list))}
    while True:
        del nodes[curr_node]
        if sum(instance.adj_list[curr_node]) != 1:
            return False
        if not nodes:
            return True

        for i in range(len(instance.adj_list)):
            if instance.adj_list[i][curr_node] == 1:
                curr_node = i
                continue
        

def complete(instance):
    """Returns True if input graph is complete, False otherwise"""
    return sum([sum([el != 1 for el in row]) for row in adj_list]) == 0

def longest_increasing_subsequence():
    """Returns a subgraph containing the longest increasing subsequence of the input linearized DAG"""
    # TO BE IMPLEMENTED

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
                result = find_MAS(instance)
                print(' '.join(map(str, result)) + '\n', file=o)

