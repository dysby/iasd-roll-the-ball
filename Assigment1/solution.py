from typing import List, TextIO

import search
from tiles import Tile, Empty, Flow, tile_factory
from flow_rules import follow_func, flow_init


def board_state(board: List[List[Tile]]) -> List[str]:
    """
    Read Board List of Lists (N x N) and save each Tile 'to string' method output
    to a list. This state, as a list of strings, will be usefull for storage of
    various enviornment state instances and verify if two state instances
    correspond to the same enviornment state.
    """
    state = [str(tile) for row in board for tile in row]
    print(state)
    return state


def state_board(state: List[str]) -> List[List[Tile]]:
    """
    Inverse operation of board_state method. Create a Board N x N with
    'tile' object of correct class
    """
    N = int(len(state) ** (1 / 2))
    board = [[Empty for _ in range(N)] for _ in range(N)]

    # this loop will use mod calculous for accessing the
    # right index of the grid
    for i, tile_name in enumerate(state):
        board[i // N][i % N] = tile_factory(tile_name)

    return board


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
            if flow == Flow.ERROR:
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
