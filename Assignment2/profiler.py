import cProfile, pstats
import solution


def main():
    problem = solution.RTBProblem()
    problem.setAlgorithm()

    with open("public_tests/pub10.dat") as fh:
        problem.load(fh)

    profiler = cProfile.Profile()
    
    profiler.enable()
    problem.solve()
    profiler.disable()
    
    stats = pstats.Stats(profiler).sort_stats("cumtime")
    stats.print_stats()


# Sort output by Cumulative time
if __name__ == "__main__":
    main()
