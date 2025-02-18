from __future__ import annotations
from typing import Union


class Coordinate():

    DIRECTIONS = "^>v<"

    COMPASS = {
        DIRECTIONS[0]: (-1, 0),
        DIRECTIONS[1]: (0, 1),
        DIRECTIONS[2]: (1, 0),
        DIRECTIONS[3]: (0, -1),
    }

    def __init__(self,
                 x: int = 0,
                 y: int = 0):
        self.x = x
        self.y = y

    def __add__(self, rhs: Coordinate) -> Coordinate:
        x = self.x + rhs.x
        y = self.y + rhs.y
        return Coordinate(x, y)

    def __sub__(self, rhs: Coordinate) -> Coordinate:
        x = self.x - rhs.x
        y = self.y - rhs.y
        return Coordinate(x, y)

    def __abs__(self) -> Coordinate:
        x = abs(self.x)
        y = abs(self.y)
        return Coordinate(x, y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Coordinate):
            # If we return NotImplemented, Python will automatically try
            # running rhs.__eq__(self), in case 'rhs' knows what to do with
            # Coordinate objects.
            return NotImplemented
        return self.x == rhs.x and self.y == rhs.y

    def __mul__(self, rhs: int) -> Coordinate:
        x = self.x * rhs
        y = self.y * rhs
        return Coordinate(x, y)

    def __rmul__(self, lhs: int) -> Coordinate:
        x = lhs * self.x
        y = lhs * self.y
        return Coordinate(x, y)

    def __repr__(self):
        return repr(f'({self.x},{self.y})')

    def get_distance(self, c: Coordinate) -> int:
        diff = abs(self - c)
        return diff.x + diff.y

    def get_neighbor(self, dir_: Union[str, int]) -> Coordinate:
        if type(dir_) == str:  # noqa: E721
            d = dir_
        elif type(dir_) == int:  # noqa: E721
            d = self.DIRECTIONS[dir_]
        nx = self.x + self.COMPASS[d][0]
        ny = self.y + self.COMPASS[d][1]
        return Coordinate(nx, ny)

    # TODO: pull in similar methods from Map

    def get_neighbors(self,
                      x_max: int = 0,
                      y_max: int = 0,
                      dist: int = 1) -> list[Coordinate]:
        neighbors = [Coordinate(self.x-dist, self.y), Coordinate(self.x, self.y+dist),
                     Coordinate(self.x+dist, self.y), Coordinate(self.x, self.y-dist)]
        if x_max > 0:
            neighbors = [n for n in neighbors if 0 <= n.x <= x_max]
        if y_max > 0:
            neighbors = [n for n in neighbors if 0 <= n.y <= y_max]
        return neighbors
