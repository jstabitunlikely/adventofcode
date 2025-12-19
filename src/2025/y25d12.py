from Day import Day
import numpy as np
import numpy.typing as npt


class y25d12(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2025', day='12', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        items = self.puzzle_raw.split('\n\n')
        # Presents
        self.presents: list[npt.NDArray] = []
        for present in items[:-1]:
            _, present_shape = present.split(':')
            p = [[1 if char == '#' else 0 for char in row] for row in present_shape.strip().split('\n')]
            self.presents.append(np.array(p, dtype=np.int8))
        # Spaces under trees
        self.spaces = []
        for tree in items[-1].strip().split('\n'):
            size, nof_presents = tree.split(':')
            size_w, size_l = size.split('x')
            self.spaces.append(((int(size_w), int(size_l)), list(map(int, nof_presents.split()))))

    def solve_part_1(self) -> int:
        nof_ok = 0
        for ((width, height), counts) in self.spaces:
            nof_tiles = 0
            for present_id, count in enumerate(counts):
                p = self.presents[present_id]
                nof_tiles += np.sum(p) * count
            if nof_tiles <= width * height:
                nof_ok += 1
        return nof_ok

    def solve_part_2(self) -> int:
        return 0


def main() -> dict[str, int]:  # pragma: no cover
    today = y25d12()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
