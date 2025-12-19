from Day import Day


class y25d12(Day):

    def __init__(
            self, auto_fetch: bool = True,
            auto_parse: bool = True) -> None:
        self.PRESENT_DIM = 3
        super().__init__(year='2025', day='12', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        items = self.puzzle_raw.split('\n\n')
        self.presents: dict[int, set[tuple[int, int]]] = {}
        for present in items[:-1]:
            i, present_shape = present.split(':')
            self.presents[int(i)] = set()
            present_shape_l = list(present_shape.replace('\n', ''))
            for x in range(self.PRESENT_DIM):
                for y in range(self.PRESENT_DIM):
                    if present_shape_l[self.PRESENT_DIM*x+y] == '#':
                        self.presents[int(i)].add((x, y))

        self.spaces = []
        for tree in items[-1].strip().split('\n'):
            size, nof_presents = tree.split(':')
            size_w, size_l = map(int, size.split('x'))
            self.spaces.append(((size_w, size_l), list(map(int, nof_presents.split()))))

    def get_all_rotations(self, pts):
        def rotate(p): return sorted([(y, 2 - x) for x, y in p])
        r0 = sorted(list(pts))
        r1 = rotate(r0)
        r2 = rotate(r1)
        r3 = rotate(r2)
        return list({tuple(r) for r in [r0, r1, r2, r3]})

    def solve_part_1(self) -> int:
        # Pre-rotate all shapes
        self.shape_library = {sid: self.get_all_rotations(pts) for sid, pts in self.presents.items()}
        present_ids = sorted(self.presents.keys())
        total_success = 0

        for space_idx, ((W, L), counts) in enumerate(self.spaces):
            # 1. Generate Bitmasks for this specific space size
            task_data = []
            for i, count in enumerate(counts):
                if count <= 0:
                    continue
                sid = present_ids[i]
                masks = []
                for rot in self.shape_library[sid]:
                    for x in range(W - self.PRESENT_DIM + 1):
                        for y in range(L - self.PRESENT_DIM + 1):
                            m = 0
                            for px, py in rot:
                                m |= (1 << ((x + px) * L + (y + py)))
                            masks.append(m)
                # Sort masks to help consistent pruning
                task_data.append({'masks': sorted(list(set(masks))), 'count': count})

            # Sort tasks by "most difficult first" (largest shapes or fewest options)
            task_data.sort(key=lambda x: len(x['masks']))

            # 2. Optimized Backtrack
            memo = {}

            def backtrack(t_idx, current_board, last_mask_idx):
                state = (t_idx, current_board, last_mask_idx)
                if state in memo:
                    return memo[state]

                if t_idx == len(task_data):
                    return True

                task = task_data[t_idx]
                masks = task['masks']

                for i in range(last_mask_idx, len(masks)):
                    m = masks[i]
                    if not (current_board & m):
                        if task['count'] > 1:
                            # Still placing the same type of shape
                            task['count'] -= 1
                            if backtrack(t_idx, current_board | m, i + 1):
                                return True
                            task['count'] += 1
                        else:
                            # Move to next shape type
                            if backtrack(t_idx + 1, current_board | m, 0):
                                return True

                memo[state] = False
                return False

            if backtrack(0, 0, 0):
                total_success += 1
                print(f"Space {space_idx}: Success")
            else:
                print(f"Space {space_idx}: Failed")

        return total_success

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
