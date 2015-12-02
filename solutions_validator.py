import sys

instanceSizes = [4, 1, 7]

def main(argv):
	if len(argv) != 1:
		print "Usage: python solutions_validator.py [path_to_input_file]"
		return
	allPassed = True
	lineIndex = 0
	with open(argv[0], "r") as f:
		for line in f:
			if lineIndex >= len(instanceSizes):
				print "Extra data at end of file"
				return
			result = processTest(line.split(), instanceSizes[lineIndex])
			if result != "solution ok":
				print "Error with test " + str(lineIndex + 1) + ": " + result
				allPassed = False
			lineIndex += 1
	if lineIndex < len(instanceSizes):
		print "File terminated early; missing lines"
		return
	if allPassed:
                print "all solution lines ok"

def processTest(line, N):
	if len(line) != N:
		return "Line must contain " + str(N) + " integers."
	b = [False for i in range(N)]
	for v in line:
		if not v.isdigit():
			return "Line must contain " + str(N) + " integers."
		vertex = int(v) - 1
		if vertex < 0 or vertex >= N:
			return "Each integer must be between 1 and " + str(N) + ", inclusive."
		if b[vertex]:
			return "Each integer in the range 1 to " + str(N) + " must appear exactly once."
		b[vertex] = True
	if not all(b):
		return "Each integer in the range 1 to " + str(N) + " must appear exactly once."

	return "solution ok"

if __name__ == '__main__':
	main(sys.argv[1:])
