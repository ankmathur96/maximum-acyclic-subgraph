PROCESS_MODE = False
N_INSTANCES = 400

def process_instance(f):
	n_nodes = int(f.readline())
	a_list = []
	for x in range(n_nodes):
		a_list.append(f.readline().split())
	return a_list

def compute_result(a_list):
	#linearize and produce a valid ranking at the end.
	return [x for x in range(len(a_list))]

if PROCESS_MODE:
	with open('eigenvectors.out', 'w') as o:		
		for x in range(N_INSTANCES):
			with open(str(x) + '.in', 'r') as i:
				a_list = process_instance(i)
				result = compute_result(a_list)
				print(' '.join(result) + '\n', file=o)
else:
	print('running on test instance.')
	with open('test-out.out', 'w') as o:
		with open('test.in', 'r') as i:
			a_list = process_instance(i)
			result = compute_result(a_list)
			print(' '.join(result) + '\n', file=o)
