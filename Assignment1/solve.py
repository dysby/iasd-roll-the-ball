#!/usr/bin/env python3
import sys

from solution import RTBProblem

def main():
    if len(sys.argv) > 1:
        board = RTBProblem()
        with open(sys.argv[1], "r") as fh:
            board.load(fh)
        # print_board(board)
        if board.isSolution():
            print("Is solution")
        else:
            print("Not solution")

    else:
        print(f"Usage: {sys.argv[0]} <filename>")

if __name__=='__main__':
    main()