PROCESS_MODE = False
N_INSTANCES = 400

def process_instance(f):
	n_nodes = int(f.readline())
	a_list = []
	for x in range(n_nodes):
		a_list.append(f.readline().split())
	return a_list

def compute_result(a_list):
	#first check whether the graph is linear, if so, you're done.
	# try the same thing, except with circular graphs (edge cases)
	# label the vertices such that you can say one set of the graph
	# has edges where the edge (n1, n2) has n1 < n2 and the other set has n1 > n2.
	# Neither of these will have cycles. Pick the one with larger carindality.
	# linearize and produce a valid ranking at the end.
	# THE FOLLOWING IS BOILERPLATE - IT DOES NOT WORK PROPERLY.
	return [x for x in range(len(a_list))]

if PROCESS_MODE:
	with open('eigenvectors.out', 'w') as o:		
		for x in range(N_INSTANCES):
			with open(str(x) + '.in', 'r') as i:
				a_list = process_instance(i)
				result = compute_result(a_list)
				print(' '.join(map(str, result)) + '\n', file=o)
else:
	print('running on test instance.')
	with open('test-out.out', 'w') as o:
		with open('test.in', 'r') as i:
			a_list = process_instance(i)
			result = compute_result(a_list)
			print(' '.join(map(str, result)) + '\n', file=o)