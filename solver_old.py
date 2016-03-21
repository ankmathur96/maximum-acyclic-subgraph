import graph as g
import random

PROCESS_MODE = True
N_INSTANCES = 621
N_RANDOM_TRIES = 1000
TEST_INSTANCES = ["eigenvectors1.in", "eigenvectors2.in", "eigenvectors3.in"]

def find_MAS(instance):
    """Overaching function that approximates the maximum acyclic subgraph for an input directed graph"""
    lin_order = instance.linearize()[::-1]
    if lin_order:
        return [1 + x for x in lin_order]
    for i in range(len(instance.adj_list)):
        if instance.out_degree(i) + instance.in_degree(i) > 3:
            return [1 + x for x in compute_result_general(instance)]
    return [1 + x for x in compute_result_small_degree(instance)]

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
        return compute_result_small_degree_algo1(instance)
    else:
        while has_blue_edge(inst_cpy):
            # TO BE IMPLEMENTED BY ADI/ARNAV

            # Calculate in- and out-degree for each node
            in_degree_list = [0 for _ in range(len(inst_cpy.adj_list))]
            out_degree_list = [0 for _ in range(len(inst_cpy.adj_list))]
            for i in range(len(inst_cpy.adj_list)):
                out_degree_list[i] = sum(inst_cpy.adj_list[i])
                in_degree_list[i] = sum([inst_cpy.adj_list[x][i] for x in range(len(inst_cpy.adj_list))])

            
            for j in range(len(in_degree_list)):
                # Checking for nodes that either only go in, or out
                if in_degree_list[j] == 0 or out_degree_list[j] == 0:
                    for all k in range(len(inst_cpy.adj_list)):
                        if inst_cpy.adj_list[k][j] == 1:
                            if k in S:
                                S[k].append(j)
                            else:
                                S[k] = [j]
                        if inst_cpy[j][k] == 1:
                            if j in S:
                                S[j].append(k)
                            else:
                                S[j] = [k]
                # Contract vertices with in-degree == out-degree == 1
                if (in_degree_list[j] == 1) and (out_degree_list[j] == 1):
                    j_in = ""
                    j_out = ""
                    for l in range(len(inst_cpy.adj_list)):
                        if inst_cpy.adj_list[j][l] == 1:
                            j_out = l
                        if inst_cpy.adj_list[l][j] == 1:
                            j_in = l
                    inst_cpy.adj_list[j_in][j_out] = 1
                    inst_cpy.adj_list[j][j_out] = 0
                    inst_cpy.adj_list[j_in][j] = 0
                for k in range(len(inst_cpy.adj_list)):
                    # Checking for 2-cycles
                    if two_cycle(inst_cpy, j, k):
                        j_edge = ""
                        j_other_node = ""
                        k_edge = ""
                        k_other_node = ""
                        for l in range(len(inst_cpy.adj_list)):
                            if l not == j:
                                # For other out-edges from k
                                if inst_cpy.adj_list[k][l] == 1:
                                    k_edge = "out"
                                    k_other_node = l
                                # For other in-edges to j
                                if inst_cpy.adj_list[l][j] == 1:
                                    j_edge = "in"
                                    j_other_node = l
                            if l not == k:
                                # For other out-edges from j
                                if inst_cpy.adj_list[j][l] == 1:
                                    j_edge = "out"
                                    j_other_node = l
                                # For other in-edges to k
                                if inst_cpy.adj_list[l][k] == 1:
                                    k_edge = "in"
                                    k_other_node = l
                        if (j_edge == "out" and k_edge == "out"):
                            inst_cpy.adj_list[j][j_other_node] = 0
                        if (j_edge == "in" and k_edge == "in"):
                            inst_cpy.adj_list[j_other_node][j] = 0
                    for m in range(len(inst_cpy.adj_list)):
                        # Checking for 3-cycles
                        if three_cycle(inst_cpy, j, k, m):
                            for l in range(len(inst_cpy.adj_list)):
                                if l not == j and l not == k:
                                    # For other in-edges to m
                                    if inst_cpy.adj_list[l][m] == 1:
                                        m_edge = "in"
                                        m_other_node = l
                                    # For other out-edges from m
                                    if inst_cpy.adj_list[m][l] == 1:
                                        m_edge = "out"
                                        m_other_node = l
                                if l not == j and l not == m:
                                    # For other in-edges to k
                                    if inst_cpy.adj_list[l][k] == 1:
                                        k_edge = "in"
                                        k_other_node = l
                                    # For other out-edges from k
                                    if inst_cpy.adj_list[k][l] == 1:
                                        k_edge = "out"
                                        k_other_node = l
                                if l not == k and l not == m:
                                    # For other in-edges to j
                                    if inst_cpy.adj_list[l][j] == 1:
                                        j_edge = "in"
                                        j_other_node = l
                                    # For other out-edges from j
                                    if inst_cpy.adj_list[j][l] == 1:
                                        j_edge = "out"
                                        j_other_node = l
                            if (j_edge == "out" and k_edge == "out" and m_edge == "out"):
                                inst_cpy.adj_list[j][j_other_node] = 0
                            elif (j_edge == "in" and k_edge == "in" and m_edge == "in"):
                                inst_cpy.adj_list[j_other_node][j] = 0
                            elif (j_edge not == k_edge) and (j_edge not == m_edge):
                                if inst_cpy.adj_list[k][j] == 1:
                                    inst_cpy.adj_list[k][j] == 0
                                elif inst_cpy.adj_list[m][j] == 1:
                                    inst_cpy.adj_list[m][j] == 0
                            elif (k_edge not == j_edge) and (k_edge not == m_edge):
                                if inst_cpy.adj_list[j][k] == 1:
                                    inst_cpy.adj_list[j][k] == 0
                                elif inst_cpy.adj_list[m][k] == 1:
                                    inst_cpy.adj_list[m][k] == 0
                            elif (m_edge not == j_edge) and (m_edge not == k_edge):
                                if inst_cpy.adj_list[j][m] == 1:
                                    inst_cpy.adj_list[j][m] == 0
                                elif inst_cpy.adj_list[k][m] == 1:
                                    inst_cpy.adj_list[k][m] == 0
                    # See if there is a blue edge
                    current_blue_edge = []
                    if (inst_cpy.adj_list[j][k] == 1) and (in_degree_list[j] == 2) and (out_degree_list[k] == 2):
                        current_blue_edge.extend([j, k])
                    if len(current_blue_edge) == 2:
                        # If the blue edge is in a component with 9 edges: - FIX
                            # Run recursively on this subgraph - FIX
                        # else:
                            for l in range(len(inst_cpy.adj_list)):
                                if l not == j:
                                    if inst_cpy.adj_list[l][j] == 1:
                                        inst_cpy.adj_list[l][j] == 0
                                        if l in S:
                                            S[l].append(j)
                                        else:
                                            S[l] = [j]

                                if l not == k:
                                    if inst_cpy.adj_list[k][l] == 1:
                                        inst_cpy.adj_list[k][l] == 0
                                        if k in S:
                                            S[k].append(l)
                                        else:
                                            S[k] = [l]
        if not inst_cpy.is_cycle():
            # add all edges of inst_cpy to S
        else:
            # append compute_result_small_degree_algo1(inst_cpy) to S
        # TODO - didn't get to step 3/4
        return [x for x in range(len(instance.adj_list))] # FIX THIS

def compute_result_small_degree_algo1(instance):
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

def two_cycle(instance, i, j):
    """Returns true if there is an edge from i to j and back"""
    return instance.adj_list[i][j] == 1 and instance.adj_list[j][i] == 1
def three_cycle(instance, i, j, m):
    """Returns true if there is an edge from i to j to m to i, 
    or i to m to j to i """
    return (instance.adj_list[i][j] == 1 and instance.adj_list[j][m] == 1 and instance.adj_list[m][i]) or (instance.adj_list[i][m] == 1 and instance.adj_list[m][j] == 1 and instance.adj_list[j][i])

if PROCESS_MODE:
    with open('eigenvectors.out', 'w') as o:        
        for x in range(N_INSTANCES):
            print("proccessing instance" + str(x))
            with open("instances/" + str(x + 1) + '.in', 'r') as i:
                instance = process_instance(i)
                result = find_MAS(instance)
                print(' '.join(map(str, result)) + '\n', file=o)
else:
    print('running on test instances.')
    for instance in TEST_INSTANCES:
        with open(instance + '-out.out', 'w') as o:
            with open(instance, 'r') as i:
                instance = process_instance(i)
                result = find_MAS(instance)
                print(' '.join(map(str, result)) + '\n', file=o)
