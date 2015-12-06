import sys
import traceback
INSTANCES_PATH = 'instances/'
def combine_instances():
    start, end = 1, 50
    lines = []
    done = False
    while not done:
        with open(str(start) + '_' + str(end) + '.out', 'r') as sol:
            for each_line in sol:
                lines.append(each_line)
        start += 50
        end += 50
        if end > 621:
            end = 621
        if start >= 650:
            done = True
    with open('eigenvectors-blah.out', 'w') as out:
        for l in lines:
            out.write(l)

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
    s1 = 0
    s2 = 0
    with open(f1, "r") as fin1:
        with open(f2, "r") as fin2:
            for i in range(1,622):
                inst = INSTANCES_PATH + str(i) + '.in'
                with open(inst, "r") as fin:
                    N = int(fin.readline().split()[0])
                    d, e = [[0 for j in range(N)] for a in range(N)], 0
                    for k in range(N):
                        inst_list = fin.readline().split()
                        d[k] = list(map(int, inst_list))
                        e += sum(d[k])
                s1_line = fin1.readline().split()
                s2_line = fin2.readline().split()
                s1_obj = obj_val(s1_line, N, d, e)
                s2_obj = obj_val(s2_line, N, d, e)
                if s1_obj > s2_obj:
                    print('sol 1 better for ' + str(i))
                    s1 += 1
                elif s1_obj == s2_obj:
                    print('sols are equal for ' + str(i))
                else:
                    print('sol 2 is better for ' + str(i))
                    s2 += 1
    print('*******************************')
    if s1 > s2:
        print('solution 1 better overall')
        print('solution 1:', s1, ',solution2:', s2, ',equal:', 621-s1-s2)
    elif s1 == s2:
        print('solutions are equivalent')
    else:
        print('solution 2 better overall')
        print('solution 1:', s1, ',solution2:', s2, ',equal:', 621-s1-s2)
if __name__ == "__main__":
    argv = sys.argv[1:]
    if len(argv) == 0:
        try:
            combine_instances()
        except Exception:
            traceback.print_exc()
            print('USAGE: python3 compare_instances.py or python3 compare_instances.py [solution 1].out [solution 2].out')
    elif len(argv) == 2:
        try:
            print(argv)
            evaluate_solutions(argv[0], argv[1])
        except Exception:
            traceback.print_exc()
            print('USAGE: python3 compare_instances.py or python3 compare_instances.py [solution 1].out [solution 2].out')
    else:
        print('USAGE: python3 compare_instances.py or python3 compare_instances.py [solution 1].out [solution 2].out')
