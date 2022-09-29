from typing import Tuple
from enum import Enum, auto

import search


class Flow(Enum):
    """
    *Flow* is the direction of an imaginary ball ariving at the current tile, 
    following a correct path from the initial tile.

    For example, if we are on a tile with a exit to the right, the flow will become left, 
    because the next tile will see the ball comming from the left.
    """

    TOP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()
    ERROR = auto()


def follow_initial_left(
    loc: Tuple[int, int], flow: Flow
) -> Tuple[Tuple[int, int], Flow]:
    return ((loc[0], loc[1] - 1), Flow.RIGHT)


def follow_initial_right(
    loc: Tuple[int, int], flow: Flow
) -> Tuple[Tuple[int, int], Flow]:
    return ((loc[0], loc[1] + 1), Flow.LEFT)


def follow_initial_top(
    loc: Tuple[int, int], flow: Flow
) -> Tuple[Tuple[int, int], Flow]:
    return ((loc[0] - 1, loc[1]), Flow.DOWN)


def follow_initial_down(
    loc: Tuple[int, int], flow: Flow
) -> Tuple[Tuple[int, int], Flow]:
    return ((loc[0] + 1, loc[1]), Flow.TOP)


def follow_goal_left(loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
    if flow == Flow.LEFT:
        return (loc, flow)
    return (loc, Flow.ERROR)


def follow_goal_right(loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
    if flow == Flow.RIGHT:
        return (loc, flow)
    return (loc, Flow.ERROR)


def follow_goal_top(loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
    if flow == Flow.TOP:
        return (loc, flow)
    return (loc, Flow.ERROR)


def follow_goal_down(loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
    if flow == Flow.DOWN:
        return (loc, flow)
    return (loc, Flow.ERROR)


def follow_right_left(loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
    if flow == Flow.LEFT:
        return ((loc[0], loc[1] + 1), Flow.LEFT)
    elif flow == Flow.RIGHT:
        return ((loc[0], loc[1] - 1), Flow.RIGHT)
    else:
        return (loc, Flow.ERROR)


def follow_top_down(loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
    if flow == Flow.TOP:
        return ((loc[0] + 1, loc[1]), Flow.TOP)
    elif flow == Flow.DOWN:
        return ((loc[0] - 1, loc[1]), Flow.DOWN)
    else:
        return (loc, Flow.ERROR)


def follow_right_top(loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
    if flow == Flow.RIGHT:
        return ((loc[0] - 1, loc[1]), Flow.DOWN)
    elif flow == Flow.TOP:
        return ((loc[0], loc[1] + 1), Flow.LEFT)
    else:
        return (loc, Flow.ERROR)


def follow_right_down(loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
    if flow == Flow.RIGHT:
        return ((loc[0] + 1, loc[1]), Flow.TOP)
    elif flow == Flow.DOWN:
        return ((loc[0], loc[1] + 1), Flow.LEFT)
    else:
        return (loc, Flow.ERROR)


def follow_left_top(loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
    if flow == Flow.LEFT:
        return ((loc[0] - 1, loc[1]), Flow.DOWN)
    elif flow == Flow.TOP:
        return ((loc[0], loc[1] - 1), Flow.RIGHT)
    else:
        return (loc, Flow.ERROR)


def follow_left_down(loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
    if flow == Flow.LEFT:
        return ((loc[0] + 1, loc[1]), Flow.TOP)
    elif flow == Flow.DOWN:
        return ((loc[0], loc[1] - 1), Flow.RIGHT)
    else:
        return (loc, Flow.ERROR)


def follow_no_passage(loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
    return (loc, Flow.ERROR)


follow_func = {
    "initial-left": follow_initial_left,
    "initial-right": follow_initial_right,
    "initial-top": follow_initial_top,
    "initial-down": follow_initial_down,
    "goal-left": follow_goal_left,
    "goal-right": follow_goal_right,
    "goal-top": follow_goal_top,
    "goal-down": follow_goal_down,
    "right-left-not": follow_right_left,
    "top-down-not": follow_top_down,
    "right-top-not": follow_right_top,
    "right-down-not": follow_right_down,
    "left-top-not": follow_left_top,
    "left-down-not": follow_left_down,
    "no-passage-not": follow_no_passage,
    "right-left": follow_right_left,
    "top-down": follow_top_down,
    "right-top": follow_right_top,
    "right-down": follow_right_down,
    "left-top": follow_left_top,
    "left-down": follow_left_down,
    "no-passage": follow_no_passage,
    "empty-cell": follow_no_passage,
}


class RTBProblem(search.Problem):
    def __init__(self):
        """
        Method that instantiate your class. You can change the content of this. self.initial is where
        the initial state of the puzzle should be saved.
        init initial state with empty tupple
        """
        super().__init__(())
        # self.initial = ()
        self.N = 0

    def load(self, fh):
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
                # row = [tile for tile in line.split(" ")]
                row = [tile for tile in line.split()]
                board += row

        self.initial = tuple(board)

    def isSolution(self):
        """returns 1 if the loaded puzzle is a solution, 0 otherwise."""
        board = self.initial
        print(board)

        def _find_init():
            """Locate the initial tile on the board, and set initial flow."""
            for idx, tile in enumerate(board):
                if tile in (
                    "initial-left",
                    "initial-right",
                    "initial-top",
                    "initial-down",
                ):
                    return (idx // self.N, idx % self.N)
            raise ValueError("did not find initial tile")

        # initial position, flow is not defined, can be any value
        current_loc, flow = _find_init(), Flow.DOWN

        print(current_loc, board[current_loc[0] * self.N + current_loc[1]])
        while True:
            current_loc, flow = follow_func[
                board[current_loc[0] * self.N + current_loc[1]]
            ](current_loc, flow)
            print(flow, current_loc, board[current_loc[0] * self.N + current_loc[1]])

            # tile is not compatible: broke the flow or flows outside
            if (
                flow == Flow.ERROR
                or current_loc[0] < 0
                or current_loc[0] >= self.N
                or current_loc[1] < 0
                or current_loc[1] >= self.N
            ):
                return 0

            # reached another initial tile, not solvable
            if board[current_loc[0] * self.N + current_loc[1]] in (
                "initial-left",
                "initial-right",
                "initial-top",
                "initial-down",
            ):
                return 0

            # found a goal tile, is it compatible?
            if board[current_loc[0] * self.N + current_loc[1]] in (
                "goal-top",
                "goal-down",
                "goal-left",
                "goal-right",
            ):
                # final flow test to check if goal tile is compatible
                current_loc, flow = follow_func[
                    board[current_loc[0] * self.N + current_loc[1]]
                ](current_loc, flow)
                if flow == Flow.ERROR:
                    return 0
                return 1
