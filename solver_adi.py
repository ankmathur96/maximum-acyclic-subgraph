import graph as g
import random

PROCESS_MODE = True
INSTANCE_START = 1 # note that this is inclusive
INSTANCE_END = 621 # note that this is inclusive
N_RANDOM_TRIES = 100000
TEST_INSTANCES = ["eigenvectors1.in", "eigenvectors2.in", "eigenvectors3.in"]

def find_MAS(instance):
    """Overaching function that approximates the maximum acyclic subgraph for an input directed graph"""
    lin_order = instance.linearize()[::-1]
    if lin_order:
        return [1 + x for x in lin_order]
    return compute_result_2(instance) # TEMP
    # for i in range(len(instance.adj_list)):
    #     if instance.out_degree(i) + instance.in_degree(i) > 3:
    #         return [1 + x for x in compute_result_general(instance)]
    # return [1 + x for x in compute_result_small_degree(instance)]

def compute_result_general(instance):
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
    adj_list = instance.adj_list
    if circular(instance):
        return compute_result_small_degree(instance)
    if complete(instance):
        return [x for x in range(len(adj_list))]

    # TO BE DEBUGGED BY ADI/ARNAV
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
        set1 = []
        set2 = []
        for x in range(len(adj_list)): # Iterate through every edge by checking for 1s in adj_list
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
    return new_graph.linearize()[::-1]

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
        return g.DGraph(len(sub_adj_list), sub_adj_list).linearize()[::-1]
    else:
        while has_blue_edge(inst_cpy):
            # TO BE IMPLEMENTED BY ADI/ARNAV
            # Optimally treat any 2- and 3- cycles

            # Find a blue edge

            # ... continue
            break
        return [x for x in range(len(instance.adj_list))]

def compute_result_2(instance):
    return improve_ordering(recursive_split(instance), instance)

def pos_neg_split(nodes, instance):
    positive, negative = [], []
    if len(nodes) <= 1:
        return nodes
    for n in nodes:
        if instance.out_degree(n) - instance.in_degree(n) >= 0:
            positive.append(n)
        else:
            negative.append(n)
    if len(positive) == 0:
        positive.append(negative.pop(0))
    if len(negative) == 0:
        negative.append(positive.pop(0))
    for i in positive:
        for j in negative:
            instance.adj_list[i][j], instance.adj_list[j][i] = 0, 0
    return pos_neg_split(positive, instance) + pos_neg_split(negative, instance)

def recursive_split(instance):
    new_graph = graph_shallow_copy(instance)
    ordering = pos_neg_split(list(range(len(instance.node_list))), new_graph)
    return ordering

def improve_ordering(ordering, instance):
    """Attempts to improve an ordering by looking for back edges and moving nodes to
       reduce those back edges.

    Args:
        ordering (list): The ordering being improved.
        instance (DGraph): The graph which we are ordering.

    Returns:
        list: The improved ordering.

    """
    for _ in range(len(ordering)):
        new_ordering = improve_helper(ordering, instance)
        if (ordering == new_ordering):
            break
    return ordering
def improve_helper(ordering, instance):
    order_map = {}
    for i in range(len(ordering)):
        order_map[ordering[i]] = i
    for u in ordering[::-1]:
        for v in instance.adj_list[u]:
            if (v == 1 and order_map[u] > order_map[v]):
                ordering_copy = ordering[:]
                ordering_copy[order_map[v]] = u
                ordering_copy[order_map[u]] = v
                if (eval_ordering(ordering, instance) < eval_ordering(ordering_copy, instance)):
                    return ordering_copy
    return ordering

def eval_ordering(ordering, instance):
    """ takes in 0 indexed ordering"""
    N = len(instance.adj_list)
    d = instance.adj_list

    ans = ordering

    count = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            if d[ans[i]][ans[j]] == 1:
                count += 1
    return count

def graph_shallow_copy(instance):
    return g.DGraph(len(instance.adj_list), copy(instance.adj_list))
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
    adj_list = instance.adj_list
    return sum([sum([el != 1 for el in row]) for row in adj_list]) == 0


if PROCESS_MODE:
    with open(str(INSTANCE_START) + "_" + str(INSTANCE_END) + '.out', 'w') as o:        
        for x in range(INSTANCE_START, INSTANCE_END + 1):
            print("proccessing instance " + str(x))
            with open("instances/" + str(x) + '.in', 'r') as i:
                instance = process_instance(i)
                result = find_MAS(instance)
                print(' '.join(map(str, result)), file=o)
else:
    print('running on test instances.')
    for instance in TEST_INSTANCES:
        with open(instance + '-out.out', 'w') as o:
            with open(instance, 'r') as i:
                instance = process_instance(i)
                result = find_MAS(instance)
                print(' '.join(map(str, result)) + '\n', file=o)
