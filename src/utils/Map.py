from __future__ import annotations
from typing import Generator, Any, Callable

from Coordinate import Coordinate


class Map:

    def __init__(self,
                 map_: Any,
                 type_: type = int) -> None:
        if isinstance(map_, str):
            self.map_ = self.parse(map_, type_)
        else:
            self.map_ = map_
        assert isinstance(self.map_, list) and isinstance(self.map_[0], list) and isinstance(self.map_[0][0], type_), \
            'Map must be a list[list[type_]] or a string to be parsed into list[list[type_]!'
        self.x_max = len(self.map_) - 1
        self.y_max = len(self.map_[0]) - 1
        self.DIRECTIONS = "^>v<"
        self.COMPASS = {
            self.DIRECTIONS[0]: Coordinate(-1, 0),
            self.DIRECTIONS[1]: Coordinate(0, 1),
            self.DIRECTIONS[2]: Coordinate(1, 0),
            self.DIRECTIONS[3]: Coordinate(0, -1),
        }

    def parse(self,
              string: str,
              type_: Callable = int) -> list[list[Any]]:
        """
        Parses a string representation of a 2D map_ and converts it into a nested list of values.
        Assumption: lines are separated, elements are not.

        Args:
            string: A string representing the 2D map_. Each row in the map_ should be
                separated by whitespace (e.g., spaces, tabs, newlines).
            type_: An optional callable (e.g., int, float, str) that specifies the
                desired data type for the map_ elements. Defaults to int.

        Returns:
            A nested list representing the 2D map_, where each inner list corresponds
            to a row in the map_, and each element within the inner lists is of the
            specified type.
        """
        map_ = [list(line) for line in string.split()]
        map_ = [list(map(type_, line)) for line in map_]
        return map_

    def enumerate_coordinates(self) -> Generator[tuple[Coordinate, Any], None, None]:
        for x, row in enumerate(self.map_):
            for y, n in enumerate(row):
                yield Coordinate(x, y), n

    def has_coordinate(self,
                       coordinate: Coordinate) -> bool:
        return 0 <= coordinate.x <= self.x_max and 0 <= coordinate.y <= self.y_max

    def find_elements(self,
                      elements: list[Any]) -> dict[str, Any]:
        results = {}
        for p, e in self.enumerate_coordinates():
            if e in elements:
                results[e] = p
        return results

    def get_element(self,
                    coordinate: Coordinate) -> Any:
        if not self.has_coordinate(coordinate):
            raise ValueError(f'Coordinate {coordinate} is not in the map_!')
        return self.map_[coordinate.x][coordinate.y]

    def set_element(self,
                    coordinate: Coordinate,
                    value: Any):
        if not self.has_coordinate(coordinate):
            raise ValueError(f'Coordinate {coordinate} is not in the map_!')
        self.map_[coordinate.x][coordinate.y] = value

    def get_neighbor_coordinates_by_direction(self,
                                              coordinate: Coordinate,
                                              direction: str,
                                              distance: int = 1) -> dict[str, list[Coordinate]]:
        neighbors = {}
        for d in direction:
            neighbors[d] = [coordinate + n*self.COMPASS[d] for n in range(1, distance+1)]
            neighbors[d] = [n for n in neighbors[d] if self.has_coordinate(n)]
        return neighbors

    def get_neighbor_coordinates(self,
                                 coordinate: Coordinate,
                                 direction: str,
                                 distance: int = 1) -> list[Coordinate]:
        coordinates_by_direction = self.get_neighbor_coordinates_by_direction(
            coordinate=coordinate, direction=direction, distance=distance)
        coordinates = []
        for c in coordinates_by_direction.values():
            coordinates.extend(c)
        return coordinates

    def get_neighbors(self,
                      coordinate: Coordinate,
                      direction: str,
                      distance: int = 1) -> list[tuple[Coordinate, Any]]:
        coordinates = self.get_neighbor_coordinates(coordinate=coordinate, direction=direction, distance=distance)
        return [(c, self.get_element(c)) for c in coordinates]

    def get_neighbors_by_direction(self,
                                   coordinate: Coordinate,
                                   direction: str,
                                   distance: int = 1) -> dict[str, list[tuple[Coordinate, Any]]]:
        coordinates_by_direction = self.get_neighbor_coordinates_by_direction(
            coordinate=coordinate, direction=direction, distance=distance)
        neighbors_by_direction = {}
        for d, coordinates in coordinates_by_direction.items():
            neighbors_by_direction[d] = [(c, self.get_element(c)) for c in coordinates]
        return neighbors_by_direction

    def get_neighbor_coordinates_by_range(self,
                                          coordinate: Coordinate,
                                          range_: int) -> list[Coordinate]:
        hood = []
        for x in range(0, range_+1):
            for y in range(0, (range_-x)+1):
                hood.append(coordinate + Coordinate(+x, +y))
                if x:
                    hood.append(coordinate + Coordinate(-x, +y))
                if y:
                    hood.append(coordinate + Coordinate(+x, -y))
                if x and y:
                    hood.append(coordinate + Coordinate(-x, -y))
        return [p for p in hood if self.has_coordinate(p)]

    def get_distance(self,
                     p1: Coordinate,
                     p2: Coordinate) -> int:
        return p1.get_distance(p2)
