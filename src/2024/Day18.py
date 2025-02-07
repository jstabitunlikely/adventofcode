from Day import Day
import networkx as nx

from Coordinate import Coordinate


class Day18(Day):

    def __init__(self,
                 ram_size: int = 71,
                 byte_num: int = 1024,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='18', auto_fetch=auto_fetch, auto_parse=auto_parse)
        self.RAM_SIZE = ram_size
        self.BYTE_NUM = byte_num

    def parse_puzzle(self) -> None:
        raw_split = self.puzzle_raw.strip()
        y_x = [c.split(',') for c in raw_split.split('\n')]
        x_y = [Coordinate(int(x), int(y)) for y, x in y_x]
        self.puzzle = x_y

    def build_graph(self,
                    ram_size: int,
                    bytz: list[Coordinate]) -> nx.Graph:
        xy_max = ram_size-1
        R = nx.Graph()
        for x in range(xy_max+1):
            for y in range(xy_max+1):
                node = Coordinate(x, y)
                if node not in bytz:
                    R.add_node(node)
                    # Note: not the most efficient as it will add every edge twice (once from both directions)
                    [R.add_edge(node, n, weight=1) for n in node.get_neighbors(xy_max, xy_max) if n not in bytz]
        return R

    def solve_part_1(self) -> int:
        R = self.build_graph(self.RAM_SIZE, self.puzzle[:self.BYTE_NUM])
        source = Coordinate(0, 0)
        target = Coordinate(self.RAM_SIZE-1, self.RAM_SIZE-1)
        return nx.shortest_path_length(R, source, target)

    def solve_part_2(self) -> str:
        R = self.build_graph(self.RAM_SIZE, [])
        source = Coordinate(0, 0)
        target = Coordinate(self.RAM_SIZE-1, self.RAM_SIZE-1)
        for b in self.puzzle:
            R.remove_node(b)
            if not nx.has_path(R, source, target):
                break
        return ','.join(map(str, [b.y, b.x]))


def main() -> dict[str, str]:  # pragma: no cover
    today = Day18()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
