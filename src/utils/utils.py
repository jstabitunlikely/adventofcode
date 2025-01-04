from Coordinate import Coordinate

def sign(num):
    if num < 0:
        return -1
    if num > 0:
        return 1
    return 0

def is_on_map(c: Coordinate, map_: list[list[str]]) -> bool:
    return 0 <= c.x < len(map_) and 0 <= c.y < len(map_[0])
