from Day import Day
from Map import Map
from Coordinate import Coordinate


class Day20(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='20', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        self.puzzle = Map(self.puzzle_raw, str)

    def get_track(self,
                  start: Coordinate,
                  end: Coordinate) -> list[Coordinate]:
        track = [start]
        pp = start
        p = start
        while p != end:
            pn = [n[0] for n in self.puzzle.get_neighbors(p, '^>v<') if n[1] in '.SE' and n[0] != pp][0]
            track.append(pn)
            pp = p
            p = pn
        return track

    def solve_part_1(self,
                     cheat_max: int = 2,
                     limit: int = 100) -> int:
        endpoints = self.puzzle.find_first_elements(['S', 'E'])
        track = self.get_track(endpoints['S'], endpoints['E'])
        cheats = []
        # track_len = len(track)
        for i, p1 in enumerate(track[:-1]):
            # REVISIT: runtime is ~3m
            # if not i % (track_len//100+1):
            #     print(f'.', end='')
            p2s = [p2 for p2 in track[i+1:] if 0 < self.puzzle.get_distance(p1, p2) <= cheat_max]
            cheat = [track[i:].index(p2) - self.puzzle.get_distance(p1, p2) for p2 in p2s]
            cheat = [c for c in cheat if c > 0]
            cheats.extend(cheat)
        return len([c for c in cheats if c >= limit])

    def solve_part_2(self, limit: int = 100) -> int:
        return self.solve_part_1(cheat_max=20, limit=limit)


def main() -> dict[str, int]:  # pragma: no cover
    today = Day20()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
