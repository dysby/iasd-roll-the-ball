#!/bin/sh
timeout -s INT 1m python -m cProfile -o prof solve.py
python -c "import pstats; pstats.Stats('prof').sort_stats('time').print_stats(20)"
