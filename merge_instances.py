import sys
import traceback

def obj_val(line, N, d, e):
    ans1 = list(map(lambda x: (int(x) - 1), line))
    count1 = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            if d[ans1[i]][ans1[j]] == 1:
                count1 += 1
    if e:
        obj_val1 = count1 / e
    else:
        obj_val1 = 0
    return obj_val1

def evaluate_solutions(f1, f2):
    equal = []
    total = 0
    with open('eigenvectors_merged.out', 'w') as out:
        with open(f1, "r") as fin1:
            with open(f2, "r") as fin2:
                for i in range(1,622):
                    inst = "instances/" + str(i) + '.in'
                    with open(inst, "r") as fin:
                        N = int(fin.readline().split()[0])
                        d, e = [[0 for j in range(N)] for a in range(N)], 0
                        for k in range(N):
                            inst_list = fin.readline().split()
                            d[k] = list(map(int, inst_list))
                            e += sum(d[k])
                    s1_line = fin1.readline()
                    s2_line = fin2.readline()
                    s1_obj = obj_val(s1_line.split(), N, d, e)
                    s2_obj = obj_val(s2_line.split(), N, d, e)
                    if s1_obj >= s2_obj:
                        print(s1_line, file=out)
                        total += s1_obj
                    elif s1_obj == s2_obj:
                        equal.append(i)
                    else:
                        print(s2_line, file=out)
                        total += s2_obj
    print("wrote to eigenvectors_merged_" + str(total) + ".out")
if __name__ == "__main__":
    argv = sys.argv[1:]
    if len(argv) == 2:
        try:
            evaluate_solutions(argv[0], argv[1])
        except Exception as e:
            traceback.print_exc()
            print('USAGE: python3 merge_instances.py or python3 merge_instances.py [solution 1].out [solution 2].out')
    else:
        print('USAGE: python3 merge_instances.py or python3 merge_instances.py [solution 1].out [solution 2].out')
