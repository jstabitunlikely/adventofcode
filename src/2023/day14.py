from day14_input import example as dish
from day14_input import puzzle_input as dish


def main():
    dish_width = len(dish[0])
    dish_height = len(dish)

    last_square_idxs = [-1] * dish_width
    round_cnts = [0] * dish_width

    load = 0
    for li, line in enumerate(dish):
        square_idxs = [i for i, rock in enumerate(line) if rock == '#']
        for s in square_idxs:
            last_square_idxs[s] = li
            round_cnts[s] = 0

        round_idxs = [i for i, rock in enumerate(line) if rock == 'O']
        round_idxs_new = [last_square_idxs[r]+1 + round_cnts[r] for r in round_idxs]
        load += sum([dish_height - p for p in round_idxs_new])

        for r in round_idxs:
            round_cnts[r] += 1

    print(load)


if __name__ == '__main__':
    main()
