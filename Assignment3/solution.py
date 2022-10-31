from typing import Tuple, List
from enum import Enum, auto
import search


class Flow(Enum):
    """
    *Flow* is the direction of an imaginary ball arriving at the current tile, following a correct path from the initial
    tile.

    For example, if we are on a tile with an exit to the right, the flow will become left, because the next tile will
    see the ball coming from the left.
    """

    TOP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()
    ERROR = auto()


map_tile_to_bytes = {
    "initial-left": b"00000",
    "initial-right": b"00001",
    "initial-top": b"00010",
    "initial-down": b"00011",
    "goal-left": b"00100",
    "goal-right": b"00101",
    "goal-top": b"00110",
    "goal-down": b"00111",
    "right-left-not": b"01000",
    "top-down-not": b"01001",
    "right-top-not": b"01010",
    "right-down-not": b"01011",
    "left-top-not": b"01100",
    "left-down-not": b"01101",
    "no-passage-not": b"01110",
    "right-left": b"01111",
    "top-down": b"10000",
    "right-top": b"10001",
    "right-down": b"10010",
    "left-top": b"10011",
    "left-down": b"10100",
    "no-passage": b"10101",
    "empty-cell": b"10110",
}

initial_tile_types = {
    b"00000",
    b"00001",
    b"00010",
    b"00011",
}

goal_tile_types = {b"00100", b"00101", b"00110", b"00111"}

# use | for set union and & for set intersection
unmovable_tile_types = (
    initial_tile_types
    | goal_tile_types
    | {
        b"01000",
        b"01001",
        b"01010",
        b"01011",
        b"01100",
        b"01101",
        b"01110",
    }
)

# Typing Definitions
# TODO OUTDATED
# State is a tuple of varying size of strings (tile names)
# Actions type is a tuple of varying size of Action
# Each Action is a tuple with ((y,x), direction), a tile (only empty-cell) position
# and a direction to move.
State = bytes
Location = Tuple[int, int]
Action = Tuple[Location, Location]
Actions = Tuple[Action, ...]


class RTBProblem(search.Problem):
    def __init__(self):
        """
        State is a 1d binary object with N*N*TILE_ENCODING length.

        There's 23 different types of tiles, so we need at least 5 bits
        to encode all of each tile types.

        A location object (y, x) is used, where (0,0) is the top left
        corner of the grid, and (N-1, N-1) is the lower right corner.

        We use integer division and module arithmetic's to translate
        (y,x) coordinates to 1 dimension index in the state
        representation.
        """
        self.initial: State = b""
        self.algorithm = None
        self.N = 0
        self.init_tile_loc = (0, 0)
        self.goal_tile_loc = (0, 0)
        self.init_goal_dist = 0

    def load(self, fh):
        """Loads an RTB puzzle from the file object fh. You may initialize self.initial here."""
        board: bytes = b""

        for line in fh.read().splitlines():
            if line == "":
                # discards empty line
                continue
            elif line[0] in "0123456789":
                # line starts with a digit, it must be the problem size definition line.
                self.N = int(line)
            elif line[0] == "#":
                # discards any comment lines
                continue
            else:
                # all other lines correspond sequentially to each board line configuration.
                row = [map_tile_to_bytes[tile] for tile in line.split()]
                board = b"".join([board, *row])

        self.initial = board
        self.init_tile_loc = self._find_init(self.initial)
        self.goal_tile_loc = self._find_goal(self.initial)
        # useful for heuristic function
        self.init_goal_dist = abs(self.goal_tile_loc[1] - self.init_tile_loc[1]) + abs(
            self.goal_tile_loc[0] - self.init_tile_loc[0]
        )

    def _loc_to_index(self, loc: Location) -> int:
        return int(self.N * loc[0] + loc[1])

    def _find_init(self, state) -> Location:
        """Locate the initial tile in the state."""
        for n in range(self.N * self.N):
            if state[n * 5 : n * 5 + 5] in initial_tile_types:
                return n // self.N, n % self.N
        raise ValueError("did not find initial tile")

    def _find_goal(self, state) -> Location:
        """Locate the goal tile in the state."""
        for n in range(self.N * self.N):
            if state[n * 5 : n * 5 + 5] in goal_tile_types:
                return n // self.N, n % self.N
        raise ValueError("did not find goal tile")

    def _in_bounds(self, loc: Location):
        if loc[0] < 0 or loc[0] >= self.N or loc[1] < 0 or loc[1] >= self.N:
            return False
        return True

    def result(self, state: State, action: Action) -> State:
        """Return the state that results from executing the given action in the given state."""
        loc_index = int(self.N * action[0][0] + action[0][1])  # to call only once
        loc_neighbor_index = int(
            self.N * action[1][0] + action[1][1]
        )  # self._loc_to_index(action[1])

        state_list = list(state)

        # swap elements in a list
        (
            state_list[loc_index * 5 : loc_index * 5 + 5],
            state_list[loc_neighbor_index * 5 : loc_neighbor_index * 5 + 5],
        ) = (
            state_list[loc_neighbor_index * 5 : loc_neighbor_index * 5 + 5],
            state_list[loc_index * 5 : loc_index * 5 + 5],
        )
        # transform list back to binary representation.
        return bytes(state_list)

    def actions(self, state: State) -> Actions:
        """
        Return the actions that can be executed in the given state.
        """
        actions = []
        # state_list = self._state_to_list(state)

        def _find_empties() -> List[Location]:
            """
            return the locations of 'empty-cell' (b"10110") tiles in state
            """
            locs = []

            for n in range(self.N * self.N):
                t = state[n * 5 : n * 5 + 5]
                if t == b"10110":
                    locs.append((n // self.N, n % self.N))

            return locs

        def _valid_destination(candidate_loc):
            """
            test if the candidate location is inside bounds and
            the tile is not unmovable or another empty-cell
            """
            if (
                candidate_loc[0] < 0
                or candidate_loc[0] >= self.N
                or candidate_loc[1] < 0
                or candidate_loc[1] >= self.N
            ):
                return False
            tile = state[
                (candidate_loc[0] * self.N + candidate_loc[1])
                * 5 : (candidate_loc[0] * self.N + candidate_loc[1])
                * 5
                + 5
            ]
            if tile in unmovable_tile_types | {b"10110"}:
                return False
            return True

        empties = _find_empties()
        for empty_loc in empties:
            # Direction UP
            candidate_loc = empty_loc[0] - 1, empty_loc[1]
            if _valid_destination(candidate_loc):
                actions.append((empty_loc, candidate_loc))
            # Direction DOWN
            candidate_loc = empty_loc[0] + 1, empty_loc[1]
            if _valid_destination(candidate_loc):
                actions.append((empty_loc, candidate_loc))
            # Direction LEFT
            candidate_loc = empty_loc[0], empty_loc[1] - 1
            if _valid_destination(candidate_loc):
                actions.append((empty_loc, candidate_loc))
            # Direction RIGHT
            candidate_loc = empty_loc[0], empty_loc[1] + 1
            if _valid_destination(candidate_loc):
                actions.append((empty_loc, candidate_loc))

        return tuple(actions)

    def goal_test(self, state) -> bool:
        """Return True if the state is a goal."""
        # initial position, flow will not be defined, can be any value
        loc, flow = self.init_tile_loc, Flow.DOWN
        # set first tile type, one of initial types
        tile = state[
            (loc[0] * self.N + loc[1]) * 5 : (loc[0] * self.N + loc[1]) * 5 + 5
        ]

        first = (
            True  # flag to check first passage in initial type tile to prevent loops
        )
        while True:
            if (
                tile == b"01110" or tile == b"10101" or tile == b"10110"
            ):  # follow_no_passage,
                return False
            elif tile == b"00000":  # follow_initial_left
                if first:
                    loc, flow = ((loc[0], loc[1] - 1), Flow.RIGHT)
                else:
                    return False
            elif tile == b"00001":  # follow_initial_right
                if first:
                    loc, flow = ((loc[0], loc[1] + 1), Flow.LEFT)
                else:
                    return False
            elif tile == b"00010":  # follow_initial_top
                if first:
                    loc, flow = ((loc[0] - 1, loc[1]), Flow.DOWN)
                else:
                    return False
            elif tile == b"00011":  # follow_initial_down
                if first:
                    loc, flow = ((loc[0] + 1, loc[1]), Flow.TOP)
                else:
                    return False
            elif tile == b"00100":  # follow_goal_left
                if flow == Flow.LEFT:
                    return True
                return False
            elif tile == b"00101":  # follow_goal_right
                if flow == Flow.RIGHT:
                    return True
                return False
            elif tile == b"00110":  # follow_goal_top
                if flow == Flow.TOP:
                    return True
                return False
            elif tile == b"00111":  # follow_goal_down
                if flow == Flow.DOWN:
                    return True
                return False
            elif tile == b"01000" or tile == b"01111":  # follow_right_left
                if flow == Flow.LEFT:
                    loc = (loc[0], loc[1] + 1)
                elif flow == Flow.RIGHT:
                    loc = (loc[0], loc[1] - 1)
                else:
                    return False
            elif tile == b"01001" or tile == b"10000":  # follow_top_down
                if flow == Flow.TOP:
                    loc = (loc[0] + 1, loc[1])
                elif flow == Flow.DOWN:
                    loc = (loc[0] - 1, loc[1])
                else:
                    return False
            elif tile == b"01010" or tile == b"10001":  # follow_right_top
                if flow == Flow.RIGHT:
                    loc, flow = ((loc[0] - 1, loc[1]), Flow.DOWN)
                elif flow == Flow.TOP:
                    loc, flow = ((loc[0], loc[1] + 1), Flow.LEFT)
                else:
                    return False
            elif tile == b"01011" or tile == b"10010":  # follow_right_down
                if flow == Flow.RIGHT:
                    loc, flow = ((loc[0] + 1, loc[1]), Flow.TOP)
                elif flow == Flow.DOWN:
                    loc, flow = ((loc[0], loc[1] + 1), Flow.LEFT)
                else:
                    return False
            elif tile == b"01100" or tile == b"10011":  # follow_left_top
                if flow == Flow.LEFT:
                    loc, flow = ((loc[0] - 1, loc[1]), Flow.DOWN)
                elif flow == Flow.TOP:
                    loc, flow = ((loc[0], loc[1] - 1), Flow.RIGHT)
                else:
                    return False
            elif tile == b"01101" or tile == b"10100":  # follow_left_down
                if flow == Flow.LEFT:
                    loc, flow = ((loc[0] + 1, loc[1]), Flow.TOP)
                elif flow == Flow.DOWN:
                    loc, flow = ((loc[0], loc[1] - 1), Flow.RIGHT)
                else:
                    return False
            else:
                raise ValueError("did not find tile type")

            first = False
            # validate new_loc
            if loc[0] < 0 or loc[0] >= self.N or loc[1] < 0 or loc[1] >= self.N:
                return False
            # get tile at new position
            tile = state[
                (loc[0] * self.N + loc[1]) * 5 : (loc[0] * self.N + loc[1]) * 5 + 5
            ]
            # continue

    def _follow_path_forward(self, state) -> Location:  # ???
        """
        Return the location of the last square the path can
        flow to.

        Follows the ball flow and if it detects a break returns
        the last valid position (not the current invalid one).
        """
        # initial position, flow will not be defined, can be any value
        loc, flow = self.init_tile_loc, Flow.DOWN
        # set first tile type, one of initial types
        tile = state[
            (loc[0] * self.N + loc[1]) * 5 : (loc[0] * self.N + loc[1]) * 5 + 5
        ]

        first = (
            True  # flag to check first passage in initial type tile to prevent loops
        )
        last = loc
        last_temp = loc
        while True:
            if (
                tile == b"01110" or tile == b"10101" or tile == b"10110"
            ):  # follow_no_passage,
                return last
            elif tile == b"00000":  # follow_initial_left
                if first:
                    last_temp = loc
                    loc, flow = ((loc[0], loc[1] - 1), Flow.RIGHT)
                else:
                    return last
            elif tile == b"00001":  # follow_initial_right
                if first:
                    last_temp = loc
                    loc, flow = ((loc[0], loc[1] + 1), Flow.LEFT)
                else:
                    return last
            elif tile == b"00010":  # follow_initial_top
                if first:
                    last_temp = loc
                    loc, flow = ((loc[0] - 1, loc[1]), Flow.DOWN)
                else:
                    return last
            elif tile == b"00011":  # follow_initial_down
                if first:
                    last_temp = loc
                    loc, flow = ((loc[0] + 1, loc[1]), Flow.TOP)
                else:
                    return last
            elif tile == b"00100":  # follow_goal_left
                if flow == Flow.LEFT:
                    return loc
                return last
            elif tile == b"00101":  # follow_goal_right
                if flow == Flow.RIGHT:
                    return loc
                return last
            elif tile == b"00110":  # follow_goal_top
                if flow == Flow.TOP:
                    return loc
                return last
            elif tile == b"00111":  # follow_goal_down
                if flow == Flow.DOWN:
                    return loc
                return last
            elif tile == b"01000" or tile == b"01111":  # follow_right_left
                if flow == Flow.LEFT:
                    last_temp = loc
                    loc = (loc[0], loc[1] + 1)
                elif flow == Flow.RIGHT:
                    last_temp = loc
                    loc = (loc[0], loc[1] - 1)
                else:
                    return last
            elif tile == b"01001" or tile == b"10000":  # follow_top_down
                if flow == Flow.TOP:
                    last_temp = loc
                    loc = (loc[0] + 1, loc[1])
                elif flow == Flow.DOWN:
                    last_temp = loc
                    loc = (loc[0] - 1, loc[1])
                else:
                    return last
            elif tile == b"01010" or tile == b"10001":  # follow_right_top
                if flow == Flow.RIGHT:
                    last_temp = loc
                    loc, flow = ((loc[0] - 1, loc[1]), Flow.DOWN)
                elif flow == Flow.TOP:
                    last_temp = loc
                    loc, flow = ((loc[0], loc[1] + 1), Flow.LEFT)
                else:
                    return last
            elif tile == b"01011" or tile == b"10010":  # follow_right_down
                if flow == Flow.RIGHT:
                    last_temp = loc
                    loc, flow = ((loc[0] + 1, loc[1]), Flow.TOP)
                elif flow == Flow.DOWN:
                    last_temp = loc
                    loc, flow = ((loc[0], loc[1] + 1), Flow.LEFT)
                else:
                    return last
            elif tile == b"01100" or tile == b"10011":  # follow_left_top
                if flow == Flow.LEFT:
                    last_temp = loc
                    loc, flow = ((loc[0] - 1, loc[1]), Flow.DOWN)
                elif flow == Flow.TOP:
                    last_temp = loc
                    loc, flow = ((loc[0], loc[1] - 1), Flow.RIGHT)
                else:
                    return last
            elif tile == b"01101" or tile == b"10100":  # follow_left_down
                if flow == Flow.LEFT:
                    last_temp = loc
                    loc, flow = ((loc[0] + 1, loc[1]), Flow.TOP)
                elif flow == Flow.DOWN:
                    last_temp = loc
                    loc, flow = ((loc[0], loc[1] - 1), Flow.RIGHT)
                else:
                    return last
            else:
                raise ValueError("did not find tile type")

            first = False
            # validate new_loc
            if loc[0] < 0 or loc[0] >= self.N or loc[1] < 0 or loc[1] >= self.N:
                return last
            # get tile at new position
            last = last_temp
            tile = state[
                (loc[0] * self.N + loc[1]) * 5 : (loc[0] * self.N + loc[1]) * 5 + 5
            ]

    def _follow_path_backward(self, state) -> Location:
        """
        Follows the ball flow from goal tile in the direction to
        initial tile and if it detects a break returns the
        last valid position (not the current invalid).

        Return the location of the last square the path can
        flow to.

        We use last, last_temp because at each tile transversal we
        can go to a outside invalid location.
        """
        # initial position, flow will not be defined, can be any value
        loc, flow = self.goal_tile_loc, Flow.DOWN
        # set first tile type, one of goal types
        tile = state[
            (loc[0] * self.N + loc[1]) * 5 : (loc[0] * self.N + loc[1]) * 5 + 5
        ]

        first = True  # flag to check first passage in goal type tile to prevent loops
        last = loc
        last_temp = loc
        while True:
            if (
                tile == b"01110" or tile == b"10101" or tile == b"10110"
            ):  # follow_no_passage,
                return last
            elif tile == b"00000":  # follow_initial_left
                if flow == Flow.LEFT:
                    return loc
                return last
            elif tile == b"00001":  # follow_initial_right
                if flow == Flow.RIGHT:
                    return loc
                return last
            elif tile == b"00010":  # follow_initial_top
                if flow == Flow.TOP:
                    return loc
                return last
            elif tile == b"00011":  # follow_initial_down
                if flow == Flow.DOWN:
                    return loc
                return last
            elif tile == b"00100":  # follow_goal_left
                if first:
                    last_temp = loc
                    loc, flow = ((loc[0], loc[1] - 1), Flow.RIGHT)
                else:
                    return last
            elif tile == b"00101":  # follow_goal_right
                if first:
                    last_temp = loc
                    loc, flow = ((loc[0], loc[1] + 1), Flow.LEFT)
                else:
                    return last
            elif tile == b"00110":  # follow_goal_top
                if first:
                    last_temp = loc
                    loc, flow = ((loc[0] - 1, loc[1]), Flow.DOWN)
                else:
                    return last
            elif tile == b"00111":  # follow_goal_down
                if first:
                    last_temp = loc
                    loc, flow = ((loc[0] + 1, loc[1]), Flow.TOP)
                else:
                    return last
            elif tile == b"01000" or tile == b"01111":  # follow_right_left
                if flow == Flow.LEFT:
                    last_temp = loc
                    loc = (loc[0], loc[1] + 1)
                elif flow == Flow.RIGHT:
                    last_temp = loc
                    loc = (loc[0], loc[1] - 1)
                else:
                    return last
            elif tile == b"01001" or tile == b"10000":  # follow_top_down
                if flow == Flow.TOP:
                    last_temp = loc
                    loc = (loc[0] + 1, loc[1])
                elif flow == Flow.DOWN:
                    last_temp = loc
                    loc = (loc[0] - 1, loc[1])
                else:
                    return last
            elif tile == b"01010" or tile == b"10001":  # follow_right_top
                if flow == Flow.RIGHT:
                    last_temp = loc
                    loc, flow = ((loc[0] - 1, loc[1]), Flow.DOWN)
                elif flow == Flow.TOP:
                    last_temp = loc
                    loc, flow = ((loc[0], loc[1] + 1), Flow.LEFT)
                else:
                    return last
            elif tile == b"01011" or tile == b"10010":  # follow_right_down
                if flow == Flow.RIGHT:
                    last_temp = loc
                    loc, flow = ((loc[0] + 1, loc[1]), Flow.TOP)
                elif flow == Flow.DOWN:
                    last_temp = loc
                    loc, flow = ((loc[0], loc[1] + 1), Flow.LEFT)
                else:
                    return last
            elif tile == b"01100" or tile == b"10011":  # follow_left_top
                if flow == Flow.LEFT:
                    last_temp = loc
                    loc, flow = ((loc[0] - 1, loc[1]), Flow.DOWN)
                elif flow == Flow.TOP:
                    last_temp = loc
                    loc, flow = ((loc[0], loc[1] - 1), Flow.RIGHT)
                else:
                    return last
            elif tile == b"01101" or tile == b"10100":  # follow_left_down
                if flow == Flow.LEFT:
                    last_temp = loc
                    loc, flow = ((loc[0] + 1, loc[1]), Flow.TOP)
                elif flow == Flow.DOWN:
                    last_temp = loc
                    loc, flow = ((loc[0], loc[1] - 1), Flow.RIGHT)
                else:
                    return last
            else:
                raise ValueError("did not find tile type")

            first = False
            # validate new_loc
            if loc[0] < 0 or loc[0] >= self.N or loc[1] < 0 or loc[1] >= self.N:
                return last
            # get tile at new position
            # last test (outside) is valid so we can assign last location to memory.
            last = last_temp
            tile = state[
                (loc[0] * self.N + loc[1]) * 5 : (loc[0] * self.N + loc[1]) * 5 + 5
            ]

    def h(self, node):
        """This heuristic works like this:
        ...
        It is consistent/not consistent because...
        It is admissible/not admissible because...
        """
        # node.state tem o estado
        loc_flow_init = self._follow_path_forward(node.state)
        loc_flow_goal = self._follow_path_backward(node.state)
        # loc_flow_end = calc_end_flow_from_goal

        # Manhattan distance = abs(x2-x1) + abs(y2-y1)
        d1 = abs(loc_flow_goal[1] - loc_flow_init[1]) + abs(
            loc_flow_goal[0] - loc_flow_init[0]
        )
        d2 = abs(loc_flow_goal[1] - self.init_tile_loc[1]) + abs(
            loc_flow_goal[0] - self.init_tile_loc[0]
        )
        d3 = abs(self.goal_tile_loc[1] - loc_flow_init[1]) + abs(
            self.goal_tile_loc[0] - loc_flow_init[0]
        )
        return min(d1, d2, d3, self.init_goal_dist)
        # min_dist(init, flow_init, flow_goal, goal)
