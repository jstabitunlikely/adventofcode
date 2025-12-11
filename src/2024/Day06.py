from Day import Day
from Map import Map
from Coordinate import Coordinate


class Day06(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='06', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        self.puzzle = Map(self.puzzle_raw, str)

    def turn_right(self, dir_: int) -> int:
        return (dir_ + 1) % 4

    def walk(self, guard: dict[str, Coordinate],
             lab: Map) -> tuple[set[Coordinate], bool]:
        guard_ = list(guard.items())[0]
        # Position of the guard
        p = guard_[1]
        # Direction of the guard as an integer
        idir = p.DIRECTIONS.index(guard_[0])
        # Unique positions visited
        visited = set([p])
        # Path history with directions
        path = set([(idir, p)])
        loop = False
        while True:
            # Look ahead
            p_next = p.get_neighbor(idir)
            # Check if we're at the edge of the map
            if not lab.has_coordinate(p_next):
                break
            # Check if there's an obstacle ahead
            while lab.get_element(p_next) == '#':
                idir = self.turn_right(idir)
                p_next = p.get_neighbor(idir)
            # Check if we're running in circles (for Part 2 only)
            if (idir, p_next) in path:
                loop = True
                break
            # Actually step ahead
            p = p_next
            # Save current position
            visited.add(p)
            path.add((idir, p))
        return visited, loop

    def solve_part_1(self) -> dict[str, int]:
        lab = self.puzzle
        guard = lab.find_first_elements(['^', '>', 'v', '<'])
        visited, _ = self.walk(guard, lab)
        num_visited = len(visited)
        # As per spec, we can't put an obstacle on the guard's starting position
        guard_pos = list(guard.items())[0][1]
        visited.remove(guard_pos)
        loops = 0
        # Try putting an obstacle onto each visited position (temporarily) and
        # do the walk again, checking if the new path has a loop
        for p in visited:
            lab.set_element(p, "#")
            _, loop = self.walk(guard, lab)
            loops += 1 if loop else 0
            lab.set_element(p, ".")
        return {
            'part_1': num_visited,
            'part_2': loops,
        }

    solve_part_2 = solve_part_1


def main() -> dict[str, int]:  # pragma: no cover
    today = Day06()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
