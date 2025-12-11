import re

from Day import Day
from Map import Map
from utils import transpose


class Day04(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='04', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        self.puzzle = Map(self.puzzle_raw, str).map_

    def solve_part_1(self) -> int:
        # horizontally
        xmas_hits = self.get_xmas_count(self.puzzle)

        # vertically
        xmas_hits += self.get_xmas_count(transpose(self.puzzle))

        # diagonally
        for i, row in enumerate(self.puzzle[:-3]):
            textrix_lsh = [row]
            textrix_rsh = [row]
            for j in range(1, 4):
                textrix_lsh.append(self.puzzle[i+j][j:] + j*['.'])  # shift left
                textrix_rsh.append(j*['.'] + self.puzzle[i+j][:-j])  # shift right
            xmas_hits += self.get_xmas_count(transpose(textrix_lsh))
            xmas_hits += self.get_xmas_count(transpose(textrix_rsh))
        return xmas_hits

    def solve_part_2(self) -> int:
        xmas_hits = 0
        for i in range(1, len(self.puzzle)-1):
            for j in range(1, len(self.puzzle[i])-1):
                if self.puzzle[i][j] != 'A':
                    continue
                else:
                    x = self.puzzle[i+1][j-1] + self.puzzle[i-1][j-1] + \
                        self.puzzle[i-1][j+1] + self.puzzle[i+1][j+1]
                    if x in ["MMSS", "MSSM", "SSMM", "SMMS"]:
                        xmas_hits += 1
        return xmas_hits

    def get_xmas_count(self,
                       puzzle: list[list[str]]) -> int:
        xmas_re = re.compile(r"(?=XMAS|SAMX)")
        count = 0
        for row in puzzle:
            count += len(re.findall(xmas_re, "".join(row)))
        return count


def main() -> dict[str, int]:  # pragma: no cover
    today = Day04()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
