from typing import List, TextIO

import search
from tiles import Tile, Empty, Flow, tile_factory
from flow_rules import follow_func, flow_init


class RTBProblem(search.Problem):
    def init(self):
        """
        Method that instantiate your class. You can change the content of this. self.initial is where
        the initial state of the puzzle should be saved.
        """
        super().__init__(None)
        self.N = 0
        # self.initial: List[List[Tile]] = [[]]

    def load(self, fh: TextIO):
        """Loads a RTB puzzle from the file object fh. You may initialize self.initial here."""
        board = []

        for line in fh.read().splitlines():
            if line[0] == "#":
                # we don't care for comments
                continue
            elif line[0] in "013456789":
                # line start with a digit, it must be the problem size definition line.
                self.N = int(line)
            else:
                # all other lines are, in sequence, corresponding to each board line configuration.
                row = [tile for tile in line.split(" ")]
                board += row

        self.initial = tuple(board)

    def isSolution(self):
        """returns 1 if the loaded puzzle is a solution, 0 otherwise."""
        # Find initial tile from board
        board = self.initial

        def _find_init():
            for idx, tile in enumerate(board):
                if tile in (
                    "initial-left",
                    "initial-right",
                    "initial-top",
                    "initial-down",
                ):
                    return ((idx // self.N, idx % self.N), flow_init[tile])
            raise ValueError("did not find initial tile")

        current_loc, flow = _find_init()

        print(flow, current_loc, board[current_loc[0] * self.N + current_loc[1]])
        while True:
            current_loc, flow = follow_func[
                board[current_loc[0] * self.N + current_loc[1]]
            ](current_loc, flow)
            print(flow, current_loc, board[current_loc[0] * self.N + current_loc[1]])

            if (
                flow == Flow.ERROR
                or current_loc[0] < 0
                or current_loc[0] >= self.N
                or current_loc[1] < 0
                or current_loc[1] >= self.N
            ):
                return 0

            if board[current_loc[0] * self.N + current_loc[1]] in (
                "goal-top",
                "goal-down",
                "goal-left",
                "goal-right",
            ):
                # final flow test to goal tile
                current_loc, flow = follow_func[
                    board[current_loc[0] * self.N + current_loc[1]]
                ](current_loc, flow)
                if flow == Flow.ERROR:
                    return 0
                return 1
