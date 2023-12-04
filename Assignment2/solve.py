import solution

problem = solution.RTBProblem()
problem.setAlgorithm()

with open("public_tests/pub07.dat") as fh:
    problem.load(fh)

print(problem.initial)
print(problem.N)
solution = problem.solve()
print(solution)
