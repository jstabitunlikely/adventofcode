from Day import Day
from itertools import permutations

from Map import Map
from Coordinate import Coordinate


class Day08(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='08', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        self.puzzle = Map(self.puzzle_raw, str)

    def find_antennas(self) -> dict[str, list[Coordinate]]:
        antennas: dict[str, list[Coordinate]] = {}
        for c, v in self.puzzle.enumerate_map():
            if v == '.':
                continue
            if v not in antennas.keys():
                antennas[v] = []
            antennas[v].append(c)
        return antennas

    def solve_part_1(self, resonant_harmonics: bool = False) -> int:
        antinodes = set()
        for antlist in self.find_antennas().values():
            for ant1, ant2 in list(permutations(antlist, 2)):
                n = 1 if resonant_harmonics else 2
                while True:
                    node = n*ant1 - (n-1)*ant2
                    if self.puzzle.has_coordinate(node):
                        antinodes.add(node)
                    else:
                        break
                    if not resonant_harmonics:
                        break
                    n += 1
        return len(antinodes)

    def solve_part_2(self):
        return self.solve_part_1(resonant_harmonics=True)


def main() -> dict[str, str]:  # pragma: no cover
    today = Day08()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
