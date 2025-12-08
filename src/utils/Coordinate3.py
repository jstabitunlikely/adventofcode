from __future__ import annotations
import math


class Coordinate3():

    def __init__(self,
                 x: int = 0,
                 y: int = 0,
                 z: int = 0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, rhs: Coordinate3) -> Coordinate3:
        x = self.x + rhs.x
        y = self.y + rhs.y
        z = self.z + rhs.z
        return Coordinate3(x, y, z)

    def __sub__(self, rhs: Coordinate3) -> Coordinate3:
        x = self.x - rhs.x
        y = self.y - rhs.y
        z = self.z - rhs.z
        return Coordinate3(x, y)

    def __abs__(self) -> Coordinate3:
        x = abs(self.x)
        y = abs(self.y)
        z = abs(self.z)
        return Coordinate3(x, y, z)

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.y))

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Coordinate3):
            # If we return NotImplemented, Python will automatically try
            # running rhs.__eq__(self), in case 'rhs' knows what to do with
            # Coordinate3 objects.
            return NotImplemented
        return self.x == rhs.x and self.y == rhs.y and self.y == rhs.y

    def __mul__(self, rhs: int) -> Coordinate3:
        x = self.x * rhs
        y = self.y * rhs
        z = self.z * rhs
        return Coordinate3(x, y, z)

    def __rmul__(self, lhs: int) -> Coordinate3:
        x = lhs * self.x
        y = lhs * self.y
        z = lhs * self.z
        return Coordinate3(x, y, z)

    def __repr__(self):
        return repr(f'({self.x},{self.y},{self.z})')

    def get_distance_abs(self, c: Coordinate3) -> int:
        diff = abs(self - c)
        return diff.x + diff.y + diff.z

    def get_distance_euclidean(self, c: Coordinate3) -> float:
        x_diff_sq = (c.x - self.x) ** 2
        y_diff_sq = (c.y - self.y) ** 2
        z_diff_sq = (c.z - self.z) ** 2
        return math.sqrt(x_diff_sq + y_diff_sq + z_diff_sq)
