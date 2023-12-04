from search import breadth_first_tree_search
from time import process_time

from search import breadth_first_graph_search,  iterative_deepening_search
#from search import uniform_cost_search, astar_search
import solution
from metrics import report_counts, CountCalls


def main(p_name="public_tests/pub01.dat"):

    problem1 = CountCalls(solution.RTBProblem())
    t10 = process_time()
    with open(p_name) as fh:
        problem1.load(fh)
    result1 = breadth_first_tree_search(problem1)
    t11 = process_time()
    problem2 = CountCalls(solution.RTBProblem())
    t20 = process_time()
    with open(p_name) as fh:
        problem2.load(fh)
    result2 = iterative_deepening_search(problem2)
    t21 = process_time()

    report_counts(problem1._counts, f"{p_name} - breadth_first_graph_search")
    report_counts(problem2._counts, f"{p_name} - iterative_deepening_search")


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
