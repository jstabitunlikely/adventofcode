import sys
import numpy as np
import numpy.typing as npt
from itertools import product

import InputFetcher
from Map import Map

EXAMPLE = """\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####\
"""


def parse_input(example: bool) -> dict[str, list[npt.NDArray]]:
    data = EXAMPLE if example else InputFetcher.fetch_input('2024', '25')
    schematics = data.split('\n\n')
    schematics_digital: dict[str, list[npt.NDArray]] = {
        'locks': [],
        'keys': [],
    }
    for sch in schematics:
        sch_str = Map(sch, str)
        sch_int = [list(map(lambda x: 1 if x == '#' else 0, l)) for l in sch_str.map_]
        sch_arr = np.array(sch_int)
        if all(sch_arr[0]):
            k = 'keys'
        elif all(sch_arr[-1]):
            k = 'locks'
        schematics_digital[k].append(sch_arr)
    return schematics_digital


def solve_1(schematics: dict[str, list[npt.NDArray]]) -> int:
    fits = 0
    for lock, key in product(schematics['keys'], schematics['locks']):
        fits += not np.any(np.bitwise_and(lock, key))
    return fits


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    schematics = parse_input(use_example)
    result_1 = solve_1(schematics)
    if use_example:
        assert result_1 == 3, result_1
    print(f'Result 1: {result_1}')
