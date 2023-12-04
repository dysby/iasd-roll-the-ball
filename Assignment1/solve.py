import solution

problem = solution.RTBProblem()
with open("public_tests/pub08.dat") as fh:
    problem.load(fh)

if problem.isSolution() == 0:
    print("Not Solution")
print("Solution")
