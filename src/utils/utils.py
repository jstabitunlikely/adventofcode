import math
from Coordinate import Coordinate


def sign(num: int) -> int:
    if num < 0:
        return -1
    if num > 0:
        return 1
    return 0


def is_on_map(c: Coordinate,
              map_: list[list[str]]) -> bool:
    # Deprecated function
    # TODO: remove and use Matrix class instead
    return 0 <= c.x < len(map_) and 0 <= c.y < len(map_[0])


def is_int(number,
           rel_tol=1e-9):
    return math.isclose(number, round(number), rel_tol=rel_tol)
