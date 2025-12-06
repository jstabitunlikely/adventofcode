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

    def enumerate_map(self) -> Generator[tuple[Coordinate, Any], None, None]:
        for x, row in enumerate(self.map_):
            for y, n in enumerate(row):
                yield Coordinate(x, y), n

    def has_coordinate(self,
                       coordinate: Coordinate) -> bool:
        return 0 <= coordinate.x <= self.x_max and 0 <= coordinate.y <= self.y_max

    def get_all_elements_by_condition(self,
                                      condition: Callable) -> Any:
        return [e for _, e in self.enumerate_map() if condition(e)]

    def get_first_element_by_condition(self,
                                       condition: Callable) -> Any:
        return self.get_all_elements_by_condition(condition=condition)[0]

    def find_all_elements_by_condition(self,
                                       condition: Callable) -> Any:
        return [c for c, e in self.enumerate_map() if condition(e)]

    def find_all_element(self,
                         element: Any) -> list[Coordinate]:
        return [p for p, e in self.enumerate_map() if e == element]

    def find_first_element(self,
                           element: Any) -> Coordinate:
        return self.find_all_element(element)[0]

    def find_first_elements(self,
                            elements: list[Any]) -> dict[Any, Coordinate]:
        results: dict[Any, Coordinate] = {}
        found = self.find_all_elements(elements)
        for k, v in found.items():
            results[k] = v[0]  # type:ignore
        return results

    def find_all_elements(self,
                          elements: list[Any]) -> dict[Any, list[Coordinate]]:
        results: dict[Any, list[Coordinate]] = {}
        for p, e in self.enumerate_map():
            if e not in elements:
                continue
            if e not in results.keys():
                results[e] = [p]
            else:
                results[e].append(p)
        return results

    def get_element(self,
                    coordinate: Coordinate,
                    check_edges: bool = True) -> Any:
        if not self.has_coordinate(coordinate):
            if check_edges:
                raise ValueError(f'Coordinate {coordinate} is not in the map_!')
            else:
                return None
        return self.map_[coordinate.x][coordinate.y]

    def set_element(self,
                    coordinate: Coordinate,
                    value: Any):
        if not self.has_coordinate(coordinate):
            raise ValueError(f'Coordinate {coordinate} is not in the map_!')
        self.map_[coordinate.x][coordinate.y] = value

    def frame(self,
              frame: Any = -1) -> None:
        self.map_ = [[frame]*self.y_max] + self.map_ + [[frame]*self.y_max]
        self.map_ = [[frame] + row + [frame] for row in self.map_]
        self.x_max += 2
        self.y_max += 2

    # TODO push down mindless math into Coordinate, leaving edge and value handling in Map

    def get_neighbor_coordinates_by_direction(self,
                                              coordinate: Coordinate,
                                              direction: str,
                                              distance: int = 1,
                                              check_edges: bool = True) -> dict[str, list[Coordinate]]:
        neighbors = {}
        for d in direction:
            neighbors[d] = [coordinate + n*self.COMPASS[d] for n in range(1, distance+1)]
            if check_edges:
                neighbors[d] = [n for n in neighbors[d] if self.has_coordinate(n)]
        return neighbors

    def get_neighbor_coordinates(self,
                                 coordinate: Coordinate,
                                 direction: str,
                                 distance: int = 1,
                                 check_edges: bool = True) -> list[Coordinate]:
        coordinates_by_direction = self.get_neighbor_coordinates_by_direction(
            coordinate=coordinate, direction=direction, distance=distance, check_edges=check_edges)
        coordinates = []
        for c in coordinates_by_direction.values():
            coordinates.extend(c)
        return coordinates

    def get_neighbors(self,
                      coordinate: Coordinate,
                      direction: str,
                      distance: int = 1,
                      check_edges: bool = True) -> list[tuple[Coordinate, Any]]:
        coordinates = self.get_neighbor_coordinates(
            coordinate=coordinate, direction=direction, distance=distance, check_edges=check_edges)
        return [(c, self.get_element(c, check_edges=False)) for c in coordinates]

    def get_neighbors_by_direction(self,
                                   coordinate: Coordinate,
                                   direction: str,
                                   distance: int = 1,
                                   check_edges: bool = True) -> dict[str, list[tuple[Coordinate, Any]]]:
        coordinates_by_direction = self.get_neighbor_coordinates_by_direction(
            coordinate=coordinate, direction=direction, distance=distance, check_edges=check_edges)
        neighbors_by_direction = {}
        for d, coordinates in coordinates_by_direction.items():
            neighbors_by_direction[d] = [(c, self.get_element(c)) for c in coordinates]
        return neighbors_by_direction

    def get_neighbor_coordinates_by_range(self,
                                          coordinate: Coordinate,
                                          range_: int,
                                          check_edges: bool = True) -> list[Coordinate]:
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
        if check_edges:
            hood = [p for p in hood if self.has_coordinate(p)]
        return hood

    def get_neighbors_by_range(self,
                               coordinate: Coordinate,
                               range_: int,
                               check_edges: bool = True) -> list[Any]:
        coordinates_by_range = self.get_neighbor_coordinates_by_range(
            coordinate=coordinate, range_=range_, check_edges=check_edges)
        neighbors_by_range = []
        for c in coordinates_by_range:
            neighbors_by_range.append(self.get_element(c))
        return neighbors_by_range

    def get_neighbor_coordinates_around(self,
                                        coordinate: Coordinate,
                                        range_: int,
                                        check_edges: bool = True,
                                        include_me: bool = False) -> list[Coordinate]:
        hood = []
        for x in range(0, range_+1):
            for y in range(0, (range_)+1):
                if x == 0 and y == 0 and not include_me:
                    continue
                hood.append(coordinate + Coordinate(+x, +y))
                if x:
                    hood.append(coordinate + Coordinate(-x, +y))
                if y:
                    hood.append(coordinate + Coordinate(+x, -y))
                if x and y:
                    hood.append(coordinate + Coordinate(-x, -y))
        if check_edges:
            hood = [p for p in hood if self.has_coordinate(p)]
        return hood

    def get_neighbors_around(self,
                             coordinate: Coordinate,
                             range_: int,
                             check_edges: bool = True,
                             include_me: bool = False) -> list[Any]:
        coordinates_around = self.get_neighbor_coordinates_around(
            coordinate=coordinate, range_=range_, check_edges=check_edges, include_me=include_me)
        neighbors_around = []
        for c in coordinates_around:
            neighbors_around.append(self.get_element(c))
        return neighbors_around

    def get_distance(self,
                     p1: Coordinate,
                     p2: Coordinate) -> int:
        return p1.get_distance(p2)
