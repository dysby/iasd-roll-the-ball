from typing import Tuple, List
from enum import Enum, auto

import search


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGTH = auto()


class Flow(Enum):
    """
    *Flow* is the direction of an imaginary ball arriving at the current tile,
    following a correct path from the initial tile.

    For example, if we are on a tile with a exit to the right, the flow will become left,
    because the next tile will see the ball coming from the left.
    """

    TOP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()
    ERROR = auto()


class Tile(Enum):
    INITIAL_LEFT = auto()
    INITIAL_RIGHT = auto()
    INITIAL_TOP = auto()
    INITIAL_DOWN = auto()
    GOAL_LEFT = auto()
    GOAL_RIGHT = auto()
    GOAL_TOP = auto()
    GOAL_DOWN = auto()
    RIGHT_LEFT_NOT = auto()
    TOP_DOWN_NOT = auto()
    RIGHT_TOP_NOT = auto()
    RIGHT_DOWN_NOT = auto()
    LEFT_TOP_NOT = auto()
    LEFT_DOWN_NOT = auto()
    NO_PASSAGE_NOT = auto()
    RIGHT_LEFT = auto()
    TOP_DOWN = auto()
    RIGHT_TOP = auto()
    RIGHT_DOWN = auto()
    LEFT_TOP = auto()
    LEFT_DOWN = auto()
    NO_PASSAGE = auto()
    EMPTY_CELL = auto()


map_tile_types = {
    "initial-left": Tile.INITIAL_LEFT,
    "initial-right": Tile.INITIAL_RIGHT,
    "initial-top": Tile.INITIAL_TOP,
    "initial-down": Tile.INITIAL_DOWN,
    "goal-left": Tile.GOAL_LEFT,
    "goal-right": Tile.GOAL_RIGHT,
    "goal-top": Tile.GOAL_TOP,
    "goal-down": Tile.GOAL_DOWN,
    "right-left-not": Tile.RIGHT_LEFT_NOT,
    "top-down-not": Tile.TOP_DOWN_NOT,
    "right-top-not": Tile.RIGHT_TOP_NOT,
    "right-down-not": Tile.RIGHT_DOWN_NOT,
    "left-top-not": Tile.LEFT_TOP_NOT,
    "left-down-not": Tile.LEFT_DOWN_NOT,
    "no-passage-not": Tile.NO_PASSAGE_NOT,
    "right-left": Tile.RIGHT_LEFT,
    "top-down": Tile.TOP_DOWN,
    "right-top": Tile.RIGHT_TOP,
    "right-down": Tile.RIGHT_DOWN,
    "left-top": Tile.LEFT_TOP,
    "left-down": Tile.LEFT_DOWN,
    "no-passage": Tile.NO_PASSAGE,
    "empty-cell": Tile.EMPTY_CELL,
}


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
    Tile.INITIAL_LEFT: follow_initial_left,
    Tile.INITIAL_RIGHT: follow_initial_right,
    Tile.INITIAL_TOP: follow_initial_top,
    Tile.INITIAL_DOWN: follow_initial_down,
    Tile.GOAL_LEFT: follow_goal_left,
    Tile.GOAL_RIGHT: follow_goal_right,
    Tile.GOAL_TOP: follow_goal_top,
    Tile.GOAL_DOWN: follow_goal_down,
    Tile.RIGHT_LEFT_NOT: follow_right_left,
    Tile.TOP_DOWN_NOT: follow_top_down,
    Tile.RIGHT_TOP_NOT: follow_right_top,
    Tile.RIGHT_DOWN_NOT: follow_right_down,
    Tile.LEFT_TOP_NOT: follow_left_top,
    Tile.LEFT_DOWN_NOT: follow_left_down,
    Tile.NO_PASSAGE_NOT: follow_no_passage,
    Tile.RIGHT_LEFT: follow_right_left,
    Tile.TOP_DOWN: follow_top_down,
    Tile.RIGHT_TOP: follow_right_top,
    Tile.RIGHT_DOWN: follow_right_down,
    Tile.LEFT_TOP: follow_left_top,
    Tile.LEFT_DOWN: follow_left_down,
    Tile.NO_PASSAGE: follow_no_passage,
    Tile.EMPTY_CELL: follow_no_passage,
}


initial_tile_types = {
    Tile.INITIAL_LEFT,
    Tile.INITIAL_RIGHT,
    Tile.INITIAL_TOP,
    Tile.INITIAL_DOWN,
}
goal_tile_types = {Tile.GOAL_LEFT, Tile.GOAL_RIGHT, Tile.GOAL_TOP, Tile.GOAL_DOWN}
# use | for set union and & for set intersection
unmovable_tile_types = (
    initial_tile_types
    | goal_tile_types
    | {
        Tile.RIGHT_LEFT_NOT,
        Tile.TOP_DOWN_NOT,
        Tile.RIGHT_TOP_NOT,
        Tile.RIGHT_DOWN_NOT,
        Tile.LEFT_TOP_NOT,
        Tile.LEFT_DOWN_NOT,
        Tile.NO_PASSAGE_NOT,
    }
)

# Typing Definitions
# State is a tuple of varying size of strings (tile names)
# Actions type is a tuple of varying size of Action
# Each Action is a tuple with ((y,x), direction), a tile (only empty-cell) position
# and a direction to move.
State = Tuple[Tile, ...]
Location = Tuple[int, int]
Action = Tuple[Location, Location]
Actions = Tuple[Action, ...]


class RTBProblem(search.Problem):
    def __init__(self):
        """
        Method that instantiate your class. You can change the content of this. self.initial is where
        the initial state of the puzzle should be saved.
        init initial state with empty tupple
        """
        self.initial: State = ()
        self.algorithm = None
        self.N = 0

    def load(self, fh):
        """Loads a RTB puzzle from the file object fh. You may initialize self.initial here."""
        board: List[Tile] = []

        for line in fh.read().splitlines():
            if line == "":
                # discard empty line
                continue
            elif line[0] in "0123456789":
                # line start with a digit, it must be the problem size definition line.
                self.N = int(line)
            elif line[0] == "#":
                # we don't care for comments
                continue
            else:
                # all other lines are, in sequence, corresponding to each board line configuration.
                row = [map_tile_types[tile] for tile in line.split()]
                board += row

        self.initial = tuple(board)

    def _loc_to_index(self, loc: Location) -> int:
        return int(self.N * loc[0] + loc[1])

    def _find_init(self, state) -> Location:
        """Locate the initial tile on the state, and set initial flow."""
        for idx, tile in enumerate(state):
            if tile in initial_tile_types:
                return (idx // self.N, idx % self.N)
        raise ValueError("did not find initial tile")

    def _in_bounds(self, loc: Location):
        if loc[0] < 0 or loc[0] >= self.N or loc[1] < 0 or loc[1] >= self.N:
            return False
        return True

    def result(self, state: State, action: Action) -> State:
        """Return the state that results from executing the given action in the given state."""
        loc_index = self._loc_to_index(action[0])  # to call only once
        loc_neighbor_index = self._loc_to_index(action[1])

        list_state = list(state)
        # Swapping element at index loc with element at index loc_neighbor
        list_state[loc_index], list_state[loc_neighbor_index] = (
            list_state[loc_neighbor_index],
            list_state[loc_index],
        )
        return tuple(list_state)

    def actions(self, state: State) -> Actions:
        """
        Return the actions that can be executed in the given state.
        """
        actions = []

        def _find_emptys() -> List[Location]:
            """
            return the locations of 'empty-cell' tiles in state

            >>> problem.initial
            ('right-down', 'right-left', 'right-left', 'initial-left', 'right-top', 'right-left', 'right-left', 'left-down', 'goal-right', 'right-left', 'right-left', 'left-top', 'empty-cell', 'empty-cell', 'empty-cell', 'empty-cell')
            >>> [idx for idx, tile in enumerate(problem.initial) if tile == "empty-cell"]
            [12, 13, 14, 15]
            """
            locs = [
                (idx // self.N, idx % self.N)
                for idx, tile in enumerate(state)
                if tile == Tile.EMPTY_CELL
            ]
            return locs

        def _valid_destination(candidate_loc):
            """test if the candidate location is inside bounds and the tile is not unmovable or another empty-cell"""
            # if not self._in_bounds(candidate_loc):
            if (
                candidate_loc[0] < 0
                or candidate_loc[0] >= self.N
                or candidate_loc[1] < 0
                or candidate_loc[1] >= self.N
            ):
                return False
            tile = state[candidate_loc[0] * self.N + candidate_loc[1]]
            if tile in unmovable_tile_types | {Tile.EMPTY_CELL}:
                return False
            return True

        empties = _find_emptys()
        for empty_loc in empties:
            #     Direction.UP:
            candidate_loc = empty_loc[0] - 1, empty_loc[1]
            if _valid_destination(candidate_loc):
                actions.append((empty_loc, candidate_loc))
            #     Direction.DOWN:
            candidate_loc = empty_loc[0] + 1, empty_loc[1]
            if _valid_destination(candidate_loc):
                actions.append((empty_loc, candidate_loc))
            #     Direction.LEFT:
            candidate_loc = empty_loc[0], empty_loc[1] - 1
            if _valid_destination(candidate_loc):
                actions.append((empty_loc, candidate_loc))
            #     Direction.RIGTH:
            candidate_loc = empty_loc[0], empty_loc[1] + 1
            if _valid_destination(candidate_loc):
                actions.append((empty_loc, candidate_loc))

        return tuple(actions)

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
            if flow == Flow.ERROR or not self._in_bounds(current_loc):
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
        #self.algorithm = search.iterative_deepening_search        # example : self.algorithm = search.breadth_first_tree_search
        self.algorithm = search.breadth_first_graph_search        # example : self.algorithm = search.breadth_first_tree_search
        # substitute by the function in search.py that
        # implements the chosen algorithm.
        # You can only use the algorithms defined in search.py

    def solve(self):
        """Calls the uninformed search algorithm chosen."""
        solution = self.algorithm(self)
        # self.final = solution.state
        return solution
        # You have to provide the arguments for the
        # chosen algorithm if any.
        # For instance , for the Depth Limited Search you need to
        # provide a value for the limit L, otherwise the default
        # value (50) will be used.
