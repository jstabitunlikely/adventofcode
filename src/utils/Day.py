from abc import ABC, abstractmethod
from typing import Any
from InputFetcher import InputFetcher


class Day(ABC):

    def __init__(self,
                 year: str,
                 day: str,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        self.year = year
        self.day = day
        if auto_fetch:
            self.pif = InputFetcher(year=year, day=day)
            self.puzzle_raw = self.pif.input_
            if auto_parse:
                self.parse_puzzle()
        self.answer = {
            'part_1': '',
            'part_2': '',
        }

    @abstractmethod
    def parse_puzzle(self):
        if self.puzzle_raw is None:
            raise ValueError('self.puzzle_input is None!')

    @abstractmethod
    def solve_part_1(self) -> Any:
        pass

    @abstractmethod
    def solve_part_2(self) -> Any:
        pass

    def solve(self) -> dict[str, Any]:
        # Sometimes part 1-2 are solved in one step
        p1 = self.solve_part_1()
        if isinstance(p1, dict):
            assert list(p1.keys()) == ['part_1', 'part_2']
            self.answer = p1
        else:
            self.answer['part_1'] = p1
            self.answer['part_2'] = self.solve_part_2()
        return self.answer
