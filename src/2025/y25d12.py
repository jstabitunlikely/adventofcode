from Day import Day
import pycsp3  # type: ignore
from functools import lru_cache
from itertools import combinations_with_replacement, combinations


class y25d12(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        self.PRESENT_DIM = 3
        super().__init__(year='2025', day='12', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        items = self.puzzle_raw.split('\n\n')
        # Presents
        self.presents: dict[int, list[tuple[int, int]]] = {}
        for present in items[:-1]:
            i, present_shape = present.split(':')
            self.presents[int(i)] = []
            present_shape_l = list(present_shape.replace('\n', ''))
            for x in range(self.PRESENT_DIM):
                for y in range(self.PRESENT_DIM):
                    if present_shape_l[self.PRESENT_DIM*x+y] == '#':
                        self.presents[int(i)].append((x, y))
        # Spaces under trees
        self.spaces: list = []
        for tree in items[-1].strip().split('\n'):
            size, nof_presents = tree.split(':')
            size_w, size_l = size.split('x')
            self.spaces.append(((int(size_w), int(size_l)), list(map(int, nof_presents.split()))))

    def get_all_rotations(self, offsets):
        """Generates 4 rotations for a shape within a 3x3 grid."""
        def rotate(pts): return sorted([(y, 2 - x) for x, y in pts])

        r0 = sorted(offsets)
        r1 = rotate(r0)
        r2 = rotate(r1)
        r3 = rotate(r2)
        # Use a tuple for the list of rotations to make it hashable for caching
        return [tuple(r0), tuple(r1), tuple(r2), tuple(r3)]

    @lru_cache(maxsize=None)
    def get_safe_table(self, type_i, type_j):
        """Returns allowed (r_i, r_j, dx, dy) where dx = xi - xj + PRESENT_DIM."""
        valid_tuples = []
        rots_i = self.shape_library[type_i]
        rots_j = self.shape_library[type_j]

        for ri in range(self.PRESENT_DIM+1):
            for rj in range(self.PRESENT_DIM+1):
                # Check relative distance offsets from -3 to 3
                for dx in range(-self.PRESENT_DIM, self.PRESENT_DIM+1):
                    for dy in range(-self.PRESENT_DIM, self.PRESENT_DIM+1):
                        # Check for overlap
                        overlap = False
                        for (xi, yi) in rots_i[ri]:
                            # Translate point to present J's space
                            if (xi - dx, yi - dy) in rots_j[rj]:
                                overlap = True
                                break
                        if not overlap:
                            valid_tuples.append((ri, rj, dx + self.PRESENT_DIM, dy + self.PRESENT_DIM))
        return valid_tuples

    def solve_part_1(self) -> int:
        # Pre-calculate rotations for each unique present type
        print("Pre-calculating shape_library... ", end='')
        self.shape_library = {name: self.get_all_rotations(pts) for name, pts in self.presents.items()}
        print("done.")

        regions = 0
        for space_idx, ((space_w, space_h), counts) in enumerate(self.spaces):
            pycsp3.clear()

            present_instances = []
            present_ids = sorted(self.presents.keys())
            for shape_id, count in zip(present_ids, counts):
                present_instances.extend([shape_id] * count)

            n = len(present_instances)
            print(f"Solving space {space_idx}: {n} presents in {space_w}x{space_h}...")

            # CSP MODEL
            # x, y: top-left anchor of the bounding box
            x = pycsp3.VarArray(size=n, dom=range(space_w - 2))
            y = pycsp3.VarArray(size=n, dom=range(space_h - 2))
            # r: rotation
            r = pycsp3.VarArray(size=n, dom=range(4))

            # Before the combinations loop:
            # for i in range(n - 1):
            #     if present_instances[i] == present_instances[i+1]:
            #         # Force a specific spatial order for identical shapes
            #         pycsp3.satisfy(
            #             (x[i] < x[i+1]) | ((x[i] == x[i+1]) & (y[i] <= y[i+1]))
            #         )

            # Constraint: No Overlap between any two presents
            for i, j in combinations(range(n), 2):
                # # If the 3x3 bounding boxes don't even touch, skip the complex table
                # # This mathematical constraint is handled natively and very fast.
                # pycsp3.satisfy(
                #     (x[i] + 3 <= x[j]) | (x[j] + 3 <= x[i]) |  # type: ignore
                #     (y[i] + 3 <= y[j]) | (y[j] + 3 <= y[i]) |
                #     # Only if the above are ALL false, evaluate the table:
                #     ((r[i], r[j], (x[i] - x[j]) + 3, (y[i] - y[j]) + 3)
                #      in self.get_safe_table(present_instances[i], present_instances[j]))
                # )

                # Get the pre-calculated safe relative positions
                table = self.get_safe_table(present_instances[i], present_instances[j])

                # # Aux vars for relative distance: 0..(2*PRESENT_DIM)
                max_dist = max(space_w, space_h) + self.PRESENT_DIM
                dx_rel = pycsp3.Var(dom=range(-max_dist, max_dist), id=f"dx_{i}_{j}")
                dy_rel = pycsp3.Var(dom=range(-max_dist, max_dist), id=f"dy_{i}_{j}")

                pycsp3.satisfy(
                    dx_rel == (x[i] - x[j]) + self.PRESENT_DIM,  # type: ignore
                    dy_rel == (y[i] - y[j]) + self.PRESENT_DIM  # type: ignore
                )

                pycsp3.satisfy(
                    ((dx_rel >= 0) & (dx_rel <= 2*self.PRESENT_DIM) & (dy_rel >= 0) & (dy_rel <= 2*self.PRESENT_DIM)) >>  # type: ignore
                    ((r[i], r[j], dx_rel, dy_rel) in table)                             # type: ignore
                )

                # Breaking symmetry
                # If present i and i+1 are the same shape, force a specific order
                for i in range(n - 1):
                    if present_instances[i] == present_instances[i+1]:
                        pycsp3.satisfy(x[i] <= x[i+1])

            # SOLVE
            if pycsp3.solve() is pycsp3.SAT:
                regions += 1
                # print(f"{space_idx}: Success! Found arrangement for {n} presents.")
                # for i in range(n):
                #     print(
                #         f"\tPresent {i} ({present_instances[i]}): pos=({pycsp3.value(x[i])}, {pycsp3.value(y[i])}) rot={pycsp3.value(r[i])*90}°")
            # else:
                # print(f"{space_idx}: No valid arrangement exists for this area.")

        return regions

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
