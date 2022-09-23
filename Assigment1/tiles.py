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


class InitialRight(InitialTypeTile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        return ((loc[0], loc[1] + 1), Flow.LEFT)


class InitialTop(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        return ((loc[0] + 1, loc[1] ), Flow.DOWN)


class InitialDown(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        return ((loc[0] - 1, loc[1] ), Flow.TOP)


class GoalLeft(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.LEFT:
            return (loc, flow)
        return (loc, Flow.ERROR)


class GoalRight(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.RIGHT:
            return (loc, flow)
        return (loc, Flow.ERROR)


class GoalTop(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.TOP:
            return (loc, flow)
        return (loc, Flow.ERROR)


class GoalDown(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.DOWN:
            return (loc, flow)
        return (loc, Flow.ERROR)


class RightLeft(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.LEFT:
            return ((loc[0], loc[1] + 1), Flow.LEFT)
        elif flow == Flow.RIGHT:
            return ((loc[0], loc[1] - 1), Flow.RIGHT)
        else:
            return (loc, Flow.ERROR)


class TopDown(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.TOP:
            return ((loc[0] - 1, loc[1]), Flow.TOP)
        elif flow == Flow.DOWN:
            return ((loc[0] + 1, loc[1] + 1), Flow.DOWN)
        else:
            return (loc, Flow.ERROR)


class RightTop(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.RIGHT:
            return ((loc[0] - 1, loc[1]), Flow.DOWN)
        elif flow == Flow.TOP:
            return ((loc[0], loc[1] + 1), Flow.LEFT)
        else:
            return (loc, Flow.ERROR)


class RightDown(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.RIGHT:
            return ((loc[0] + 1, loc[1]), Flow.TOP)
        elif flow == Flow.DOWN:
            return ((loc[0], loc[1] + 1), Flow.LEFT)
        else:
            return (loc, Flow.ERROR)


class LeftTop(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.LEFT:
            return ((loc[0] - 1, loc[1]), Flow.DOWN)
        elif flow == Flow.TOP:
            return ((loc[0], loc[1] - 1), Flow.RIGHT)
        else:
            return (loc, Flow.ERROR)

class LeftDown(Tile):
    def follow(self, loc: Tuple[int, int], flow: Flow) -> Tuple[Tuple[int, int], Flow]:
        if flow == Flow.LEFT:
            return ((loc[0] + 1, loc[1]), Flow.TOP)
        elif flow == Flow.DOWN:
            return ((loc[0], loc[1] - 1), Flow.RIGHT)
        else:
            return (loc, Flow.ERROR)

class NoPassage(Tile):
    pass

class Empty(Tile):
    pass

class RightLeftNot(RightLeft):
    pass

class TopDownNot(TopDown):
    pass

class RightTopNot(RightTop):
    pass


class RightDownNot(RightDown):
    pass

class LeftTopNot(LeftTop):
    pass


class LeftDownNot(LeftDown):
    pass


class NoPassageNot(NoPassage):
    pass


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


