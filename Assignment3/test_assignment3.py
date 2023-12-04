from solution import RTBProblem

def solve(fh):
    problem = RTBProblem()
    problem.load(fh)
    problem.setAlgorithm()
    solution = problem.solve()
    if solution == None:
        return 0
    print(problem.initial)
    print(solution.state)
    return 1

def test_public_01():
    with open("public_tests/pub01.dat") as fh:
        assert solve(fh) == 1


def test_public_02():
    with open("public_tests/pub02.dat") as fh:
        assert solve(fh) == 1


def test_public_03():
    with open("public_tests/pub03.dat") as fh:
        # Not solvable
        assert solve(fh) == 0

def test_public_04():
    with open("public_tests/pub04.dat") as fh:
        assert solve(fh) == 1

def test_public_05():
    with open("public_tests/pub05.dat") as fh:
        assert solve(fh) == 1

def test_public_06():
    # Not solvable
    with open("public_tests/pub06.dat") as fh:
        assert solve(fh) == 1
       
def test_public_07():
    with open("public_tests/pub07.dat") as fh:
        assert solve(fh) == 1

def test_public_08():
    with open("public_tests/pub08.dat") as fh:
        assert solve(fh) == 1

def test_public_09():
    with open("public_tests/pub09.dat") as fh:
        assert solve(fh) == 1

def test_public_10():
    with open("public_tests/pub10.dat") as fh:
        assert solve(fh) == 1

