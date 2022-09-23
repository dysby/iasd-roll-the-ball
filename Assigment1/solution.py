from typing import List, TextIO

from aimacode import search
from tiles import *

class RTBProblem(search.Problem):
    def init(self):
        """
        Method that instantiate your class. You can change the content of this. self.initial is where 
        the initial state of the puzzle should be saved.
        """
        super().__init__(None)
        # self.initial: List[List[Tile]] = [[]]

    def load(self, fh: TextIO):
        """Loads a RTB puzzle from the file object fh. You may initialize self.initial here."""
        offset = 0  # to account for comment and board dimention definition lines. after comment lines and board dimention this offset will represent the line number where the board configuration starts.

        """
        This is the board/grid of the game it is a list of lists in each position it will have a Tile object.
        """
        board: List[List[Tile]] = [[]]

        for y, line in enumerate(fh.read().splitlines()):
            if line[0] == "#":
                offset += 1
                # we don't care for comments
                continue
            elif line[0] in "013456789":
                # line start with a digit, it must be the problem size definition line.
                N = int(line)
                board = [[None for _ in range(N)] for _ in range(N)]
                offset += 1
            else:
                # all other lines are, in sequence, corresponding to each board line configuration.
                for x, name in enumerate(line.split(' ')):
                    board[y-offset][x] = tile_factory(name)

        self.initial = board

    def isSolution(self):
        """returns 1 if the loaded puzzle is a solution, 0 otherwise."""
        # Find initial tile from board
        def _find_init():
            loc = (0, 0)
            for y, line in enumerate(self.initial):
                for x, tile in enumerate(line):
                    if isinstance(tile, (InitialTop, InitialDown, InitialRight, InitialLeft)):
                        loc = (y, x)
                        return loc

        current_loc = _find_init()
        flow = set_initial_flow(self.initial[current_loc[0]][current_loc[1]])

        print(flow, current_loc, self.initial[current_loc[0]][current_loc[1]].__class__.__name__)
        while True:
            current_loc, flow = self.initial[current_loc[0]][current_loc[1]].follow(current_loc, flow)
            print(flow, current_loc, self.initial[current_loc[0]][current_loc[1]].__class__.__name__)
            if flow == Flow.ERROR:
                return 0
            if isinstance(self.initial[current_loc[0]][current_loc[1]], (GoalTop, GoalDown, GoalRight, GoalLeft)):
                # final flow test to goal tile
                current_loc, flow = self.initial[current_loc[0]][current_loc[1]].follow(current_loc, flow)
                if flow == Flow.ERROR:
                    return 0
                return 1
            


def set_initial_flow(tile: Tile) -> Flow:
    if isinstance(tile, InitialTop):
        return Flow.DOWN
    elif isinstance(tile, InitialDown):
        return Flow.TOP
    elif isinstance(tile, InitialRight):
        return Flow.LEFT
    elif isinstance(tile, InitialLeft):
        return Flow.RIGHT
    else:
        raise ValueError


