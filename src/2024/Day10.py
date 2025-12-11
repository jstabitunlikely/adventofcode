from Day import Day
from Map import Map
from Coordinate import Coordinate


class Day10(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='10', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        self.puzzle = Map(self.puzzle_raw, int)

    def find_trailheads(self,
                        trailhead: int = 0) -> list[Coordinate]:
        return self.puzzle.find_all_element(trailhead)

    def hike(self, position: Coordinate) -> list[Coordinate]:
        peaks = []
        for _, dir_ in self.puzzle.COMPASS.items():
            position_next = position + dir_
            height = self.puzzle.get_element(position)
            height_next = self.puzzle.get_element(position_next)
            # Stay on the trail
            if height_next == height + 1:
                # Arrived at the peak
                if height_next == 9:
                    peaks += [position_next]
                # Continue the hike
                else:
                    peaks += self.hike(position_next)
        return peaks

    def solve_part_1(self) -> dict[str, int]:
        self.puzzle.frame(-1)
        trailheads = self.find_trailheads()
        scores = 0
        ratings = 0
        for th in trailheads:
            peaks = self.hike(th)
            scores += len(set(peaks))
            ratings += len(peaks)
        return {
            'part_1': scores,
            'part_2': ratings,
        }

    solve_part_2 = solve_part_1


def main() -> dict[str, int]:  # pragma: no cover
    today = Day10()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
