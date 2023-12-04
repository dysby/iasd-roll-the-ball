from time import process_time

from search import uniform_cost_search, astar_search
import solution
from metrics import report_counts, CountCalls


def main(p_name="public_tests/pub01.dat"):

    # report((uniform_cost_search_graph, astar_search_graph),
    #   (problem1, ))

    # p1 = solution.RTBProblem()
    # with open("public_tests/pub01.dat") as fh:
    #     p1.load(fh)

    # report((uniform_cost_search, astar_search),
    #    (p1, ))

    problem1 = CountCalls(solution.RTBProblem())
    t10 = process_time()
    with open(p_name) as fh:
        problem1.load(fh)
    result1 = uniform_cost_search(problem1)
    counts1 = problem1._counts
    counts1.update(goal=len(result1.path()), cost=result1.path_cost)
    t11 = process_time()
    problem2 = CountCalls(solution.RTBProblem())
    t20 = process_time()
    with open(p_name) as fh:
        problem2.load(fh)
    result2 = astar_search(problem2)
    counts2 = problem2._counts
    counts2.update(goal=len(result2.path()), cost=result2.path_cost)
    t21 = process_time()

    report_counts(counts1, f"{p_name} - uniform")
    report_counts(counts2, f"{p_name} - astar")


if __name__ == "__main__":
    p_names = [
        "public_tests/pub01.dat",
        "public_tests/pub02.dat",
        "public_tests/pub03.dat",
        "public_tests/pub04.dat",
        "public_tests/pub05.dat",
        "public_tests/pub06.dat",
        "public_tests/pub07.dat",
        "public_tests/pub08.dat",
        "public_tests/pub09.dat",
        "public_tests/pub10.dat",
    ]
    for p_name in p_names:
        main(p_name)
