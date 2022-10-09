from typing import Tuple
from enum import Enum, auto

import search


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGTH = auto()

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

class Tile(Enum):
    INITIAL_LEFT = "initial-left"
    INITIAL_RIGHT = "initial-right"
    INITIAL_TOP = "initial-top"
    INITIAL_DOWN = "initial-down"
    GOAL_LEFT = "goal-left"
    GOAL_RIGHT = ""
    GOAL_TOP = "goal-top"
    GOAL_DOWN = "goal-down"
    RIGHT_LEFT_NOT = "right-left-not"
    TOP_DOWN_NOT = "top-down-not"
    RIGHT_TOP_NOT = "right-top-not"
    RIGHT_DOWN_NOT = "right-down-not"
    LEFT_TOP_NOT = "left-top-not"
    LEFT_DOWN_NOT = "left-down-not"
    NO_PASSAGE_NOT = "no-passage-not"
    RIGHT_LEFT = "right-left"
    TOP_DOWN = "top-down"
    RIGHT_TOP = "right-top"
    RIGHT_DOWN = "right-down"
    LEFT_TOP = "left-top"
    LEFT_DOWN = "left-down"
    NO_PASSAGE = "no-passage"
    EMPTY_CELL = "empty-cell"




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

initial_tile_types = {"initial-left", "initial-right", "initial-top", "initial-down"}
goal_tile_types = {"goal-left", "goal-right", "goal-top", "goal-down"}
# use | for set union and & for set intersection
unmovable_tile_types = (
    initial_tile_types
    | goal_tile_types
    | {
        "right-left-not",
        "top-down-not",
        "right-top-not",
        "right-down-not",
        "left-top-not",
        "left-down-not",
        "no-passage-not",
    }
)


compatible_tiles = {
    "initial-left": [
        "right-top",
        "right-top-not",
        "right-down",
        "right-down-not",
        "right-left",
        "right-left-not",
    ],
    "initial-right": [
        "left-top",
        "left-top-not",
        "left-down",
        "left-down-not",
        "right-left",
        "right-left-not",
    ],
    "initial-top": [],
    "initial-down": [],
    "goal-left": [],
    "goal-right": [],
    "goal-top": [],
    "goal-down": [],
    "right-left-not": [],
    "top-down-not": [],
    "right-top-not": [],
    "right-down-not": [],
    "left-top-not": [],
    "left-down-not": [],
    "no-passage-not": [],
    "right-left": [],
    "top-down": [],
    "right-top": [],
    "right-down": [],
    "left-top": [],
    "left-down": [],
    "no-passage": [],
    "empty-cell": [],
}


class RTBProblem(search.Problem):
    def __init__(self):
        """
        Method that instantiate your class. You can change the content of this. self.initial is where
        the initial state of the puzzle should be saved.
        init initial state with empty tupple
        """
        self.initial = None
        self.algorithm = None
        self.N = 0

    def load(self, fh):
        """Loads a RTB puzzle from the file object fh. You may initialize self.initial here."""
        board = []

        for line in fh.read().splitlines():
            if line[0] == "#":
                # we don't care for comments
                continue
            elif line[0] in "0123456789":
                # line start with a digit, it must be the problem size definition line.
                self.N = int(line)
            elif line == "":
                # discard empty line
                continue
            else:
                # all other lines are, in sequence, corresponding to each board line configuration.
                row = [tile for tile in line.split()]
                board += row

        self.initial = tuple(board)

    def isSolution(self):
        """returns 1 if the loaded puzzle is a solution, 0 otherwise."""
        board = self.initial
        # hack for pub10
        if self.N == 0 and len(board) > 0:
            self.N = int(len(board) ** 0.5)

        def _find_init():
            """Locate the initial tile on the board, and set initial flow."""
            for idx, tile in enumerate(board):
                if tile in initial_tile_types:
                    return (idx // self.N, idx % self.N)
            raise ValueError("did not find initial tile")

        # initial position, flow will not be defined, can be any value
        current_loc, flow = _find_init(), Flow.DOWN

        # print(current_loc, board)
        while True:
            current_loc, flow = follow_func[
                board[current_loc[0] * self.N + current_loc[1]]
            ](current_loc, flow)
            # print(flow, current_loc, board[current_loc[0] * self.N + current_loc[1]])

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
            if board[current_loc[0] * self.N + current_loc[1]] in initial_tile_types:
                return 0

            # found a goal tile, is it compatible?
            if board[current_loc[0] * self.N + current_loc[1]] in goal_tile_types:
                # final flow test to check if goal tile is compatible
                current_loc, flow = follow_func[
                    board[current_loc[0] * self.N + current_loc[1]]
                ](current_loc, flow)
                if flow == Flow.ERROR:
                    return 0
                return 1

    def result(self, state, action):
        """Return the state that results from executing the given action in the given state."""
        pass

    def actions(self, state):
        """Return the actions that can be executed in the given state."""
        pass

    def _find_init(self, state) -> Tuple[int, int]:
            """Locate the initial tile on the state, and set initial flow."""
            for idx, tile in enumerate(state):
                if tile in initial_tile_types:
                    return (idx // self.N, idx % self.N)
            raise ValueError("did not find initial tile")

    def goal_test(self, state) -> bool:
        """Return True if the state is a goal."""
        if self.N == 0 and len(state) > 0:
            self.N = int(len(state) ** 0.5)

        # initial position, flow will not be defined, can be any value
        current_loc, flow = self._find_init(state), Flow.DOWN

        # print(current_loc, state)
        while True:
            current_loc, flow = follow_func[
                state[current_loc[0] * self.N + current_loc[1]]
            ](current_loc, flow)
            # print(flow, current_loc, state[current_loc[0] * self.N + current_loc[1]])

            # tile is not compatible: broke the flow or flows outside
            if (
                flow == Flow.ERROR
                or current_loc[0] < 0
                or current_loc[0] >= self.N
                or current_loc[1] < 0
                or current_loc[1] >= self.N
            ):
                return False

            # reached another initial tile, not solvable
            if state[current_loc[0] * self.N + current_loc[1]] in initial_tile_types:
                return False

            # found a goal tile, is it compatible?
            if state[current_loc[0] * self.N + current_loc[1]] in goal_tile_types:
                # final flow test to check if goal tile is compatible
                current_loc, flow = follow_func[
                    state[current_loc[0] * self.N + current_loc[1]]
                ](current_loc, flow)
                if flow == Flow.ERROR:
                    return False
                return True

    def setAlgorithm(self):
        """Sets the uninformed search algorithm chosen."""
        self.algorithm = search.breadth_first_tree_search
        # example : self.algorithm = search.breadth_first_tree_search
        # substitute by the function in search.py that
        # implements the chosen algorithm.
        # You can only use the algorithms defined in search.py

    def solve(self):
        """Calls the uninformed search algorithm chosen."""
        return self.algorithm(self, ...)
        # You have to provide the arguments for the
        # chosen algorithm if any.
        # For instance , for the Depth Limited Search you need to
        # provide a value for the limit L, otherwise the default
        # value (50) will be used.
