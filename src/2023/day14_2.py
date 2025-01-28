from day14_input import example as dish
# from day14_input import puzzle_input as dish

def get_rock_indices( dish, orientation='north'):
    if orientation == 'north':
        dish_height = len(dish)
    elif 'south' == orientation:
        dish_height = 0
        dish = dish[::-1]

    dish_width = len(dish[0])
    last_square_idxs = [-1] * dish_width
    round_cnts = [0] * dish_width

    round_idxs_oriented = []
    round_idxs_all = []
    for li, line in enumerate(dish):
        square_idxs = [i for i, rock in enumerate(line) if rock == '#']
        for s in square_idxs:
            last_square_idxs[s] = li
            round_cnts[s] = 0

        round_idxs = [i for i, rock in enumerate(line) if rock == 'O']
        round_idxs_all.append(round_idxs)
        round_idxs_oriented.append( [last_square_idxs[r]+1 + round_cnts[r] for r in round_idxs])
        for r in round_idxs:
            round_cnts[r] += 1
    print(round_idxs_all)
    return round_idxs_oriented

def main():
    idx = get_rock_indices(dish)
    print(idx)

if __name__ == '__main__':
    main()
