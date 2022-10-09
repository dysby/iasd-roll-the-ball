from enum import Enum, auto
from typing import Tuple

class Flow(Enum):
    TOP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()
    ERROR = auto()

class Tile:
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        return (loc, Flow.ERROR)

class InitialTypeTile(Tile):
    pass

class InitialLeft(InitialTypeTile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        return ((loc[0], loc[1] - 1), Flow.RIGHT)
    def __str__(self):
        return "initial-left"


class InitialRight(InitialTypeTile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        return ((loc[0], loc[1] + 1), Flow.LEFT)
    def __str__(self):
        return "initial-right"


class InitialTop(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        return ((loc[0] + 1, loc[1] ), Flow.DOWN)
    def __str__(self):
        return "initial-top"


class InitialDown(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        return ((loc[0] - 1, loc[1] ), Flow.TOP)
    def __str__(self):
        return "initial-down"


class GoalLeft(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.LEFT:
            return (loc, flow)
        return (loc, Flow.ERROR)
    def __str__(self):
        return "goal-left"


class GoalRight(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.RIGHT:
            return (loc, flow)
        return (loc, Flow.ERROR)
    def __str__(self):
        return "goal-right"


class GoalTop(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.TOP:
            return (loc, flow)
        return (loc, Flow.ERROR)
    def __str__(self):
        return "goal-top"


class GoalDown(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.DOWN:
            return (loc, flow)
        return (loc, Flow.ERROR)
    def __str__(self):
        return "goal-down"


class RightLeft(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.LEFT:
            return ((loc[0], loc[1] + 1), Flow.LEFT)
        elif flow == Flow.RIGHT:
            return ((loc[0], loc[1] - 1), Flow.RIGHT)
        else:
            return (loc, Flow.ERROR)
    def __str__(self):
        return "right-left"


class TopDown(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.TOP:
            return ((loc[0] - 1, loc[1]), Flow.TOP)
        elif flow == Flow.DOWN:
            return ((loc[0] + 1, loc[1] + 1), Flow.DOWN)
        else:
            return (loc, Flow.ERROR)
    def __str__(self):
        return "top-down"


class RightTop(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.RIGHT:
            return ((loc[0] - 1, loc[1]), Flow.DOWN)
        elif flow == Flow.TOP:
            return ((loc[0], loc[1] + 1), Flow.LEFT)
        else:
            return (loc, Flow.ERROR)
    def __str__(self):
        return "right-top"


class RightDown(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.RIGHT:
            return ((loc[0] + 1, loc[1]), Flow.TOP)
        elif flow == Flow.DOWN:
            return ((loc[0], loc[1] + 1), Flow.LEFT)
        else:
            return (loc, Flow.ERROR)
    def __str__(self):
        return "right-down"


class LeftTop(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.LEFT:
            return ((loc[0] - 1, loc[1]), Flow.DOWN)
        elif flow == Flow.TOP:
            return ((loc[0], loc[1] - 1), Flow.RIGHT)
        else:
            return (loc, Flow.ERROR)

    def __str__(self):
        return "left-top"
class LeftDown(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.LEFT:
            return ((loc[0] + 1, loc[1]), Flow.TOP)
        elif flow == Flow.DOWN:
            return ((loc[0], loc[1] - 1), Flow.RIGHT)
        else:
            return (loc, Flow.ERROR)

    def __str__(self):
        return "left-down"

class NoPassage(Tile):
    def __str__(self):
        return "no-passage"

class Empty(Tile):
    def __str__(self):
        return "empty-cell"

class RightLeftNot(RightLeft):
    def __str__(self):
        return "right-left-not"

class TopDownNot(TopDown):
    def __str__(self):
        return "top-down-not"

class RightTopNot(RightTop):
    def __str__(self):
        return "right-top-not"


class RightDownNot(RightDown):
    def __str__(self):
        return "right-down-not"

class LeftTopNot(LeftTop):
    def __str__(self):
        return "left-top-not"


class LeftDownNot(LeftDown):
    def __str__(self):
        return "left-down-not"
    


class NoPassageNot(NoPassage):
    def __str__(self):
        return "no-passage-not"


def tile_factory(name: str = "empty-cell") -> Tile:
    """Factory Method - return a new instance of class associated with name sting
    """
    tile_types = {
        "initial-left": InitialLeft,
        "initial-right": InitialRight,
        "initial-top": InitialTop,
        "initial-down": InitialDown,
        "goal-left": GoalLeft,
        "goal-right": GoalRight,
        "goal-top": GoalTop,
        "goal-down": GoalDown,
        "right-left-not": RightLeftNot,
        "top-down-not": TopDownNot,
        "right-top-not": RightTopNot,
        "right-down-not": RightDownNot,
        "left-top-not": LeftTopNot,
        "left-down-not": LeftDownNot,
        "no-passage-not": NoPassageNot,
        "right-left": RightLeft,
        "top-down": TopDown,
        "right-top": RightTop,
        "right-down": RightDown,
        "left-top": LeftTop,
        "left-down": LeftDown,
        "no-passage": NoPassage,
        "empty-cell": Empty,
    }
    if name not in tile_types.keys():
        raise ValueError

    return tile_types[name]()


