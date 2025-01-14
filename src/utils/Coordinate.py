class Coordinate:
    x = 0
    y = 0

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, rhs: object) -> object:
        x = self.x + rhs.x
        y = self.y + rhs.y
        return Coordinate(x, y)

    def __sub__(self, rhs: object) -> object:
        x = self.x - rhs.x
        y = self.y - rhs.y
        return Coordinate(x, y)

    def __abs__(self) -> object:
        x = abs(self.x)
        y = abs(self.y)
        return Coordinate(x, y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, rhs: object) -> bool:
        return self.x == rhs.x and self.y == rhs.y

    def __mul__(self, rhs: int) -> object:
        x = self.x * rhs
        y = self.y * rhs
        return Coordinate(x, y)

    def __rmul__(self, lhs: int) -> object:
        x = lhs * self.x
        y = lhs * self.y
        return Coordinate(x, y)

    def __repr__(self):
        return repr(f'({self.x},{self.y})')

    def get_neighbors(self,
                      x_max: int = 0,
                      y_max: int = 0,) -> list[object]:
        neighbors = [Coordinate(self.x-1, self.y), Coordinate(self.x, self.y+1),
                     Coordinate(self.x+1, self.y), Coordinate(self.x, self.y-1)]
        if x_max > 0:
            neighbors = [n for n in neighbors if 0 <= n.x <= x_max]
        if y_max > 0:
            neighbors = [n for n in neighbors if 0 <= n.y <= y_max]
        return neighbors
