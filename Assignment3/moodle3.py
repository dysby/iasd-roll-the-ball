from time import process_time

from search import (
    uniform_cost_search,
    astar_search,
    iterative_deepening_search,
    breadth_first_graph_search,
    compare_searchers,
)
import solution


def main():
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

    problems = []

    for p_name in p_names:
        problems.append(solution.RTBProblem())
        with open(p_name) as fh:
            problems[-1].load(fh)

    compare_searchers(
        problems=problems,
        header=["Searcher", *p_names],
        searchers=[
#            breadth_first_graph_search,
#            iterative_deepening_search,
            uniform_cost_search,
            astar_search,
        ],
    )


if __name__ == "__main__":
    main()
