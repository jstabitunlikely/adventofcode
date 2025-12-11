from Day import Day
import networkx as nx


class y25d11(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2025', day='11', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        self.puzzle = []
        for device in self.puzzle_raw.strip().split('\n'):
            device_id, device_connections = device.split(':')
            self.puzzle.append((device_id, device_connections.split()))

    def solve_part_1(self) -> int:
        network = nx.DiGraph()
        for dev_id, dev_conn in self.puzzle:
            for o in dev_conn:
                network.add_edge(dev_id, o)
        nof_paths = len(list(nx.all_simple_paths(network, 'you', 'out')))
        return nof_paths

    def solve_part_2(self) -> int:
        return 0


def main() -> dict[str, str]:  # pragma: no cover
    today = y25d11()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
