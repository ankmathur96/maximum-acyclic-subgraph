def combine_instances():
	start, end = 1, 50
	lines = []
	done = False
	while not done:
		with open(str(start) + '_' + str(end), 'r') as sol:
			for each_line in sol:
				lines.append(each_line + '\n')
		lines[-1] = lines[-1][:-1]
		start += 50
		end += 50
		if end > 621:
			end = 621
		if start >= 650:
			done = True
	with open('eigenvectors.out', 'w') as out:
		for l in lines:
			out.write(l)

def obj_val(line, N, d, e):
	ans1 = map(lambda x: (int(x) - 1), line)

	count1 = 0.0
	for i in range(N):
		for j in range(i + 1, N):
			if d[ans1[i]][ans1[j]] == 1:
				count1 += 1
	obj_val1 = count1 / e
	return obj_val1

def evaluate_solutions(inst, f1, f2):
	s1 = 0
	s2 = 0
	with open('comparison.out', 'w') as out:
		with open(f1, "r") as fin1:
			with open(f2, "r") as fin2:
			for i in range(1,622):
				inst = str(i) + '.in'
				with open(inst, "r") as fin:
					N = int(fin.readline().split()[0])
					d, e = [[0 for j in range(N)] for i in range(N)], 0
					for i in xrange(N):
						d[i] = map(int, fin.readline().split())
						e += sum(d[i])
				s1_line = fin1.readline().split()
				s2_line = fin2.readline().split()
				s1_obj = obj_val(s1_line)
				s2_obj = obj_val(s2_line)
				if s1_obj > s2_obj:
					print('sol 1 better for', i, file=out)
					s1 += 1
				elif s1_obj == s2_obj:
					print('sols equal', i, file=out)
				else:
					print('sol 2 is better for', i, file=out)
					s2 += 1
	if s1 > s2:
		print('solution 1 better overall')
	elif s1 == s2:
		print('solutions are equivalent')
	else:
		print('solution 2 better overall')
if __name__ == "__main__":
	if len(argv) == 0:
		try:
			combine_instances()
		except Exception:
			print('USAGE: python3 combine_instances.py or python3 combine_instances.py [solution 1].out [solution 2].out')
	elif len(argv) == 2:
		try:
			evaluate_solutions(argv[0], argv[1])
		except Exception:
			print('USAGE: python3 combine_instances.py or python3 combine_instances.py [solution 1].out [solution 2].out')
	else:
		print('USAGE: python3 combine_instances.py or python3 combine_instances.py [solution 1].out [solution 2].out')
